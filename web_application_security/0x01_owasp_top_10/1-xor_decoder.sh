#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./1-xor_decoder.sh {xor}encoded_string"
  exit 1
fi
encoded=$(echo "$1" | sed 's/{xor}//')
decoded=$(echo "$encoded" | base64 -d 2>/dev/null)
if [ $? -ne 0 ]; then
  echo "Error: Invalid Base64 input."
  exit 1
fi
key=95
decoded_message=""
for (( i=0; i<${#decoded}; i++ )); do
    char=$(printf "%d" "'${decoded:$i:1}")
    xor_char=$(($char ^ $key))
    decoded_message+=$(printf \\$(printf '%03o' "$xor_char"))
done
echo "$decoded_message"
