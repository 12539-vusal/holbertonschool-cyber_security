#!/bin/bash
echo $2 | sha256sum -c $1
