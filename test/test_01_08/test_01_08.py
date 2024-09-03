import pytest
from canedge_manager import CANedgeType
from test.test_migrate import TestMigrate


class Test_01_08(TestMigrate):

    _simulated_devices_nof = 10

    @pytest.mark.parametrize("type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name",
        [
            # CANedge 1
            # Default to default
            (CANedgeType.CANEDGE1,
            "fw/ce1-01.07.01.zip",
            "fw/ce1-01.08.01.zip",
            "test_01_08/ce1-01.07-default.json",
            "test_01_08/ce1-01.08-default.json",
            "config.config_func_01_07_XX_01_08_XX"
            ),
            # CANedge 1 GNSS
            # Default to default
            (CANedgeType.CANEDGE1G,
             "fw/ce1g-01.07.01.zip",
             "fw/ce1g-01.08.01.zip",
             "test_01_08/ce1g-01.07-default.json",
             "test_01_08/ce1g-01.08-default.json",
             "config.config_func_01_07_XX_01_08_XX"
             ),
            # CANedge 2
            # Default to default
            (CANedgeType.CANEDGE2,
             "fw/ce2-01.07.01.zip",
             "fw/ce2-01.08.01.zip",
             "test_01_08/ce2-01.07-default.json",
             "test_01_08/ce2-01.08-default.json",
             "config.config_func_01_07_XX_01_08_XX"
             ),
            # CANedge 2 GNSS
            # Default to default
            (CANedgeType.CANEDGE2G,
             "fw/ce2g-01.07.01.zip",
             "fw/ce2g-01.08.01.zip",
             "test_01_08/ce2g-01.07-default.json",
             "test_01_08/ce2g-01.08-default.json",
             "config.config_func_01_07_XX_01_08_XX"
             ),
            # CANedge 3 GNSS
            # Default to default
            (CANedgeType.CANEDGE3G,
             "fw/ce3g-01.07.07.zip",
             "fw/ce3g-01.08.01.zip",
             "test_01_08/ce3g-01.07-default.json",
             "test_01_08/ce3g-01.08-default.json",
             "config.config_func_01_07_XX_01_08_XX"
             ),
            # CANedge 1
            # Remove temporary secondaryport->power_cycle
            (CANedgeType.CANEDGE1,
             "fw/ce1-01.07.01.zip",
             "fw/ce1-01.08.01.zip",
             "test_01_08/ce1-01.07-secondaryport-powercycle.json",
             "test_01_08/ce1-01.08-secondaryport-powercycle.json",
             "config.config_func_01_07_XX_01_08_XX"
             ),
        ])
    def test_cfg(self, s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir):
        self.main(s3_client, type, fw_pack_pre, fw_pack_post, cfg_pre, cfg_post, cfg_func_name, bucket_name, tmpdir)
