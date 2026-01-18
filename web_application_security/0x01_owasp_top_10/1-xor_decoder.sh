#!/bin/bash

# Check if the argument is provided
if [ -z "$1" ]; then
  echo "Usage: ./1-xor_decoder.sh {xor}encoded_string"
  exit 1
fi

# Remove the {xor} prefix
encoded=$(echo "$1" | sed 's/{xor}//')

# Base64 decode the input
decoded=$(echo "$encoded" | base64 -d 2>/dev/null)

# Check if base64 decoding succeeded
if [ $? -ne 0 ]; then
  echo "Error: Invalid Base64 input."
  exit 1
fi

# Define XOR key (you can modify this based on the actual key)
key=95

# Perform XOR decoding by looping through each character
decoded_message=""
for (( i=0; i<${#decoded}; i++ )); do
    char=$(printf "%d" "'${decoded:$i:1}")  # Get ASCII value of each char
    xor_char=$(($char ^ $key))              # XOR with the key
    decoded_message+=$(printf \\$(printf '%03o' "$xor_char"))  # Convert back to character
done

# Output the decoded message
echo "$decoded_message"
