import pytest
from canedge_manager import CANedgeType
from test.test_migrate import TestMigrate


class Test_01_02(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-00.07.05.zip",
                "fw/ce1-01.02.05.zip",
                "test_01_02/ce1_00.07_1.json",
                "test_01_02/ce1_01.02_1.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # Non-default values in log section (which is moved to log-file)
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-00.07.05.zip",
                "fw/ce1-01.02.05.zip",
                "test_01_02/ce1_00.07_2.json",
                "test_01_02/ce1_01.02_2.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # Migrate filter with prescaling
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-00.07.05.zip",
                "fw/ce1-01.02.05.zip",
                "test_01_02/ce1_00.07_3.json",
                "test_01_02/ce1_01.02_3.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # CANedge 2
            # Default to default
            (
                CANedgeType.CANEDGE2,
                "fw/ce2-00.07.05.zip",
                "fw/ce2-01.02.05.zip",
                "test_01_02/ce2_00.07_1.json",
                "test_01_02/ce2_01.02_1.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
            # With Wifi and S3 server. Expects that the signed_payload is set to 0 if endpoint is present
            (
                CANedgeType.CANEDGE2,
                "fw/ce2-00.07.05.zip",
                "fw/ce2-01.02.05.zip",
                "test_01_02/ce2_00.07_2.json",
                "test_01_02/ce2_01.02_2.json",
                "config.config_func_00_07_XX_01_02_XX"
            ),
        ])
    def test_cfg(self, s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
