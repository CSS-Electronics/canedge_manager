import pytest
import json
import importlib
from os import path
from canedge import CANedge, CANedgeReturnCodes
from test.fwPackage import unpack
from test.s3Simulate import S3Simulate


class Test_00_07:

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            (
                "../fw/ce1-00.06.02.zip",
                "../fw/ce1-00.07.05.zip",
                "ce1_00.06_1.json",
                "ce1_00.07_1.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
            (
                "../fw/ce1-00.06.02.zip",
                "../fw/ce1-00.07.05.zip",
                "ce1_00.06_2.json",
                "ce1_00.07_2.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
            # CANedge 2
            (
                "../fw/ce2-00.06.02.zip",
                "../fw/ce2-00.07.05.zip",
                "ce2_00.06_1.json",
                "ce2_00.07_1.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
            (
                "../fw/ce2-00.06.02.zip",
                "../fw/ce2-00.07.05.zip",
                "ce2_00.06_2.json",
                "ce2_00.07_2.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
        ])
    def test_cfg(self, s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):

        # Import config (migration) function
        cfg_func_module = importlib.import_module(cfg_func_name)
        cfg_func = cfg_func_module.config_func

        # Load expected config after update
        with open(cfg_post) as json_file:
            config_expected = json.load(json_file)

        # Extract fw packs
        fw_pre = unpack(fw_pack_pre, path.join(tmpdir, 'pre'))
        fw_post = unpack(fw_pack_post, path.join(tmpdir, 'post'))

        # Create s3 simulation
        s3_simulate = S3Simulate(s3_client=s3_client, bucket_name=bucket_name)
        s3_simulate.populate(schema_name=fw_pre['schema_name'],
                             config_name=fw_pre['config_name'],
                             config_path=cfg_pre,
                             devices_nof=self._simulated_devices_nof)

        # Create canedge manager
        ce = CANedge(s3_client, bucket_name, fw_pre['firmware_path'], fw_post['firmware_path'])

        # Update configurations
        for result in ce.cfg_update(device_ids_to_update=ce.device_ids, cfg_cb=cfg_func):
            assert result['res'] is CANedgeReturnCodes.OK

        # Get and verify all updated configs
        for device_id in ce.device_ids:
            config_path_tmp = path.join(tmpdir, 'config.json')
            s3_client.fget_object(bucket_name, device_id + '/' + fw_post['config_name'], config_path_tmp)

            # Compare with expected
            with open(config_path_tmp) as json_file:
                assert config_expected == json.load(json_file)
