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

    # This is an example of a simple configuration update (without firmware upgrade)

    # Firmware 00.07.XX to 00.07.XX configuration update

    # New configuration uses same structure. The old configuration can safely be copied to the new.
    config_new = config_old

    # Optionally update specific fields
    config_new["general"]["device"]["meta"] = "FW07.01"
    
    return config_new