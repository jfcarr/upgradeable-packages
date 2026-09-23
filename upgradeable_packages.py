#!/usr/bin/env -S uv run -q -s

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "argparse>=1.4.0",
# ]
# ///

import argparse
import shutil
import subprocess
import sys
from enum import Enum


class UpgradeResult(Enum):
    UP_TO_DATE = 1
    PENDING = 2
    NOT_APPLICABLE = 3


def apt_upgrades_available() -> UpgradeResult:
    result = subprocess.run(
        ["apt-get", "-s", "-q", "upgrade"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return UpgradeResult.NOT_APPLICABLE

    for line in result.stdout.splitlines():
        if line.startswith("Inst "):
            return UpgradeResult.PENDING

    return UpgradeResult.UP_TO_DATE


def flatpak_upgrades_available() -> UpgradeResult:
    if shutil.which("flatpak") is None:
        return UpgradeResult.NOT_APPLICABLE

    result = subprocess.run(
        ["flatpak", "remote-ls", "--updates"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return UpgradeResult.NOT_APPLICABLE

    return (
        UpgradeResult.PENDING
        if bool(result.stdout.strip())
        else UpgradeResult.UP_TO_DATE
    )


def snap_upgrades_available() -> UpgradeResult:
    if shutil.which("snap") is None:
        return UpgradeResult.NOT_APPLICABLE

    result = subprocess.run(
        ["snap", "refresh", "--list"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return UpgradeResult.NOT_APPLICABLE

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # Ignore the table header and the no-updates message.
    ignored = {
        "Name Version Rev Tracking Publisher Notes",
        "All snaps up to date.",
    }

    return (
        UpgradeResult.PENDING
        if any(line not in ignored for line in lines)
        else UpgradeResult.UP_TO_DATE
    )


def main():
    parser = argparse.ArgumentParser(
        prog="upgradeable_packages",
        description="Show upgradeable status for apt, flatpak, and snap.",
    )

    parser.add_argument(
        "-a",
        "--apt",
        action="store_true",
        default=False,
        help="Check for upgradeable APT packages.",
    )

    parser.add_argument(
        "-f",
        "--flatpak",
        action="store_true",
        default=False,
        help="Check for upgradeable Flatpak packages.",
    )

    parser.add_argument(
        "-s",
        "--snap",
        action="store_true",
        default=False,
        help="Check for upgradeable Snap packages.",
    )

    parser.add_argument(
        "-c",
        "--combined",
        action="store_true",
        default=False,
        help="Check for any upgradeable packages.",
    )

    args = parser.parse_args()

    try:
        if args.apt:
            apt_has_upgrades = apt_upgrades_available()

            if apt_has_upgrades == UpgradeResult.NOT_APPLICABLE:
                print("n/a")
            else:
                print(
                    "pending"
                    if apt_has_upgrades == UpgradeResult.PENDING
                    else "up-to-date"
                )

        if args.flatpak:
            flatpak_has_upgrades = flatpak_upgrades_available()

            if flatpak_has_upgrades == UpgradeResult.NOT_APPLICABLE:
                print("n/a")
            else:
                print(
                    "pending"
                    if flatpak_has_upgrades == UpgradeResult.PENDING
                    else "up-to-date"
                )

        if args.snap:
            snap_has_upgrades = snap_upgrades_available()

            if snap_has_upgrades == UpgradeResult.NOT_APPLICABLE:
                print("n/a")
            else:
                print(
                    "pending"
                    if snap_has_upgrades == UpgradeResult.PENDING
                    else "up-to-date"
                )

        if args.combined:
            apt_has_upgrades = apt_upgrades_available()
            flatpak_has_upgrades = flatpak_upgrades_available()
            snap_has_upgrades = snap_upgrades_available()

            print(
                "pending"
                if apt_has_upgrades == UpgradeResult.PENDING
                or flatpak_has_upgrades == UpgradeResult.PENDING
                or snap_has_upgrades == UpgradeResult.PENDING
                else "up-to-date"
            )

    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
