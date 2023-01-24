import pytest
from test.test_config_migrate import TestMigrate

class Test_01_07(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default (NOTE, CAN internal extended id filter changed from "id_format": 0 to "id_format": 1)
            (
                "../fw/ce1-01.06.02.zip",
                "../fw/ce1-01.07.01.zip",
                "ce1_01.06_1.json",
                "ce1_01.07_1.json",
                "config.config_func_01_06_XX_01_07_XX"
            ),
            # CANedge 2
            # Default to default (NOTE, CAN internal extended id filter changed from "id_format": 0 to "id_format": 1)
            (
                "../fw/ce2-01.06.02.zip",
                "../fw/ce2-01.07.01.zip",
                "ce2_01.06_1.json",
                "ce2_01.07_1.json",
                "config.config_func_01_06_XX_01_07_XX"
            ),
            # CANedge 2
            # Five wifi APs reduced to four
            (
                "../fw/ce2-01.06.02.zip",
                "../fw/ce2-01.07.01.zip",
                "ce2_01.06_2.json",
                "ce2_01.07_2.json",
                "config.config_func_01_06_XX_01_07_XX"
            ),
            # CANedge 2
            # With non-default CAN filters. Should migrate filters (not apply the new default)
            (
                "../fw/ce2-01.06.02.zip",
                "../fw/ce2-01.07.01.zip",
                "ce2_01.06_3.json",
                "ce2_01.07_3.json",
                "config.config_func_01_06_XX_01_07_XX"
            ),
        ])
    def test_cfg(self, s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
