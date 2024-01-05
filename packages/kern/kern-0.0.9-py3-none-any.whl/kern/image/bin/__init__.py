#!/usr/bin/env python3

__all__ = ['main']

import sys

def main(argv=None):

    import argparse
    from kern import image

    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser('image')
    parser.add_argument('query', nargs='?')
    args = parser.parse_args(argv)

    file = sys.stdin.buffer

    if args.query is None:
        text = image.to_text(file)
    else:
        text = image.and_text_to_text(file, args.query)
    print(text)

if __name__ == '__main__':
    main(sys.argv[1:])
