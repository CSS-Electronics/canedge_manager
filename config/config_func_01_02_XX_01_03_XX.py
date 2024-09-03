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

    # Firmware 01.02.XX to 01.03.XX configuration migration.

    # No changes to GENERAL section
    config_new["general"] = config_old["general"]

    # No changes to LOG section
    config_new["log"] = config_old["log"]
    
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

    # New field in CONNECT section (connect->s3->server->request_style) (only CANedge2)
    if "connect" in config_old:
        # Copy CONNECT section
        config_new["connect"] = config_old["connect"]

        # If a S3 server endpoint is set, add request_style (default to path_style)
        if "s3" in config_new["connect"]:
            if "server" in config_new["connect"]["s3"]:
                if "endpoint" in config_new["connect"]["s3"]["server"]:
                    if "request_style" not in config_new["connect"]["s3"]["server"]:
                        config_new["connect"]["s3"]["server"]["request_style"] = 0

    return config_new
