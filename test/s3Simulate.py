import json
import random

from test.s3Client import S3Client


class S3Simulate(object):

    def __init__(self, s3_client: S3Client, bucket_name):
        self._s3_client = s3_client
        self._bucket_name = bucket_name
        pass

    def populate(self, schema_name: str, config_name: str, config_path, devices_nof=10):

        # Push simulated devices on S3
        for i in range(0, devices_nof):
            device_id = "{:08X}".format(random.randrange(1 << 32))

            # Create and push a device.json file
            device_obj_name = device_id + '/device.json'
            device_obj = json.dumps({"id": device_id, "sch_name": schema_name, "kpub": ""})
            self._s3_client.put_object_string(self._bucket_name, device_obj_name, device_obj)

            # Push the config file
            config_obj_name = device_id + '/' + config_name
            self._s3_client.fput_object(self._bucket_name, config_obj_name, config_path)
        pass

