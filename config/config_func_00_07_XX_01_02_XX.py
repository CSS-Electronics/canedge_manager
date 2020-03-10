import json


def migrate_filter_list(filter_list):

    # Migrate filter prescaler.
    # Old structure:
    # - "prescaler": count prescaler value
    # New structure
    # - "prescaler_type": prescaler type, none, value, time or data
    # - "prescaler_value": prescaler value

    # Loop each filter element and migrate the presclaer if set
    for i, filter_elm in enumerate(filter_list):
        if "prescaler" not in filter_elm:
            # Prescaler not set, set to prescaler type None (0)
            filter_list[i]["prescaler_type"] = 0
        else:
            # Prescaler set, migrate the count value
            if filter_elm["prescaler"] == 0 or filter_elm["prescaler"] == 1:
                # Prescaler is set but not used (value is 0 or 1)
                filter_list[i]["prescaler_type"] = 0
            else:
                # Prescaler is set and used. Set to "count" type and reuse the prescaler value
                filter_list[i]["prescaler_type"] = 1
                filter_list[i]["prescaler_value"] = filter_elm["prescaler"]

            del filter_elm["prescaler"]

    return filter_list

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

    # Firmware 00.07.XX to 01.02.XX configuration migration.

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

    # Changes to prescaling in CAN section. Migrate from old to new structure
    config_new["can_1"] = config_old["can_1"]
    if "filter" in config_new["can_1"]:
        config_new["can_1"]["filter"] = migrate_filter_list(config_new["can_1"]["filter"])
        pass

    config_new["can_2"] = config_old["can_2"]
    if "filter" in config_new["can_2"]:
        config_new["can_2"]["filter"] = migrate_filter_list(config_new["can_2"]["filter"])
        pass

    # No changes to LIN sections
    config_new["lin_1"] = config_old["lin_1"]
    config_new["lin_2"] = config_old["lin_2"]

    # New field in CONNECT section (only CANedge2)
    if "connect" in config_old:
        config_new["connect"] = config_old["connect"]
        if "s3" in config_new["connect"]:
            if "server" in config_new["connect"]["s3"]:
                if "server" in config_new["connect"]["s3"]:
                    if "endpoint" in config_new["connect"]["s3"]["server"]:
                        if "signed_payload" not in config_new["connect"]["s3"]["server"]:
                            # Default SIGNED PAYLOAD to disabled
                            config_new["connect"]["s3"]["server"]["signed_payload"] = 0

    return config_new
