# CANedge CLI

Manage multiple devices connected to S3.

Works on a single firmware version at a time. Can be used to update configurations and firmwares.

Note that the list of devices is created when the tool is started. To refresh the list, re-start the tool.

Run with:

`python canedge_cli.py -s [SERVER_CONFIG].json -a [SERVER_ALIAS] -b [BUCKETNAME] -f [CONFIG_FUNCTION].py -c [FIRMWARE_BINARY].bin`

- Loads a server configuration from a list of server configuration stored as json (compatible with minio server configuration file)
- The user provides a configuration function which is applied during configuration update
- Takes a current firmware file. Session works only with devices matching this firmware
- Takes optionally a new firmware. This can be used to firmware upgrade devices. In this case, the configuration function becomes a migration function - migrating the firmware from the current firmware to the new.

Tips:
- If the "-s" argument is omitted, the tool searches for a file named "servers.json"
- If the "-a" argument is omitted, the tool will select the first server alias in server file
- If used for firmware update to a new major / minor version, first run `config` to create a compatible configuration file.
