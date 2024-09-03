import json
import importlib
from os import path
from canedge_manager import CANedge, CANedgeReturnCodes, CANedgeType
from test.firmware import fw_unpack
from test.s3_simulator import S3Simulate


class TestMigrate(object):

    def main(self, s3_client, type: CANedgeType, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):

        # Import config (migration) function
        cfg_func_module = importlib.import_module(cfg_func_name)
        cfg_func = cfg_func_module.config_func

        # Load expected config after update
        with open(cfg_post) as json_file:
            config_expected = json.load(json_file)

        # Extract fw packs
        fw_pre = fw_unpack(fw_pack_pre, path.join(tmpdir, 'pre'))
        fw_post = fw_unpack(fw_pack_post, path.join(tmpdir, 'post'))

        # Create s3 simulation
        s3_simulate = S3Simulate(s3_client=s3_client, bucket_name=bucket_name)
        s3_simulate.populate(type=type,
                             schema_name=fw_pre['schema_name'],
                             config_name=fw_pre['config_name'],
                             config_path=cfg_pre,
                             devices_nof=self._simulated_devices_nof)

        # Create canedge manager
        ce = CANedge(s3_client, bucket_name, fw_pre['firmware_path'], fw_post['firmware_path'])

        assert len(ce.device_ids) == self._simulated_devices_nof, "Unexpected number of devices found"

        # Update configurations
        for result in ce.cfg_update(device_ids_to_update=ce.device_ids, cfg_cb=cfg_func):
            assert result['res'] is CANedgeReturnCodes.OK, result['msg']

        # Get and verify all updated configs
        for device_id in ce.device_ids:
            config_path_tmp = path.join(tmpdir, 'config.json')
            s3_client.fget_object(bucket_name, device_id + '/' + fw_post['config_name'], config_path_tmp)

            # Compare with expected
            with open(config_path_tmp) as json_file:
                assert json.load(json_file) == config_expected, "Unexpected migration"

