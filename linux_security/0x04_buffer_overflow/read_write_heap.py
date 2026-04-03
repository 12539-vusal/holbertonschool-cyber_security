#!/usr/bin/python3
"""
read_write_heap.py - İşləyən prosesin heap yaddaşını dəyişdirir.

İstifadə: sudo python3 read_write_heap.py <PID> <axtarılan_string> <yeni_string>
Misal:     sudo python3 read_write_heap.py 6515 Holberton maroua
"""

import sys
import os


def print_usage():
    print("İstifadə: {} pid axtarılan_string yeni_string".format(sys.argv[0]))
    print("Misal:    sudo python3 {} 6515 Holberton maroua".format(sys.argv[0]))


def find_heap(pid):
    """
    /proc/<pid>/maps faylından heap bölgəsini tapır.
    Qaytarır: (başlanğıc_addr, son_addr) və ya None
    """
    maps_file = "/proc/{}/maps".format(pid)
    try:
        with open(maps_file, "r") as f:
            for line in f:
                # "[heap]" olan sətri axtar
                if "[heap]" in line:
                    # Formatı: aaaaaa-bbbbbb rw-p ...
                    parts = line.split()
                    addr_range = parts[0]
                    start_str, end_str = addr_range.split("-")
                    start = int(start_str, 16)
                    end   = int(end_str,   16)
                    print("[*] Heap tapıldı: 0x{:x} - 0x{:x} "
                          "(ölçü: {} bayt)".format(start, end, end - start))
                    return start, end
    except PermissionError:
        print("[!] İcazə yoxdur — sudo ilə işlət")
        sys.exit(1)
    except FileNotFoundError:
        print("[!] PID {} tapılmadı".format(pid))
        sys.exit(1)
    return None, None


def read_heap(pid, start, end):
    """
    /proc/<pid>/mem vasitəsilə heap məzmununu oxuyur.
    """
    mem_file = "/proc/{}/mem".format(pid)
    size = end - start
    try:
        with open(mem_file, "rb") as f:
            f.seek(start)
            heap_data = f.read(size)
        return heap_data
    except PermissionError:
        print("[!] /proc/{}/mem oxumaq üçün icazə yoxdur".format(pid))
        sys.exit(1)


def write_heap(pid, offset, new_bytes):
    """
    /proc/<pid>/mem vasitəsilə heap-ə yeni dəyər yazır.
    """
    mem_file = "/proc/{}/mem".format(pid)
    try:
        with open(mem_file, "rb+") as f:
            f.seek(offset)
            f.write(new_bytes)
        print("[+] Uğurla yazıldı!")
    except PermissionError:
        print("[!] /proc/{}/mem-ə yazmaq üçün icazə yoxdur".format(pid))
        sys.exit(1)


def main():
    # ── Arqument yoxlaması ─────────────────────────────────────────────────
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    pid        = sys.argv[1]
    search_str = sys.argv[2]
    new_str    = sys.argv[3]

    # PID rəqəm olmalıdır
    if not pid.isdigit():
        print("[!] PID rəqəm olmalıdır")
        print_usage()
        sys.exit(1)

    pid = int(pid)

    print("[*] PID         : {}".format(pid))
    print("[*] Axtarılan   : '{}'".format(search_str))
    print("[*] Yeni string : '{}'".format(new_str))

    # Yeni string köhnədən uzun olmamalıdır (null terminator üçün)
    search_bytes = search_str.encode("utf-8") + b"\x00"
    new_bytes    = new_str.encode("utf-8")    + b"\x00"

    if len(new_bytes) > len(search_bytes):
        print("[!] Xəbərdarlıq: yeni string köhnədən uzundur ({} > {})".format(
            len(new_bytes), len(search_bytes)))
        print("    Bu heap korrupsiyasına səbəb ola bilər!")
        # Yenə də davam edirik, amma xəbərdar edirik

    # ── Heap bölgəsini tap ─────────────────────────────────────────────────
    heap_start, heap_end = find_heap(pid)
    if heap_start is None:
        print("[!] Heap tapılmadı")
        sys.exit(1)

    # ── Heap məzmununu oxu ─────────────────────────────────────────────────
    print("[*] Heap oxunur...")
    heap_data = read_heap(pid, heap_start, heap_end)

    # ── Stringi heap-də axtar ──────────────────────────────────────────────
    search_no_null = search_str.encode("utf-8")
    idx = heap_data.find(search_no_null)

    if idx == -1:
        print("[!] '{}' heap-də tapılmadı".format(search_str))
        sys.exit(1)

    absolute_offset = heap_start + idx
    print("[*] '{}' tapıldı → heap offset: {} | ünvan: 0x{:x}".format(
        search_str, idx, absolute_offset))

    # ── Yeni stringi yaz ───────────────────────────────────────────────────
    # Qalan baytları \x00 ilə doldur (köhnə stringin izlərini sil)
    pad_len   = len(search_no_null) - len(new_str.encode("utf-8"))
    write_data = new_str.encode("utf-8") + b"\x00" * (pad_len + 1)

    print("[*] 0x{:x} ünvanına yazılır: {}".format(
        absolute_offset, write_data))
    write_heap(pid, absolute_offset, write_data)

    print("[+] Tamamlandı! Proses indi '{}' çap etməlidir.".format(new_str))


if __name__ == "__main__":
    main()
