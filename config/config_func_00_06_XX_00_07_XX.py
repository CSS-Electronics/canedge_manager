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

    # Firmware 00.06.XX to 00.07.XX configuration migration.

    # No changes to GENERAL section
    config_new["general"] = config_old["general"]

    # No changes to LOG section
    config_new["log"] = config_old["log"]

    # No changes to RTC section
    config_new["rtc"] = config_old["rtc"]

    # No changes to CONNECT section
    if "connect" in config_old:
        config_new["connect"] = config_old["connect"]

    # Secondary port power state changed to power schedule
    if "power" in config_old["secondaryport"]:
        if config_old["secondaryport"]["power"] == 0:
            # Set power schedule to empty list (always off)
            config_new['secondaryport'] = {"power_schedule": []}
        else:
            # Add one element to power schedule list. From 00:00 to 00:00 (always on)
            config_new['secondaryport'] = {"power_schedule": [{"from": "00:00", "to": "00:00"}]}

    # New GENERAL, HEARTBEAT and CONTROL sections added to CAN. Set default values
    # CAN 1 
    config_new["can_1"] = config_old["can_1"]
    # CAN 1->General
    config_new["can_1"]["general"] = {'rx_state': 1, 'tx_state': 1}
    # CAN 1->Heartbeat
    config_new["can_1"]["heartbeat"] = {'state': 0, 'id_format': 1, 'id': '00435353'}
    # CAN 1->Control
    config_new["can_1"]["control"] = {'control_rx_state': 0,
                                      'control_tx_state': 0,
                                      "start": {
                                          "id_format": 1,
                                          "id": "00435354",
                                          "id_mask": "1FFFFFFF",
                                          "data_mask": "FFFFFFFFFFFFFFFF",
                                          "data_high": "0100000000000000",
                                          "data_low": "0100000000000000"},
                                      "stop": {
                                          "id_format": 1,
                                          "id": "00435354",
                                          "id_mask": "1FFFFFFF",
                                          "data_mask": "FFFFFFFFFFFFFFFF",
                                          "data_high": "0000000000000000",
                                          "data_low": "0000000000000000"}
                                      }

    # CAN 2
    config_new["can_2"] = config_old["can_2"]
    # CAN 1->General
    config_new["can_2"]["general"] = config_new["can_1"]["general"]
    # CAN 1->Heartbeat
    config_new["can_2"]["heartbeat"] = config_new["can_1"]["heartbeat"]
    # CAN 1->Control
    config_new["can_2"]["control"] = config_new["can_1"]["control"]
    
    # New LIN sections added. Set default values
    config_new["lin_1"] = {'phy': {'mode': 0, 'bit_rate': 19200}}
    config_new["lin_2"] = {'phy': {'mode': 0, 'bit_rate': 19200}}

    return config_new
