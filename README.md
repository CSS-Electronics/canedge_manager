# CANedge over-the-air manager (BETA)

This tool lets you manage multiple CANedge devices connected to your S3 server. It supports batch over-the-air firmware/configuration updates. The tool works on a single firmware version and single CANedge variant at a time. It works with any S3 compatible storage (AWS, Google Cloud, MinIO, ...).

Features:
- Update Configuration Files (without updating the Firmware)
- Encrypt device passwords
- Migrate devices to new Firmwares
- Migrate Configuration Files for MINOR/MAJOR updates
- Validates updated configuration files using the device Rule Schema
- Uses a user provided configuration migration function to update/modify configuration files

## Project structure
The project structure is:

- `canedge_manager.py` (main canedge manager module)
- `canedge_manager_cli.py` (canedge manager command line interface)
- `servers.json` (example of S3 server details file)
- `config/` (configuration function examples)

## Installation

Tested with [Python 3.11](https://www.python.org/downloads/).

Requirements: `pip install -r requirements.txt`
    
## Module usage
The CANedge module can be imported and used directly to update device firmware and configuration:

```python

from canedge_manager import CANedge
from minio import Minio
from config_func_00_07_XX_credential_encryption import config_func as config_func

#-------------------------------------
# Add relevant input variables
devices = ["12345678"]
bucket = "your-bucket"
endpoint = "your-endpoint" # e.g. s3.us-east-1.amazonaws.com
access_key = "your-access-key"
secret_key = "your-secret-key"
secure = False
fw_old_path = "path-to-old/firmware.bin"
fw_new_path = "path-to-new/firmware.bin"

#-------------------------------------
# Create client connection to S3 server
mc = Minio(endpoint=endpoint,
           access_key=access_key,
           secret_key=secret_key,
           secure=secure)

# Init a CANedge object
ce = CANedge(mc=mc,
             bucket=bucket,
             fw_old_path=fw_old_path,
             fw_new_path=fw_new_path)

# Update configuration for a list of devices
list(ce.cfg_update(device_ids_to_update=devices, cfg_cb=config_func))

# Update firmware for a list of devices
list(ce.fw_update(device_ids_to_update=devices))

# Cleans unused Configuration and Rule Schema files
list(ce.cfg_clean())


```

## Command Line Interface (CLI) usage

The CLI is a simple front-end to the CANedge manager. The CLI supports batch firmware, configuration and clean-up operations.

Things to note:
- The list of devices is created when the tool is started - to refresh the list, re-start the tool
- When using the CLI, the configuration function needs to be written in Python
- The `config/` directory provides configuration function examples to be used as a starting point
- It is recommended to initially test with one or a few devices before updates are applied to all devices

Typing `python canedge_cli.py --help` provides the following help:
```
usage: canedge_cli.py [-h] [-s SERVER] [-a ALIAS] -b BUCKET -f CFGFUNC -c
                      FWCUR [-n FWNEW]

CANedge Command Line Interface

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        A json file containing a list S3 server details (if
                        omitted, servers.json is used) (default: servers.json)
  -a ALIAS, --alias ALIAS
                        The alias of the relevant server from server to use (if
                        omitted, the 1st entry is used) (default: None)
  -b BUCKET, --bucket BUCKET
                        S3 bucket name (default: None)
  -f CFGFUNC, --cfgfunc CFGFUNC
                        A user-provided configuration function applied during
                        the configuration update (default: None)
  -c FWCUR, --fwcur FWCUR
                        The Firmware file currently used on the devices to be
                        updates (*.bin) (default: None)
  -n FWNEW, --fwnew FWNEW
                        The Firmware file to be migrated to (*.bin) (default:
                        None)
```

Tips:
- If the "-s" argument is omitted, the tool searches for a file named "servers.json"
- If the "-a" argument is omitted, the tool will select the first server alias in server file
- If used for firmware update to a new major / minor version, first run `config` to create a compatible configuration file
- MinIO server configuration files can be used directly (-s argument)

The format of the S3 server file is:
```
{
  "ALIAS": {
    "url": "http://hostname:port",
    "accessKey": "ACCESS_KEY",
    "secretKey": "SECRET_KEY"
  }
}
```
Note that the url (endpoint) shall include *http://* or *https://*.

Running the above will connect you to the server and fetch a list of devices with specified firmware.

Once started, type ´help´ for more information on the available commands:
```
(CANedge)help

Documented commands (type help <topic>):
========================================
clean  config  exit  help  ls  update
```

### Example on starting the CLI tool:
```
python canedge_manager_cli.py -s servers.json -b office -f config/config_func_01_07_XX_01_08_XX.py -c firmware_01_08.01.bin
```
Note: This example assumes you have download the relevant `firmware.bin` and renamed it as above.

### Example on using the CLI tool:
List devices:
```
(CANedge)ls
   0, ID: 071E61AD, FW: 00.07.01, HW: 00.00, CFG_CRC: 2218F2BC
   1, ID: 0DB63A93, FW: 00.07.01, HW: 00.00, CFG_CRC: D8CA618F
   2, ID: 0EEBBC43, FW: 00.07.01, HW: 00.00, CFG_CRC: 3D550818
   3, ID: 12C1A48D, FW: 00.07.01, HW: 00.00, CFG_CRC: 8C4E8370
   4, ID: 26AEB06C, FW: 00.07.01, HW: 00.00, CFG_CRC: F3CC41A8
   5, ID: 2FB30D1C, FW: 00.07.01, HW: 00.00, CFG_CRC: C5FCB62F
   6, ID: 3B912722, FW: 00.07.01, HW: 00.00, CFG_CRC: 4C14CA13
   7, ID: 4B23D6A0, FW: 00.07.01, HW: 00.00, CFG_CRC: 443BECCD
   8, ID: 51697F4D, FW: 00.07.01, HW: 00.00, CFG_CRC: 3E7D99C3
   9, ID: A9110452, FW: 00.07.01, HW: 00.00, CFG_CRC: 3BB5B899
  10, ID: ADC02130, FW: 00.07.01, HW: 00.00, CFG_CRC: 6127A604
  11, ID: C8B4DC35, FW: 00.07.01, HW: 00.00, CFG_CRC: ABD94077
  12, ID: D2920F21, FW: 00.07.01, HW: 00.00, CFG_CRC: E8F96938
  13, ID: E04A72BB, FW: 00.07.01, HW: 00.00, CFG_CRC: DED0F604
  14, ID: F7261DAD, FW: 00.07.01, HW: 00.00, CFG_CRC: 8C4C5238
```

Configuration update devices 0-5:
```
(CANedge)config -r 0-5
- 071E61AD | Config updated
- 0DB63A93 | Config updated
- 0EEBBC43 | Config updated
- 12C1A48D | Config updated
- 26AEB06C | Config updated
- 2FB30D1C | Config updated
```

Configuration update device 6 with --dry argument (an unused configuration file is created):
```
(CANedge)config -r 6-6 --dry
- 3B912722 | Config updated
```

## Certificate
If the server uses TLS (https) and a custom certificate is used, it may be necessary to specifically provide the server root certificate. This can be done by setting the environment variable `SSL_CERT_FILE`.

Example on Windows:
```set SSL_CERT_FILE=C:\Users\bob\Desktop\server_cert.crt```

# Changelog
All notable changes to this project will be documented in this file.

```
CANedge module

## [00.00.03] - 2024-09-03

### Changed
- Manager now only works with one CANEdge type/model at a time
- "device_type" (CANedgeType) input added to configuration functions

## [00.00.02] - 2019-10-02
### Added

### Changed
- Configuration function prototype changed. Now takes additional arguments "tools", "index" and "device_id"
- Configuration tools object now includes helper functions for credential encryption

CANedge CLI

## [00.00.02] - 2019-10-02
### Added
- Configuration change `config` command now takes `--dry` argument to create a test configuration file `config-XX.XX.json`. Eg. `config -r 0-0 --dry`
```
