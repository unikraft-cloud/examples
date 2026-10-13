#!/usr/bin/env python3
"""Apply the plugin configuration to the desktop.

Read the JSON configuration from the file given as the first argument, write
the lxpanel panel, and print shell assignments for the wrapper. A missing or
incorrect configuration gives the default desktop.

Configuration keys, all optional:

    resolution  "<width>x<height>", for example "1280x800"
    launchers   list of {"name": str, "exec": str, "icon": str (optional)},
                added to the panel after the default launchers
    autostart   list of shell commands, started after the desktop
    password    password for HTTP Basic Auth on noVNC, no authentication if
                not set
    user        user name for HTTP Basic Auth, "novnc" if not set

The environment variables NOVNC_PASSWORD and NOVNC_USER replace "password" and
"user" of the configuration.
"""

import json
import os
import re
import shlex
import sys

PANEL = "/etc/xdg/lxpanel/default/panels/panel"
AUTH_FILE = "/etc/novnc/auth"
MENU_ICON = "/usr/share/icons/Adwaita/symbolic/actions/view-app-grid-symbolic.svg"
DEFAULT_ICON = "/usr/share/icons/Adwaita/scalable/mimetypes/application-x-executable.svg"
DEFAULT_USER = "novnc"
DEFAULT_LAUNCHERS = [
    {"name": "Terminal", "exec": "xterm",
     "icon": "/usr/share/pixmaps/mini.xterm_48x48.xpm"},
    {"name": "Firefox", "exec": "firefox-esr -new-window",
     "icon": "firefox-esr"},
]


def warn(msg):
    print(f"novnc-config: {msg}", file=sys.stderr)


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        warn(f"ignoring {path}: {e}")
        return {}

    if not isinstance(cfg, dict):
        warn("ignoring the configuration, it is not a JSON object")
        return {}

    return cfg


def is_text(value):
    # lxpanel reads one value per line, thus a newline would break the panel
    return isinstance(value, str) and value != "" and "\n" not in value


def get_list(cfg, key):
    value = cfg.get(key, [])
    if not isinstance(value, list):
        warn(f"ignoring '{key}', it is not a list")
        return []
    return value


def launchers(cfg):
    items = list(DEFAULT_LAUNCHERS)

    for item in get_list(cfg, "launchers"):
        if not isinstance(item, dict) or not is_text(item.get("name")) or \
                not is_text(item.get("exec")):
            warn(f"ignoring launcher {item!r}, it needs 'name' and 'exec'")
            continue

        icon = item.get("icon")
        items.append({"name": item["name"], "exec": item["exec"],
                      "icon": icon if is_text(icon) else DEFAULT_ICON})

    return items


def button(item):
    return ("    Button {\n"
            f"      image={item['icon']}\n"
            f"      tooltip={item['name']}\n"
            f"      action={item['exec']}\n"
            "    }\n")


def write_panel(items):
    os.makedirs(os.path.dirname(PANEL), exist_ok=True)
    with open(PANEL, "w", encoding="utf-8") as f:
        f.write("Global {\n"
                "  edge=bottom\n"
                "  align=left\n"
                "  margin=0\n"
                "  widthtype=percent\n"
                "  width=100\n"
                "  height=32\n"
                "  iconsize=24\n"
                "  setdocktype=1\n"
                "  setpartialstrut=1\n"
                "  autohide=0\n"
                "}\n"
                "Plugin {\n"
                "  type=menu\n"
                "  Config {\n"
                f"    image={MENU_ICON}\n"
                "    system {\n"
                "    }\n"
                "  }\n"
                "}\n"
                "Plugin {\n"
                "  type=launchbar\n"
                "  Config {\n")
        for item in items:
            f.write(button(item))
        f.write("  }\n"
                "}\n"
                "Plugin {\n"
                "  type=taskbar\n"
                "  expand=1\n"
                "  Config {\n"
                "    tooltips=1\n"
                "    IconsOnly=0\n"
                "    ShowAllDesks=0\n"
                "    MaxTaskWidth=200\n"
                "  }\n"
                "}\n"
                "Plugin {\n"
                "  type=dclock\n"
                "  Config {\n"
                "    ClockFmt=%R\n"
                "  }\n"
                "}\n")


def write_auth(creds):
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    fd = os.open(AUTH_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(creds)


def main():
    cfg = load(sys.argv[1])

    write_panel(launchers(cfg))

    resolution = cfg.get("resolution")
    if resolution is not None:
        m = re.fullmatch(r"([1-9][0-9]{2,4})x([1-9][0-9]{2,4})",
                         str(resolution))
        if m:
            print(f"WIDTH={m.group(1)}")
            print(f"HEIGHT={m.group(2)}")
        else:
            warn(f"ignoring resolution {resolution!r}, use <width>x<height>")

    password = os.environ.get("NOVNC_PASSWORD") or cfg.get("password")
    user = os.environ.get("NOVNC_USER") or cfg.get("user", DEFAULT_USER)
    if password is not None:
        # websockify splits the auth source at the first ':'
        if not is_text(password) or not is_text(user) or ":" in user:
            warn("ignoring 'password' and 'user', they must be text and "
                 "'user' must not contain ':'")
        else:
            write_auth(f"{user}:{password}")
            print(f"NOVNC_AUTH_FILE={AUTH_FILE}")

    commands = [c for c in get_list(cfg, "autostart") if is_text(c)]
    print("AUTOSTART=(" + " ".join(shlex.quote(c) for c in commands) + ")")


if __name__ == "__main__":
    main()
