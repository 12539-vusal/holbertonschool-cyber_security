#!/bin/bash
head -n 1 /dev/urandom | tr -dc '[:alnum:]'
