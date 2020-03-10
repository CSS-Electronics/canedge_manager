import pytest
from test.test_config_migrate import TestMigrate


class Test_00_07(TestMigrate):

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
        self.main(s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
