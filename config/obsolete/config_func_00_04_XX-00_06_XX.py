def config_func(config_old, config_new):
    """
    CANedge configuration update function
    :param config_old: The current device configuration
    :param config_new: Default new device configuration
    :return: Update configuration
    """

    # This is an example of a firmware upgrade requiring a configuration migration
      
    # Firmware 00.04.XX to 00.06.XX configuration migration.
    # NOTE: This example assumes that the advanced bit-rate (bit-timing) setting is not used
    
    # No changes to LOG section
    config_new["log"] = config_old["log"]
    
    # No changes to RTC section
    config_new["rtc"] = config_old["rtc"]
    
    # No changes to CONNECT section
    config_new["connect"] = config_old["connect"]
    
    # No changes to SECONDARY PORT section
    config_new["secondaryport"] = config_old["secondaryport"]    
    
    # No changes to CAN_X sections
    config_new["can_1"] = config_old["can_1"]    
    config_new["can_2"] = config_old["can_2"]    
    
    # SECURITY and DEBUG sections moved to new GENERAL section    
    # If optional field "kpub" exists, copy to general -> security -> kpub 
    if "security" in config_old and "kpub" in config_old["security"]:
        config_new["general"]["security"]["kpub"] = config_old["security"]["kpub"]
    
    config_new["general"]["debug"]["syslog"] = config_old["debug"]["syslog"]            
        
    # Optionally populate the new device meta field
    config_new["general"]["device"]["meta"] = "Device name"
        
    return config_new