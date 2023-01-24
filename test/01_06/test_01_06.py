import pytest
from test.test_config_migrate import TestMigrate

class Test_01_06(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (
                "../fw/ce1-01.04.01.zip",
                "../fw/ce1-01.06.02.zip",
                "ce1_01.04_1.json",
                "ce1_01.06_1.json",
                "config.config_func_01_04_XX_01_06_XX"
            ),
            # CANedge 2
            # Default to default
            (
                "../fw/ce2-01.04.01.zip",
                "../fw/ce2-01.06.02.zip",
                "ce2_01.04_1.json",
                "ce2_01.06_1.json",
                "config.config_func_01_04_XX_01_06_XX"
            ),
        ])
    def test_cfg(self, s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
