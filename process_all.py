import glob

from txt2json import process_file


def main():
    for fn in glob.glob('*.txt'):
        if fn.endswith('-names.txt'):
            continue

        with open(fn, encoding='utf8') as in_f, open(f'{fn[:-4]}.json', 'w', encoding='utf8') as out_f, open(f'{fn[:-4]}-names.txt', 'w', encoding='utf8') as names_f:
            process_file(in_f, out_f, names_f)


if __name__ == "__main__":
    main()
