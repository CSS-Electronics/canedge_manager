def config_func(tools, index, device_type, device_id, config_old: {}, config_new: {}):
    """
    CANedge configuration update function
    :param tools: A collection of tools used for device configuration
    :param index: Consecutive device index (from 0)
    :param device_id: Device ID
    :param config_old: The current device configuration
    :param config_new: Default new device configuration
    :return: Update configuration
    """

    # This is an example of a firmware upgrade requiring a configuration migration

    # Firmware 01.04.XX to 01.06.XX configuration migration.

    # GENERAL section, no changes
    config_new["general"] = config_old["general"]

    # LOG section, support for error frames added
    config_new["log"] = config_old["log"]

    # Set error frame logging state
    config_new["log"]["error_frames"] = {"state": 0}

    # RTC section, no changes
    config_new["rtc"] = config_old["rtc"]

    # SECONDARY PORT section, no changes
    config_new['secondaryport'] = config_old['secondaryport']

    # CAN sections, no changes
    for can_x in ["can_1", "can_2"]:
        config_new[can_x] = config_old[can_x]

    # LIN sections, no changes
    for lin_x in ["lin_1", "lin_2"]:
        config_new[lin_x] = config_old[lin_x]

    # CONNECT section, no changes
    if "connect" in config_old:
        config_new["connect"] = config_old["connect"]

    return config_new
