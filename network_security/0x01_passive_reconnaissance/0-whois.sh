#!/bin/bash
whois "$1" | awk -F': *' '/^(Registrant|Admin|Tech)/ && !/^Registry/ {f=$1; v=$2; if(f~/(Phone Ext|Fax Ext)$/) f=f":"; print f ", " v}' >"$1.csv"
