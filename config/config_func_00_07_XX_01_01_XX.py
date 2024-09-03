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

    # Firmware 00.07.XX to 01.01.XX configuration migration.

    # No changes to GENERAL section
    config_new["general"] = config_old["general"]

    # New structure in LOG section
    # The fields previously in LOG moved to LOG->FILE
    config_new["log"]["file"] = config_old["log"]
    if "compression" not in config_new["log"]:
        config_new["log"]["compression"] = {"level": 0}
    if "encryption" not in config_new["log"]:
        config_new["log"]["encryption"] = {"state": 0}

    # No changes to RTC section
    config_new["rtc"] = config_old["rtc"]

    # No changes to SECONDARY PORT section
    config_new['secondaryport'] = config_old['secondaryport']

    # No changes to CAN sections
    config_new["can_1"] = config_old["can_1"]
    config_new["can_2"] = config_old["can_2"]

    # No changes to LIN sections
    config_new["lin_1"] = config_old["lin_1"]
    config_new["lin_2"] = config_old["lin_2"]

    # New field in CONNECT section (only CANedge2)
    if "connect" in config_old:
        config_new["connect"] = config_old["connect"]
        if "s3" in config_new["connect"]:
            if "server" in config_new["connect"]["s3"]:
                if "endpoint" in config_new["connect"]["s3"]["server"]:
                    if "signed_payload" not in config_new["connect"]["s3"]["server"]:
                        # Default SIGNED PAYLOAD to disabled
                        config_new["connect"]["s3"]["server"]["signed_payload"] = 0

    return config_new
