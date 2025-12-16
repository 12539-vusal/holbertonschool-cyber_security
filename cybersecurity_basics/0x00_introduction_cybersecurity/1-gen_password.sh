#!/bin/bash
tr -d '[:alnum:]' < /dev/urandom | head -c $1
