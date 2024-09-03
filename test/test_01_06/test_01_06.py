import pytest
from canedge_manager import CANedgeType
from test.test_migrate import TestMigrate

class Test_01_06(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-01.04.01.zip",
                "fw/ce1-01.06.02.zip",
                "test_01_06/ce1_01.04_1.json",
                "test_01_06/ce1_01.06_1.json",
                "config.config_func_01_04_XX_01_06_XX"
            ),
            # CANedge 2
            # Default to default
            (
                CANedgeType.CANEDGE2,
                "fw/ce2-01.04.01.zip",
                "fw/ce2-01.06.02.zip",
                "test_01_06/ce2_01.04_1.json",
                "test_01_06/ce2_01.06_1.json",
                "config.config_func_01_04_XX_01_06_XX"
            ),
        ])
    def test_cfg(self, s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
