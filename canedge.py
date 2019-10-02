import re
import io
import json
from enum import IntEnum
from typing import Generator, Dict
from jsonschema import validate, ValidationError
from collections import OrderedDict
from base64 import b64encode, b64decode
from Crypto.PublicKey import ECC
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes


class CANedgeReturnCodes(IntEnum):
    OK = 0,
    UNKNOWN_ERROR = 1,
    CONFIG_VALIDATION_ERROR = 2,
    CONFIG_NOT_FOUND_ERROR = 3,
    UNKNOWN_DEVICE_ID_ERROR = 4,


class CANEdgeSecurity(object):

    # Generate a new symmetric key using device public key
    @staticmethod
    def __gen_sym_key(device_public_key_string_xy):

        _ECC_CURVE = 'secp256r1'

        # Construct ECC point from device public key
        device_kpub_int_x = int.from_bytes(device_public_key_string_xy[:32], byteorder='big')
        device_kpub_int_y = int.from_bytes(device_public_key_string_xy[32:], byteorder='big')
        device_kpub_p = ECC.construct(curve=_ECC_CURVE, point_x=device_kpub_int_x, point_y=device_kpub_int_y)

        # Create user private / public key pair
        user_key_pair = ECC.generate(curve=_ECC_CURVE)

        # The shared secret is calculated using the device public point and the private key.
        # The secret is the x-coordinate of the resulting point
        shared_secret_int = (device_kpub_p.pointQ * user_key_pair.d).x

        # Calculate symmetric key from shared secret using hmac-sha256 and static data "config"
        shared_secret_string = int(shared_secret_int).to_bytes(32, byteorder='big')
        h = HMAC.new(shared_secret_string, msg=b'config', digestmod=SHA256)

        # Truncate to get shared private key (16 bytes)
        symmetric_key = h.digest()[0:16]

        # Create public key byte strings
        user_kpub_string_x = int(user_key_pair.pointQ.x).to_bytes(32, byteorder='big')
        user_kpub_string_y = int(user_key_pair.pointQ.y).to_bytes(32, byteorder='big')

        return symmetric_key, user_kpub_string_x + user_kpub_string_y

    def __init__(self, device_public_key_base64: str):

        # Generate shared secret (symmetric key)
        self.device_public_key_base64 = device_public_key_base64
        self.device_kpub_string_xy = b64decode(self.device_public_key_base64)
        self.ksym, self.user_kpub_string_xy = self.__gen_sym_key(self.device_kpub_string_xy)

    def encrypt_encode(self, field_value: str) -> str:
        # Create CTR cipher (the library creates a random nonce)
        iv = get_random_bytes(16)
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(self.ksym, AES.MODE_CTR, counter=ctr)

        # Encrypt data
        ct = cipher.encrypt(bytes(field_value, 'ascii'))

        # Concatenate and encode
        return b64encode(iv + ct).decode()

    @property
    def sym_key_base64(self) -> str:
        return b64encode(self.ksym).decode()

    @property
    def sym_key_base64(self) -> str:
        return b64encode(self.ksym).decode()

    @property
    def user_public_key_base64(self) -> str:
        if self.user_kpub_string_xy is None:
            exit("User public key not set")
        return b64encode(self.user_kpub_string_xy).decode()


class CANedgeConfig(object):

    def __init__(self, device_public_key_base64: str):
        # Create the security object, used to enctrypt fields in configuration
        self._security = CANEdgeSecurity(device_public_key_base64)
        pass

    @property
    def security(self) -> CANEdgeSecurity:
        return self._security

