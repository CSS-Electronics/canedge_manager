def config_func(config_old, config_new):
    """
    CANedge configuration update function
    :param config_old: The current device configuration
    :param config_new: Default new device configuration
    :return: Update configuration
    """

    # This is an example of a firmware upgrade requiring a configuration migration
      
    # Firmware 00.05.XX to 00.06.XX configuration migration.
    # NOTE: This example assumes that the advanced bit-rate (bit-timing) setting is not used

    config_new = config_old

    # Firmware 00.06 defaults the CAN-bus retransmission setting to enabled. This can optionally be set during upgrade.
    config_new["can_1"]["phy"]["retransmission"] = 1
    config_new["can_2"]["phy"]["retransmission"] = 1

    return config_new