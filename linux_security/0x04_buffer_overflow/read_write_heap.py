#!/usr/bin/python3
"""
read_write_heap.py

This script searches for a string in the heap of a running process and
replaces it with another string of the same length or less.

Usage:
    ./read_write_heap.py <pid> <search_string> <replace_string>

Note:
    - You must have permission to read/write the process memory (run as root).
    - Replacement string must not be longer than the original.
"""

import sys
import os


def find_heap(pid):
    """
    Parse /proc/<pid>/maps to locate the heap segment.

    Args:
        pid (str): Process ID

    Returns:
        tuple: (start_address, end_address) of the heap as integers
    """
    try:
        with open(f'/proc/{pid}/maps', 'r') as maps_file:
            for line in maps_file:
                if '[heap]' not in line:
                    continue

                parts = line.split()
                start_str, end_str = parts[0].split('-')
                start = int(start_str, 16)
                end = int(end_str, 16)
                return start, end
    except FileNotFoundError:
        print(f'Error: Process {pid} not found', file=sys.stdout)
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f'Error reading process maps: {e}', file=sys.stdout)
        sys.exit(1)

    print('Error: Heap not found', file=sys.stdout)
    sys.exit(1)


def get_heap(pid, start, end):
    """
    Read the heap segment from /proc/<pid>/mem.

    Args:
        pid (str): Process ID
        start (int): Start address of the heap
        end (int): End address of the heap

    Returns:
        bytes: Heap content
    """
    try:
        with open(f'/proc/{pid}/mem', 'rb') as heap:
            heap.seek(start)
            return heap.read(end - start)
    except PermissionError:
        print('Error: Permission denied. Run with sudo', file=sys.stdout)
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f'Error reading heap memory: {e}', file=sys.stdout)
        sys.exit(1)


def write_heap(pid, address, data):
    """
    Write data to a specific address in the process heap.

    Args:
        pid (str): Process ID
        address (int): Memory address to write to
        data (bytes): Data to write
    """
    try:
        with open(f'/proc/{pid}/mem', 'rb+') as heap:
            heap.seek(address)
            heap.write(data)
    except PermissionError:
        print('Error: Permission denied. Run with sudo', file=sys.stdout)
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f'Error writing to heap memory: {e}', file=sys.stdout)
        sys.exit(1)


def main():
    """
    Main function: Parse args, find heap, locate and replace string in memory.
    """
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py <pid> <search_str> <replace_str>",
              file=sys.stdout)
        sys.exit(1)

    # Validate PID is numeric
    try:
        pid_int = int(sys.argv[1])
        if pid_int <= 0:
            raise ValueError
    except ValueError:
        print("Error: PID must be a positive integer", file=sys.stdout)
        sys.exit(1)

    # Check if process exists
    if not os.path.exists(f'/proc/{sys.argv[1]}'):
        print(f"Error: Process {sys.argv[1]} not found", file=sys.stdout)
        sys.exit(1)

    pid = sys.argv[1]
    search = sys.argv[2].encode('ASCII')
    replace_raw = sys.argv[3].encode('ASCII')

    # Validate replacement string is not longer than search string
    if len(replace_raw) > len(search):
        print(f"Error: Replacement string too long "
              f"({len(replace_raw)} > {len(search)})", file=sys.stdout)
        sys.exit(1)

    # Pad replacement string with null bytes to match search length
    replace = replace_raw.ljust(len(search), b'\x00')

    # Find heap boundaries
    start, end = find_heap(pid)

    # Read heap memory
    mem = get_heap(pid, start, end)

    # Find search string in heap
    index = mem.find(search)
    if index == -1:
        print(f"Error: String '{sys.argv[2]}' not found in heap",
              file=sys.stdout)
        sys.exit(1)

    # Calculate absolute address and write replacement
    search_addr = start + index
    write_heap(pid, search_addr, replace)


if __name__ == "__main__":
    main()
