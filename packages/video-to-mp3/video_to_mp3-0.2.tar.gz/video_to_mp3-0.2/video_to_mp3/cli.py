import argparse
from .video_to_mp3 import convert


# @click.command()
# @click.option("--input", default=BASE_DIR, help="path of the input file")
# @click.option("--output", default=BASE_DIR, help="path of the output file")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='path of the input file', required=True)
    parser.add_argument('--output', help='path of the output file')
    args = parser.parse_args()
    convert(args.input, args.output)


if __name__ == '__main__':
    main()