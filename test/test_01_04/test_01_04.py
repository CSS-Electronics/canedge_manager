import pytest
from canedge_manager import CANedgeType
from test.test_migrate import TestMigrate


class Test_01_04(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-01.03.01.zip",
                "fw/ce1-01.04.01.zip",
                "test_01_04/ce1_01.03_1.json",
                "test_01_04/ce1_01.04_1.json",
                "config.config_func_01_03_XX_01_04_XX"
            ),
            # CANedge 1
            # Without lin to mandatory lin
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-01.03.01.zip",
                "fw/ce1-01.04.01.zip",
                "test_01_04/ce1_01.03_2.json",
                "test_01_04/ce1_01.04_2.json",
                "config.config_func_01_03_XX_01_04_XX"
            ),
            # CANedge 2
            # Default to default
            (
                CANedgeType.CANEDGE2,
                "fw/ce2-01.03.01.zip",
                "fw/ce2-01.04.01.zip",
                "test_01_04/ce2_01.03_1.json",
                "test_01_04/ce2_01.04_1.json",
                "config.config_func_01_03_XX_01_04_XX"
            ),
        ])
    def test_cfg(self, s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
