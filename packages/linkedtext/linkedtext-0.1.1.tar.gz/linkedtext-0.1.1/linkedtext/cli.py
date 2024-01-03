"""
CLI
"""

from linkedtext import LinkedText
import argparse


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
        '-f',
        '--filename',
        type=str,
        help='Markdown file.',
        required=True
    )

    args = parser.parse_args()

    filename = args.filename

    if filename is not None:
        r = LinkedText(markdown_file=filename)
        r.process()
        print('Task Complete!.')


if __name__ == '__main__':
    main()
