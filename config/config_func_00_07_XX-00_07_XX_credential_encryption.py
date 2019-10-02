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

    # This is an example of how to upgrade existing access point and S3 credentials from plain to encrypted form. Note
    # that below assumes that the existing configuration holds the information in unencrypted form.
    # Devices already using encrypted credentials are skipped (no configuration returned)

    # New configuration uses same structure. The old configuration can safely be copied to the new.
    config_new = config_old

    # Set device name
    config_new["general"]["device"]["meta"] = "{};{}".format(index, device_id)

    # Only update configurations unencrypted credentials
    if config_new["connect"]["wifi"]["keyformat"] == 0 and config_new["connect"]["s3"]["server"]["keyformat"] == 0:

        # Set the server kpub
        config_new["general"]["security"] = {"kpub": tools.security.user_public_key_base64}

        # Set the access point key format to 1 (encrypted)
        config_new["connect"]["wifi"]["keyformat"] = 1

        # Loop each accesspoint in list
        for ap in config_new["connect"]["wifi"]["accesspoint"]:
            # Encrypt the wifi password
            unencrypted_wifi_pwd = ap["pwd"]
            ap["pwd"] = tools.security.encrypt_encode(unencrypted_wifi_pwd)

        # Encrypt the S3 secret key
        unencrypted_s3_secretkey = config_new["connect"]["s3"]["server"]["secretkey"]
        config_new["connect"]["s3"]["server"]["keyformat"] = 1
        config_new["connect"]["s3"]["server"]["secretkey"] = tools.security.encrypt_encode(unencrypted_s3_secretkey)

    else:
        # This configuration update function only supports upgrade of plain to encrypted passwords.
        # Set new config to None to skip update of config
        config_new = None

    return config_new
