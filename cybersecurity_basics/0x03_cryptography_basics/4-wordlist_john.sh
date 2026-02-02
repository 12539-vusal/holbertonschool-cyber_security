#!/bin/bash
john --wordlist=/usr/share/john/rockyou.txt --format=Raw-MD5 "$1"
