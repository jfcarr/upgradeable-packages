# Upgradeable Packages (upgradeable_packages)

For Debian-based systems, this script calls apt, flatpak, and snap to determine if updates are pending and returns an UpgradeResult enum with "NOT_APPLICABLE", "PENDING", or "UP_TO_DATE", accordingly.

## Requirements / Setup

This project requires [uv](https://docs.astral.sh/uv/).

Initialize the project with:

```bash
uv sync
```

## Usage

The script is directly runnable: It has a crunchbang line that manages uv.

Check APT:

```bash
./upgradeable_packages.py --apt
```

Check Flatpak:

```bash
./upgradeable_packages.py --flatpak
```

Check Snap:

```bash
./upgradeable_packages.py --snap
```

Check all sources:

```bash
./upgradeable_packages.py --combined
```
