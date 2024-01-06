from typing import List

import typer

from device import Device


def format_device_list(devices: List[Device]) -> str:
    output = ""
    for device in devices:
        output += str(device) + '\n'
    return output


def print_devices(devices: List[Device]):
    if not devices:
        typer.echo("there are 0 devices")
        return

    typer.echo("devices: ")
    for device in devices:
        typer.echo(f"🖥️ {device}")
    typer.echo(f"there are {len(devices)} devices")
