import pytest
from test.test_config_migrate import TestMigrate


class Test_01_02(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (
                "../fw/ce1-00.07.05.zip",
                "../fw/ce1-01.01.01.zip",
                "ce1_00.07_1.json",
                "ce1_01.02_1.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # Non-default values in log section (which is moved to log-file)
            (
                "../fw/ce1-00.07.05.zip",
                "../fw/ce1-01.01.01.zip",
                "ce1_00.07_2.json",
                "ce1_01.02_2.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # Migrate filter with prescaling
            (
                "../fw/ce1-00.07.05.zip",
                "../fw/ce1-01.01.01.zip",
                "ce1_00.07_3.json",
                "ce1_01.02_3.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # CANedge 2
            # Default to default
            (
                "../fw/ce2-00.07.05.zip",
                "../fw/ce2-01.01.01.zip",
                "ce2_00.07_1.json",
                "ce2_01.02_1.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # With Wifi and S3 server. Expects that the signed_payload is set to 0 if endpoint is present
            (
                "../fw/ce2-00.07.05.zip",
                "../fw/ce2-01.01.01.zip",
                "ce2_00.07_2.json",
                "ce2_01.02_2.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
        ])
    def test_cfg(self, s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)