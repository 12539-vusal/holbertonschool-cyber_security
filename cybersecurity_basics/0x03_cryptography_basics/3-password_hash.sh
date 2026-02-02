#!/bin/bash
echo -n "$1$(openssl rand -base64 12 | cut -c1-16)" | openssl dgst -sha512 > 3_hash.txt
