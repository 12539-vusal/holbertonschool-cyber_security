#!/bin/bash
echo $1 $2 | sha256sum -c
