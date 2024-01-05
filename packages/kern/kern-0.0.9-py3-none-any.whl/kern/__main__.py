#!/usr/bin/env python3

__all__ = ['main']

import os
import sys
import kern
import shutil
import argparse
import subprocess

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser('input')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(argv)

    streams = []
    if not os.isatty(sys.stdin.fileno()):
        stream = sys.stdin.buffer
        streams.append(stream)

    for file in args.files:
        stream = open(file, 'rb')
        streams.append(stream)

    blobs_with_types = []
    for stream in streams:
        blob = stream.read()
        if kern.is_image(blob):
            proc = subprocess.Popen(["input-image"], stdin=subprocess.PIPE)
            proc.communicate(blob)
        if kern.is_pdf(blob):
            proc = subprocess.Popen(["input-pdf"], stdin=subprocess.PIPE)
            proc.communicate(blob)
        if kern.is_doc(blob):
            proc = subprocess.Popen(["input-doc"], stdin=subprocess.PIPE)
            proc.communicate(blob)
        if kern.is_html(blob):
            proc = subprocess.Popen(["input-html"], stdin=subprocess.PIPE)
            proc.communicate(blob)
        if kern.is_url(blob):
            proc = subprocess.Popen(["input-url"], stdin=subprocess.PIPE)
            proc.communicate(blob)

if __name__ == '__main__':
    main(sys.argv[1:])
