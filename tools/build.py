#!/usr/bin/env python3
"""Validate the BASIC listing and build a reproducible 720 KiB MSX FAT12 disk."""
from pathlib import Path
import re
import struct
import hashlib
import argparse

ROOT = Path(__file__).resolve().parents[1]


def validate(source: str) -> None:
    previous = -1
    numbers = set()
    for raw in source.splitlines():
        match = re.fullmatch(r"(\d+) (.*)", raw)
        if not match:
            raise ValueError(f"Not a numbered BASIC line: {raw!r}")
        number = int(match[1])
        if not previous < number <= 65529:
            raise ValueError(f"Duplicate or out-of-order line: {number}")
        if len(raw.encode("ascii")) > 255:
            raise ValueError(f"Line {number} exceeds the MSX editor limit")
        previous = number
        numbers.add(number)
    for raw in source.splitlines():
        code = raw.split("REM", 1)[0]
        for target in re.findall(r"\b(?:GOTO|GOSUB|RESTORE|THEN|ELSE)\s+(\d+)\b", code):
            if int(target) not in numbers:
                raise ValueError(f"Missing target {target} in {raw}")
    # These are the exact eight bytes requested in the original brief.
    for value in ["99", "5A", "7E", "DB", "FF", "3C", "42", "81"]:
        if f"CHR$(&H{value})" not in source:
            raise ValueError("The requested sprite pattern is missing")


def set_fat12(fat: bytearray, cluster: int, value: int) -> None:
    offset = cluster + cluster // 2
    if cluster & 1:
        fat[offset] = (fat[offset] & 0x0F) | ((value & 0x0F) << 4)
        fat[offset + 1] = value >> 4
    else:
        fat[offset] = value & 0xFF
        fat[offset + 1] = (fat[offset + 1] & 0xF0) | ((value >> 8) & 0x0F)


def make_disk(files: dict[str, bytes]) -> bytes:
    sector = 512
    disk = bytearray(1440 * sector)
    # Standard MSX 720K BPB: 2 sectors/cluster, 112 root entries, two FATs.
    disk[0:3] = b"\xeb\xfe\x90"
    disk[3:11] = b"MSXGAME "
    struct.pack_into("<HBHBHHBHHH", disk, 11,
                     512, 2, 1, 2, 112, 1440, 0xF9, 3, 9, 2)
    # Disk ROM calls the Z80 entry at offset 0x1e. RET returns to Disk BASIC,
    # which then runs AUTOEXEC.BAS; an empty entry would execute random memory.
    disk[0x1E] = 0xC9
    disk[510:512] = b"\x55\xaa"
    fat = bytearray(3 * sector)
    fat[0:3] = b"\xf9\xff\xff"
    cluster = 2
    for index, (name, data) in enumerate(files.items()):
        stem, extension = name.split(".")
        first_cluster = cluster
        count = (len(data) + 1023) // 1024
        for offset in range(count):
            set_fat12(fat, cluster, 0xFFF if offset == count - 1 else cluster + 1)
            start = (14 + (cluster - 2) * 2) * sector
            chunk = data[offset * 1024:(offset + 1) * 1024]
            disk[start:start + len(chunk)] = chunk
            cluster += 1
        entry = bytearray(32)
        entry[0:11] = (stem.ljust(8) + extension.ljust(3)).encode("ascii")
        entry[11] = 0x20
        struct.pack_into("<H", entry, 24, 0x5C21)  # reproducible 2026-01-01 date
        struct.pack_into("<HI", entry, 26, first_cluster, len(data))
        disk[7 * sector + index * 32:7 * sector + (index + 1) * 32] = entry
    disk[sector:4 * sector] = fat
    disk[4 * sector:7 * sector] = fat
    return bytes(disk)


def build(check: bool = False) -> None:
    source = (ROOT / "game/ZOMBIE.BAS").read_text(encoding="ascii")
    validate(source)
    basic = source.replace("\r\n", "\n").replace("\n", "\r\n").encode("ascii")
    disk = make_disk({
        "AUTOEXEC.BAS": b'10 RUN "ZOMBIE.BAS"\r\n\x1a',
        "ZOMBIE.BAS": basic + b"\x1a",
    })
    outputs = {
        ROOT / "docs/game/ZOMBIE.BAS": basic,
        ROOT / "docs/game/ZOMBIE.DSK": disk,
    }
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_bytes() != content:
                raise SystemExit(f"Rebuild required: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print(f"Validated {len(source.splitlines())} BASIC lines; {len(basic)} source bytes")
    print(f"720K bootable Disk BASIC image: SHA256 {hashlib.sha256(disk).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated files without writing")
    build(parser.parse_args().check)
