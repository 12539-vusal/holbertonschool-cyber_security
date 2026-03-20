#!/bin/bash
sudo nmap $1 -sF -p80,85 -ff -T2
