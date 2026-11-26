#!/usr/bin/env python3
"""THE WORLD TODAY - Wednesday, 25 November 2026.

A one-page newspaper image summing up the day's world news.
This program copies the shipped image to the output location.
Standard library only, no network, deterministic: the same bytes
go out on every run.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
