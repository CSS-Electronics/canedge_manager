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

    # This is an example of a firmware upgrade requiring a configuration migration.

    # Firmware 01.07.XX to 01.08.XX configuration migration.

    # Add the new debug->restart timer. Take the default value from the new default config
    config_old["general"]["debug"] = config_new["general"]["debug"]

    # For CE1G, CE2G and CE3G, add the new GNSS distance message (introduced in 01.07.03) if missing
    if device_type in [CANedgeType.CANEDGE1G, CANedgeType.CANEDGE2G, CANedgeType.CANEDGE3G]:

        # Get current and new internal filter lists
        old_can_internal_filters = config_old.get("can_internal", {}).get("filter", {}).get("id", [])
        new_can_internal_filters = config_new.get("can_internal", {}).get("filter", {}).get("id", [])

        # Find "GnssDistance" in both lists
        old_gnss_distance = next((x for x in old_can_internal_filters if x.get("name", "") == "GnssDistance"), None)
        new_gnss_distance = next((x for x in new_can_internal_filters if x.get("name", "") == "GnssDistance"), None)

        # If GnssDistance not in old list, add
        if old_gnss_distance is None and new_gnss_distance is not None:
            old_can_internal_filters.insert(5, new_gnss_distance)

    # For CE1, CE2, CE3, fix minor error in 01.07 default config
    if device_type in [CANedgeType.CANEDGE1, CANedgeType.CANEDGE2, CANedgeType.CANEDGE3]:

        # Get current filter list
        old_can_internal_filters = config_old.get("can_internal", {}).get("filter", {}).get("id", [])

        # If filter "AllExtendedID" exists, ensure the "id_format" is indeed set to "extended" (1)
        old_all_extended = next((x for x in old_can_internal_filters if x.get("name", "") == "AllExtendedID"), None)
        if isinstance(old_all_extended, dict) and "id_format" in old_all_extended:
            old_all_extended["id_format"] = 1

    # # For CE2, CE2G, CE3, CE3G, add new connect->protocol (protocol = 0 is S3)
    if device_type in [CANedgeType.CANEDGE2, CANedgeType.CANEDGE2G, CANedgeType.CANEDGE3, CANedgeType.CANEDGE3G]:
        connect = config_old.get("connect", None)
        if isinstance(connect, OrderedDict):
            connect["protocol"] = 0
            connect.move_to_end("s3")

    # If present, remove temporary secondaryport->power_cycle field
    if config_old.get("secondaryport", {}).get("power_cycle", None) is not None:
        del config_old["secondaryport"]["power_cycle"]

    # Return updated config
    return config_old