class CANedge(object):

    __VERSION = "00.00.02"

    def __init__(self, mc, bucket, fw_old_path, fw_new_path=None):

        self.mc = mc
        self.bucket = bucket
        self.fw_old_path = fw_old_path
        self.fw_new_path = fw_new_path if (fw_new_path is not None) else fw_old_path

        # Read fw binaries
        with open(self.fw_old_path, mode='rb') as file:
            fw_old_bin = file.read()

        with open(self.fw_new_path, mode='rb') as file:
            fw_new_bin = file.read()

        self.__fw_old = self.__parse_fw_bin(fw_old_bin)
        self.__fw_new = self.__parse_fw_bin(fw_new_bin)

        # Get devices matching the schema version
        self.__devices = []
        for device in self.__s3_get_devices():
            self.__devices.append(device)
        self.__devices = sorted(self.__devices, key=lambda k: k['id'])

    def __find_device_by_id(self, device_id):
        device = list(filter(lambda x: x['id'] == device_id, self.devices))
        return device[0] if device is not None else None

    # Parse a raw binary image
    @staticmethod
    def __parse_fw_bin(fw_bin):

        assert (fw_bin[0:4] == b"\xDE\xAD\x10\xCC") or (fw_bin[0:4] == b"\xBA\xAD\xA5\x55"), "Invalid fw binary"

        # Get firmware revision
        rev_major = fw_bin[4]
        rev_minor = fw_bin[5]
        rev_patch = fw_bin[6]
        rev_string = "{:02d}.{:02d}.{:02d}".format(rev_major, rev_minor, rev_patch)

        # Get schema
        schema_name = "schema-{:02d}.{:02d}.json".format(rev_major, rev_minor)
        schema_offset = int.from_bytes(fw_bin[24:28], byteorder='big')
        schema_nob = int.from_bytes(fw_bin[28:32], byteorder='big')
        schema = fw_bin[schema_offset:schema_offset + schema_nob].decode("utf-8")

        # Get config
        config_name = "config-{:02d}.{:02d}.json".format(rev_major, rev_minor)
        config_offset = int.from_bytes(fw_bin[32:36], byteorder='big')
        config_nob = int.from_bytes(fw_bin[36:40], byteorder='big')
        config = fw_bin[config_offset:config_offset + config_nob].decode("utf-8")

        return {"fw_ver": rev_string, "sch_name": schema_name, "sch": schema, "cfg_name": config_name, "cfg": config}

    def __s3_get_obj_string(self, obj_name):
        data_string = ""
        data = self.mc.get_object(self.bucket, obj_name)
        for d in data.stream(1024):
            data_string += d.decode('ascii')
        return data_string

    def __s3_put_obj_string(self, obj_name, string):
        data = io.BytesIO(string.encode())
        nob = data.getbuffer().nbytes
        self.mc.put_object(self.bucket, obj_name, data, nob)

    def __s3_get_devices(self) -> Generator[Dict, None, None]:
        """
        Fetch devices on server with matching schema name
        :return:
        """
        # Loop devices
        for obj1 in self.mc.list_objects(self.bucket, recursive=False):
            # Loop device files
            for obj2 in self.mc.list_objects(self.bucket, prefix=obj1.object_name, recursive=False):
                r = re.search(r'^([A-F0-9]{8})/device\.json$', obj2.object_name)
                if r:
                    # Load device file
                    device = json.loads(self.__s3_get_obj_string(obj2.object_name))

                    # If schema version matches, append to output
                    if device["sch_name"] == self.__fw_old["sch_name"]:
                        yield device

    @property
    def fw(self) -> str:
        return self.__fw_old["fw_ver"]

    @property
    def fw_migration(self) -> str:
        return self.__fw_new["fw_ver"]

    @property
    def devices(self) -> []:
        return self.__devices

    @property
    def device_ids(self) -> []:
        return list((x['id'] for x in self.__devices))

    @property
    def tool_version(self) -> str:
        return self.__VERSION

    # Update configuration
    def cfg_update(self, device_ids_to_update: [str], cfg_cb, config_name=None) -> Generator[Dict, None, None]:
        """
        Updates device configuration using provided migration function
        :param device_ids_to_update:
        :param cfg_cb:
        :param config_name:
        :return: generator
        """
        # Loop devices
        for index, device_id in enumerate(device_ids_to_update):

            res = {"res": CANedgeReturnCodes.OK, "id": device_id, "msg": None}

            # Check if device id is in list of known devices
            device = self.__find_device_by_id(device_id)
            if device is None:
                res = {"res": CANedgeReturnCodes.UNKNOWN_DEVICE_ID_ERROR, "id": device_id}
                yield res
                continue

            # Get device old config
            cfg_old = self.__s3_get_obj_string(device["id"] + '/' + self.__fw_old["cfg_name"])

            # Parse json
            cfg_old_obj = json.loads(cfg_old, object_pairs_hook=OrderedDict)
            cfg_new_obj = json.loads(self.__fw_new["cfg"], object_pairs_hook=OrderedDict)

            # Create config object
            tools = CANedgeConfig(device_public_key_base64=device["kpub"])

            # Invoke the users migration call-back function
            cfg_updated = cfg_cb(tools, index, device_id, cfg_old_obj, cfg_new_obj)

            # Validate the new configuration against the new schema
            schema_new = json.loads(self.__fw_new["sch"])
            try:
                msg = validate(instance=cfg_updated, schema=schema_new)
            except ValidationError as e:
                res["res"] = CANedgeReturnCodes.CONFIG_VALIDATION_ERROR
                res["msg"] = e.message
                yield res
                continue
            except Exception as e:
                res["res"] = CANedgeReturnCodes.CONFIG_VALIDATION_ERROR
                yield res
                continue

            # Push the new config
            if config_name is None:
                # If a config name is not provided, use the default name of the new fw config
                config_name = self.__fw_new["cfg_name"]
            self.__s3_put_obj_string(device["id"] + '/' + config_name, json.dumps(cfg_updated, indent=2))

            yield res

    # Clean unused configs and schemas
    def cfg_clean(self) -> Generator[Dict, None, None]:

        # Loop devices
        for device in self.devices:

            res = {"res": CANedgeReturnCodes.OK, "id": device["id"], "removed": []}

            for obj in self.mc.list_objects_v2(self.bucket, prefix=device["id"] + '/', recursive=False):

                # Config
                r = re.search(r'^[A-F0-9]{8}/(config-\d{2}\.\d{2}\.json)$', obj.object_name)
                if r:
                    if (r[1] != self.__fw_old["cfg_name"]) and (r[1] != self.__fw_new["cfg_name"]):
                        self.mc.remove_object(self.bucket, obj.object_name)
                        res["removed"].append(r[1])

                # Schema
                r = re.search(r'^[A-F0-9]{8}/(schema-\d{2}\.\d{2}\.json)$', obj.object_name)
                if r:
                    if (r[1] != self.__fw_old["sch_name"]) and (r[1] != self.__fw_new["sch_name"]):
                        self.mc.remove_object(self.bucket, obj.object_name)
                        res["removed"].append(r[1])

            yield res

    # Update firmware
    def fw_update(self, device_ids_to_update: [str]) -> Generator[Dict, None, None]:

        # Loop devices
        for device_id in device_ids_to_update:

            res = {"res": CANedgeReturnCodes.OK, "id": device_id}

            # Check if device id is in list of known devices
            device = self.__find_device_by_id(device_id)
            if device is None:
                res = {"res": CANedgeReturnCodes.UNKNOWN_DEVICE_ID_ERROR, "id": device_id}
                yield res
                continue

            # Check that a fw update is needed
            if device["fw_ver"] == self.__fw_new["fw_ver"]:
                yield res
                continue

            # Check that a valid configuration file is present
            try:
                self.mc.stat_object(self.bucket, device["id"] + '/' + self.__fw_new["cfg_name"])
            except Exception as e:
                res["res"] = CANedgeReturnCodes.CONFIG_NOT_FOUND_ERROR
                yield res
                continue

            # Put firmware
            self.mc.fput_object(self.bucket, device["id"] + '/firmware.bin', self.fw_new_path)

            yield res
