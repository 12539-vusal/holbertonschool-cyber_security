#!/bin/bash
sudo nmap $1 -p440,450 --open --reason --packet-trace -sX
