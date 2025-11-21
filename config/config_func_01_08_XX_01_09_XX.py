import copy
from collections import OrderedDict
from canedge_manager import CANedgeType, CANedgeTools

def config_func(tools: CANedgeTools, index: int, device_type: CANedgeType, device_id: str, config_old: OrderedDict, config_new: OrderedDict) -> OrderedDict:
    """
    CANedge configuration update function
    :param tools: A collection of tools used for device configuration
    :param index: Consecutive device index (from 0)
    :param device_type: Device type
    :param device_id: Device ID
    :param config_old: The current device configuration
    :param config_new: The new default device configuration
    :return: Update configuration
    """

    # Firmware 01.08.XX to 01.09.XX configuration migration example
    # Changes from 01.08.XX to 01.09.XX relevant for configuration migration:
    # - The internal signal filters "AllStandardID" and "AllExtendedID" are removed (and replaced by dedicated filters)
    # - New internal signal filters added ("Heartbeat", "TimeCalendar", "TimeExternal")
    # - Dedicated heartbeat-signal removed. Replaced by internal heartbeat-signal.
    #       Internal heartbeat can optionally be routed to physical CAN-bus. Routing is NOT enabled in this example.

    # From can_internal, remove "AllStandardID" and "AllExtendedID" filters (replaced by dedicated signal filters)
    for config_old_internal_signal in config_old["can_internal"]["filter"]["id"][:]:
        if config_old_internal_signal["name"] in ["AllStandardID", "AllExtendedID"]:
            config_old["can_internal"]["filter"]["id"].remove(config_old_internal_signal)

    # Add the new dedicated internal signal filters (taken from the new default config)
    # Create a list of current internal signals (using f1 as a unique identifier)
    config_old_internal_filter_f1s = [x["f1"] for x in config_old["can_internal"]["filter"]["id"]]
    for config_new_internal_filter_ids in config_new["can_internal"]["filter"]["id"]:
        if config_new_internal_filter_ids["f1"] not in config_old_internal_filter_f1s:
            config_old["can_internal"]["filter"]["id"].append(copy.deepcopy(config_new_internal_filter_ids))

    # Sort the internal signal filters by f1
    config_old["can_internal"]["filter"]["id"] = sorted(config_old["can_internal"]["filter"]["id"], key=lambda x: x["f1"])

    # Remove the dedicated heartbeat-signal
    for i, can_x in enumerate(["can_1", "can_2"]):

        if can_x not in config_old:
            continue

        heartbeat_enabled = False
        # Is heartbeat-signal defined?
        if "heartbeat" in config_old[can_x]:

            # Yes, is it enabled?
            if "state" in config_old[can_x]["heartbeat"] and config_old[can_x]["heartbeat"]["state"] == 1:
                # Yes
                heartbeat_enabled = True

            # Remove old heartbeat-signal
            del config_old[can_x]["heartbeat"]

        # If the dedicated heartbeat-signal was enabled, enable the corresponding internal heartbeat signal
        if heartbeat_enabled is True:
            for internal_signal in config_old["can_internal"]["filter"]["id"]:
                if internal_signal["name"] == "Heartbeat":
                    internal_signal["state"] = 1

    # Return updated config
    return config_old