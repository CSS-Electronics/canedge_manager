import pytest
from canedge_manager import CANedgeType
from test.test_migrate import TestMigrate


class Test_00_07(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-00.06.02.zip",
                "fw/ce1-00.07.05.zip",
                "test_00_07/ce1_00.06_1.json",
                "test_00_07/ce1_00.07_1.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
            (
                CANedgeType.CANEDGE1,
                "fw/ce1-00.06.02.zip",
                "fw/ce1-00.07.05.zip",
                "test_00_07/ce1_00.06_2.json",
                "test_00_07/ce1_00.07_2.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
            # CANedge 2
            (
                CANedgeType.CANEDGE2,
                "fw/ce2-00.06.02.zip",
                "fw/ce2-00.07.05.zip",
                "test_00_07/ce2_00.06_1.json",
                "test_00_07/ce2_00.07_1.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
            (
                CANedgeType.CANEDGE2,
                "fw/ce2-00.06.02.zip",
                "fw/ce2-00.07.05.zip",
                "test_00_07/ce2_00.06_2.json",
                "test_00_07/ce2_00.07_2.json",
                "config.config_func_00_06_XX_00_07_XX"
            ),
        ])
    def test_cfg(self, s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
