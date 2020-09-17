import pytest
from test.test_config_migrate import TestMigrate


class Test_01_03(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (
                "../fw/ce1-01.02.05.zip",
                "../fw/ce1-01.03.01.zip",
                "ce1_01.02_1.json",
                "ce1_01.03_1.json",
                "config.config_func_01_02_XX_01_03_XX"
            ),
            # CANedge 2
            # Default to default
            (
                "../fw/ce2-01.02.05.zip",
                "../fw/ce2-01.03.01.zip",
                "ce2_01.02_1.json",
                "ce2_01.03_1.json",
                "config.config_func_01_02_XX_01_03_XX"
            ),
            # Set request_style
            (
                    "../fw/ce2-01.02.05.zip",
                    "../fw/ce2-01.03.01.zip",
                    "ce2_01.02_2.json",
                    "ce2_01.03_2.json",
                    "config.config_func_01_02_XX_01_03_XX"
            ),

        ])
    def test_cfg(self, s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
