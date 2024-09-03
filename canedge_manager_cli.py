import argparse
import importlib
import json
import os
import re
from cmd import Cmd
from minio import Minio
from canedge_manager import CANedge, CANedgeReturnCodes

class CANedgeCli(Cmd):

    intro = ""
    prompt = "(CANedge)"

    def __init__(self, args):
        super(CANedgeCli, self).__init__()

        # Load the configuration call-back function
        cfgfunc_name, cfgfunc_ext = os.path.splitext(args["cfgfunc"])
        try:
            cfgfunc_name_import = cfgfunc_name
            cfgfunc_name_import = cfgfunc_name_import.replace("\\", ".")
            cfgfunc_name_import = cfgfunc_name_import.replace("/", ".")
            config_func = importlib.import_module(cfgfunc_name_import)
        except Exception:
            raise Exception("Could not load configuration function")
        self.cfgfunc = config_func.config_func

        # Load server configuration file
        try:
            with open(args["server"], mode='r') as file:
                server_cfgs = json.load(file)
        except Exception:
            raise Exception("Server configuration file not found")

        # If minio config, load hosts
        if 'version' in server_cfgs.keys():
          if server_cfgs["version"] == "9" and 'hosts' in server_cfgs.keys():
            server_cfgs = server_cfgs["hosts"]

        # If alias not provided, default to first in list
        if args["alias"] is None:
            args["alias"] = list(server_cfgs.keys())[0]

        # Get fetch the server config by alias
        if args["alias"] not in server_cfgs:
            raise Exception("Server alias not found")
        server_cfg = server_cfgs[args["alias"]]

        # Init S3 client
        tls = True if server_cfg["url"].find("https") >= 0 else False

        # Strip http / https from url
        server_url = server_cfg["url"]
        server_url = server_url.replace("https://", "")
        server_url = server_url.replace("http://", "")

        mc = Minio(endpoint=server_url,
                   access_key=server_cfg["accessKey"],
                   secret_key=server_cfg["secretKey"],
                   secure=tls)

        # Init CANedge
        self.ce = CANedge(mc=mc, bucket=args["bucket"], fw_old_path=args["fwcur"], fw_new_path=args["fwnew"])

        # Info text
        self.intro += f"CANedge manager CLI using CANedge manager API version: {self.ce.tool_version}\n"
        self.intro += f"- S3 client connected to: {server_cfg['url']}/{args['bucket']}\n"
        if args["fwnew"] is None:
            self.intro += f"- Firmware {self.ce.fw}\n"
        else:
            self.intro += f"Firmware: {self.ce.fw}->{self.ce.fw_migration}\n"
        self.intro += f"- Configuration function: {cfgfunc_name}\n"
        self.intro += "Type \"exit\" to exit\n"
        self.intro += "Type \"help\" for list of commands"

    def _parse_id_selection(self, inp):
        devices = []
        if inp[0:2] == "-a":
            devices = self.ce.device_ids
        elif inp[0:2] == "-l":
            devices = re.findall(r"([A-F0-9]{8})", inp.upper())
        elif inp[0:2] == "-r":
            id_range = re.search(r"(\d+)-(\d+)", inp)
            if id_range:
                if len(id_range.groups()) == 2:
                    start = int(id_range.groups()[0])
                    end = int(id_range.groups()[1])
                    if len(self.ce.device_ids) > end and start >= 0:
                        devices = self.ce.device_ids[start:end+1]

        return devices

    @staticmethod
    def _parse_id_selection_help(cmd_name):
        print("{} -a: all".format(cmd_name))
        print("{} -l: list (-l AABBCCDD 00112233)".format(cmd_name))
        print("{} -r: range (-r 0-3)".format(cmd_name))

    def do_ls(self, inp):
        for i, device in enumerate(self.ce.devices):
            print("{: 4d}, ID: {}, FW: {}, HW: {}, CFG_CRC: {}"
                  .format(i, device["id"], device["fw_ver"], device["hw_ver"], device["cfg_crc32"]))

    def help_ls(self):
        print("List devices on server with matching firmware version")

    def do_config(self, inp):

        devices = self._parse_id_selection(inp)
        if len(devices) == 0:
            self.help_config()
            return

        # Is dry run?
        config_name = None
        matches_dry = re.search(r"--dry", inp)
        if matches_dry:
            config_name = "config-XX.XX.json"

        for result in self.ce.cfg_update(device_ids_to_update=devices, cfg_cb=self.cfgfunc, config_name=config_name):
            if result["res"] is CANedgeReturnCodes.OK:
                print("- {} | Config updated".format(result["id"]))
            elif result["res"] is CANedgeReturnCodes.CONFIG_VALIDATION_ERROR:
                print("- {}: Config update skipped. Error message: {}".format(result["id"], result["msg"]))
            elif result["res"] is CANedgeReturnCodes.UNKNOWN_DEVICE_ID_ERROR:
                print("- {}: Unknown device ID".format(result["id"]))
            else:
                print("- Unknown error, aborting")
                break

    def help_config(self):
        self._parse_id_selection_help("config")
        print("config -[a|l|r] --dry: Dry run creating dummy config \"config-XX.XX.json\"")

    def do_update(self, inp):

        devices = self._parse_id_selection(inp)
        if len(devices) == 0:
            self.help_update()
            return

        for result in self.ce.fw_update(devices):
            if result["res"] is CANedgeReturnCodes.OK:
                print("- {} | FW updated".format(result["id"]))
            elif result["res"] is CANedgeReturnCodes.UNKNOWN_DEVICE_ID_ERROR:
                print("- {}: Unknown device ID".format(result["id"]))
            elif result["res"] is CANedgeReturnCodes.CONFIG_NOT_FOUND_ERROR:
                print("- {}: Compatible configuration file not found".format(result["id"]))
            else:
                print("- Update error, aborting ({})".format(result))
                break

    def help_update(self):
        self._parse_id_selection_help("update")

    def do_clean(self, inp):
        for result in self.ce.cfg_clean():
            if len(result["removed"]) > 0:
                print("- {} | Removed: {}".format(result["id"], ", ".join(result["removed"])))

    def help_clean(self):
        print("Cleans unused config and schema files")

    def do_exit(self, inp):
        exit()

    def help_exit(self):
        print("Exit")

if __name__ == '__main__':

    # Parse input arguments
    parser = argparse.ArgumentParser(description='CANedge Command Line Interface',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--server', type=str, required=False, help='A json file containing a list S3 server details (if omitted, servers.json is used)', default='servers.json')
    parser.add_argument('-a', '--alias', type=str, required=False, help='The alias of the relevant server from server to use (if omitted, the 1st entry is used)', default=None)
    parser.add_argument('-b', '--bucket', type=str, required=True, help='S3 bucket name')
    parser.add_argument('-f', '--cfgfunc', required=True, type=str, help='A user-provided configuration function applied during the configuration update')
    parser.add_argument('-c', '--fwcur', required=True, type=str, help='The Firmware file currently used on the devices to be updates (*.bin)')
    parser.add_argument('-n', '--fwnew', required=False, type=str, help='The Firmware file to be migrated to (*.bin)')
    args = parser.parse_args()

    # Start CLI
    cli = CANedgeCli(vars(args))
    cli.cmdloop(intro=cli.intro)
    pass
