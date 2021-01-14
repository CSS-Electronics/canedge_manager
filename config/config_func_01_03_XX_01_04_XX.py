def config_func(tools, index, device_id, config_old: {}, config_new: {}):
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

    # Firmware 01.03.XX to 01.04.XX configuration migration.

    # GENERAL section, no changes
    config_new["general"] = config_old["general"]

    # LOG section, error_frames added
    config_new["log"] = config_old["log"]
    config_new["log"]["error_frames"] = {"state": 0}
    
    # RTC section, no changes
    config_new["rtc"] = config_old["rtc"]

    # SECONDARY PORT section, no changes
    config_new['secondaryport'] = config_old['secondaryport']

    # CAN sections, remote_frames added, filter moved
    for can_x in ["can_1", "can_2"]:
        config_new[can_x] = config_old[can_x]
        config_new[can_x]["filter"] = {"remote_frames": 0, "id": config_old[can_x]["filter"]}

    # LIN sections, before optional, now mandatory
    for lin_x in ["lin_1", "lin_2"]:
        if lin_x in config_old:
            config_new[lin_x] = config_old[lin_x]

    # CONNECT section, server->request_style now mandatory
    if "connect" in config_old:
        config_new["connect"] = config_old["connect"]

        # Add mandatory "request_style" if not already set
        if "s3" in config_new["connect"]:
            if "server" in config_new["connect"]["s3"]:
                if "request_style" not in config_new["connect"]["s3"]["server"]:
                    config_new["connect"]["s3"]["server"]["request_style"] = 0

    return config_new
