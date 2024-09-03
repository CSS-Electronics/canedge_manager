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

    # Firmware 01.06.XX to 01.07.XX configuration migration.

    # GENERAL section, no changes
    config_new["general"] = config_old["general"]

    # LOG section
    config_new["log"] = config_old["log"]

    # Set error frame logging state
    config_new["log"]["error_frames"] = {"state": 0}

    # RTC section
    config_new["rtc"] = config_old["rtc"]

    # "ntp_fallback" field obsolete, remove
    if "ntp_fallback" in config_new["rtc"]:
        del config_new["rtc"]["ntp_fallback"]

    # SECONDARY PORT section, no changes
    config_new['secondaryport'] = config_old['secondaryport']

    # CAN "internal-channel" section added. Populate with default values
    config_new["can_internal"] = {
        "general": {"rx_state": 1, "tx_state": 1},
        "filter": {"id": can_filter_id_new_default()},
        "control": control_signal_new_default(channel=0)
    }

    # Physical CAN sections
    for i, can_x in enumerate(["can_1", "can_2"]):
        config_new[can_x] = config_old[can_x]

        # Control signal concept fundamentally changed. Not possible to migrate automatically
        config_new[can_x]["control"] = control_signal_new_default(channel=i+1)

        # The default "allow all" filters changed from using mask to range
        # Only migrate if default filters used in "old" config
        if len(config_new[can_x]["filter"]["id"]) == 2:
            if config_new[can_x]["filter"]["id"][0]["name"] == f"Ch{i+1}AllStandard" and \
               config_new[can_x]["filter"]["id"][1]["name"] == f"Ch{i+1}AllExtended":
                config_new[can_x]["filter"]["id"] = can_filter_id_new_default()

    # LIN sections, no changes
    for lin_x in ["lin_1", "lin_2"]:
        config_new[lin_x] = config_old[lin_x]

    # CONNECT section
    if "connect" in config_old:
        config_new["connect"] = config_old["connect"]

        # Number of allowed APs reduced from 5 to 4
        if "wifi" in config_new["connect"]:
            if "accesspoint" in config_new["connect"]["wifi"]:

                # If 5 APs defined, reduce to 4
                if len(config_new["connect"]["wifi"]["accesspoint"]) == 5:
                    config_new["connect"]["wifi"]["accesspoint"].pop()

    return config_new


def can_filter_id_new_default() -> list:
    filter_id = [
        {
            "name": "AllStandardID",
            "state": 1,
            "type": 0,
            "id_format": 0,
            "method": 0,
            "f1": "0",
            "f2": "7FF",
            "prescaler_type": 0
        },
        {
            "name": "AllExtendedID",
            "state": 1,
            "type": 0,
            "id_format": 1,
            "method": 0,
            "f1": "0",
            "f2": "1FFFFFFF",
            "prescaler_type": 0
        }
    ]
    return filter_id


def control_signal_new_default(channel: int) -> dict:
    control_signal = {
        "control_rx_state": 0,
        "control_tx_state": 0,
        "start": {
            "message": {
                "chn": int(channel),
                "id_format": 0,
                "id": "0",
                "id_mask": "7FF"
            },
            "signal": {
                "type": 0,
                "byteorder": 0,
                "bitpos": 0,
                "length": 0,
                "factor": 0,
                "offset": 0
            },
            "trigger_high": 0,
            "trigger_low": 0
        },
        "stop": {
            "message": {
                "chn": int(channel),
                "id_format": 0,
                "id": "0",
                "id_mask": "7FF"
            },
            "signal": {
                "type": 0,
                "byteorder": 0,
                "bitpos": 0,
                "length": 0,
                "factor": 0,
                "offset": 0
            },
            "trigger_high": 0,
            "trigger_low": 0
        }
    }
    return control_signal
