def get_devices_with_big_handlers(file) -> list[dict[str, str]]:
    """
    Returns list with devices id and state that have "BIG" handler
    :param: file with logs
    """
    with open(file, "r") as f:
        lines = f.read().splitlines()

    return [
        {"ID": line.split(";")[2], "STATE": line.split(";")[-2]}
        for line in lines if "BIG" in line
    ]


def get_devices_with_invalid_state(list_with_big_handler: list[dict[str, str]]) -> set[str]:
    """
    Returns set with devices that have handler "BIG" and "DD" state
    :param list_with_big_handler: all devices with "BIG" handler that return get_devices_with_big_handlers function
    :return:
    """
    return {line["ID"] for line in list_with_big_handler if line["STATE"] == "DD"}


def get_devices_with_valid_state(
        devices_with_big_handler: list[dict[str, str]],
        failed_devices: set[str]
) -> dict[str, int]:
    """
    Returns dict of devices with "02" status and numbers of statuses
    :param devices_with_big_handler: all devices with "BIG" handler that return get_devices_with_big_handlers function
    :param failed_devices: set of devices with "BIG" handler and "DD" state
    :return:
    """
    valid_devices = [line["ID"] for line in devices_with_big_handler if line["ID"] not in failed_devices]
    valid_devices_id = set(valid_devices)

    return {
        device_id: valid_devices.count(device_id)
        for device_id in valid_devices_id
    }


if __name__ == "__main__":
    all_devices_with_big_handler = get_devices_with_big_handlers("app_2.log")
    failed_devices_id = get_devices_with_invalid_state(all_devices_with_big_handler)
    all_valid_devices = get_devices_with_valid_state(all_devices_with_big_handler, failed_devices_id)

    print(f"_______________Failed test {len(failed_devices_id)} devices________________")

    for device in failed_devices_id:
        print(f"Device {device} was removed")

    print(f"_______________Success test {len(all_valid_devices)} devices______________")

    for key, value in all_valid_devices.items():
        print(f"Device {key} sent {value} statuses")
