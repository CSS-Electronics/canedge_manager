# Changelog CANedge module
All notable changes to this project will be documented in this file.

## [00.00.02] - 2019-10-02
### Added

### Changed
- Configuration function prototype changed. Now takes additional arguments "tools", "index" and "device_id"
- Configuration tools object now includes helper functions for credential encryption

# Changelog CANedge CLI
All notable changes to this project will be documented in this file.

## [00.00.02] - 2019-10-02
### Added
- Configuration change `config` command now takes `--dry` argument to create test configuration file `config-XX.XX.json`. Eg. `config -r 0-0 --dry`
