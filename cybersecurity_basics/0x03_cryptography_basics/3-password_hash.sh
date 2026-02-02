#!/bin/bash
salt=$(openssl rand -base64 12 | cut -c1-16)
echo -n "$1$salt" | openssl dgst -sha512 > 3_hash.txt
