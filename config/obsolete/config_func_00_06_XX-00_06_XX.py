def config_func(config_old, config_new):
    """
    CANedge configuration update function
    :param config_old: The current device configuration
    :param config_new: Default new device configuration
    :return: Update configuration
    """

    # This is an example of a simple configuration update (without firmware upgrade)

    # Firmware 00.06.XX to 00.06.XX configuration update

    # New configuration uses same structure. The old configuration can safely be copied to the new.
    config_new = config_old
    
    # Optionally update specific fields
    config_new["general"]["device"]["meta"] = "New device name"    

    return config_new