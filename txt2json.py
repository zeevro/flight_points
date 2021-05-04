#!/usr/bin/python3
import argparse
import json
import os


FIXES = [
    ('\x04', 'ף'),
    ('\x05', 'ף'),
    ('\x08', 'ך'),
    ('\x11', 'ן'),
    ('\x1f', 'ם'),
    ('\x16', 'ן'),
    ('\t', 'ס'),
    ('ס-', '-ס'),
    ('ʤʡʥʧ', 'חובה'),
]

SOFIT_LETTERS = set('ךםןףץ')

KINDS = [
    'ARP',
    'חובה',
    'דרישה',
]


def fix_name(name):
    if all(c not in name for c in ' -'):
        if name[0] in SOFIT_LETTERS:
            return name[1:] + name[0]
        return name

    for sep in ' -':
        if sep not in name:
            continue
        words = name.split(sep)
        for n, word in enumerate(words):
            if word[0] in SOFIT_LETTERS:
                words[n - 1] = words[n - 1] + word[0]
                words[n] = word[1:]
        name = sep.join(words)

    return name


def process_line(line):
    line = line.rstrip('\r\n')
    for search, replace in FIXES:
        line = line.replace(search, replace)
    return line


def process_file(in_file, out_file, names_file):
    points = []
    for line in in_file:
        line = process_line(line)

        if (line.endswith(' ')) or (not any(k in line for k in KINDS)):
            line += 'ס' + process_line(in_file.readline())

        try:
            code, lat_d, lat_m, lat_s, lat_ns, lon_d, lon_m, lon_s, lon_ew, rest = line.split(maxsplit=9)

            if 'ARP' in rest:
                kind, name = rest.split(maxsplit=1)
            else:
                name, kind = rest.rsplit(maxsplit=1)

            if kind not in KINDS:
                name, kind = kind, name

            assert kind in KINDS, f'kind = {kind!r}'

            if SOFIT_LETTERS.intersection(name):
                name = fix_name(name)

            name = name.replace('-', ' ')
        except Exception as e:
            print(f'ERROR! {e.__class__.__name__}: {e} [{os.path.basename(in_file.name)}: {line!r}]')
            continue

        points.append({
            'code': code,
            'name': name,
            'kind': kind,
            'lat': round((int(lat_d[:-1]) + int(lat_m[:-1]) / 60 + int(lat_s[:-1]) / 3600) * {'N': 1, 'S': -1}[lat_ns], 6),
            'lon': round((int(lon_d[:-1]) + int(lon_m[:-1]) / 60 + int(lon_s[:-1]) / 3600) * {'E': 1, 'W': -1}[lon_ew], 6),
        })

    if names_file:
        for p in points:
            print(p['code'], p['name'], file=names_file)

    json.dump(points, out_file, indent=2, separators=(',', ': '), ensure_ascii=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--in-file', type=argparse.FileType('r', encoding='utf-8'), default='-')
    p.add_argument('-o', '--out-file', type=argparse.FileType('w', encoding='utf-8'), default='-')
    p.add_argument('-N', '--names-file', type=argparse.FileType('w', encoding='utf-8'))
    args = p.parse_args()

    process_file(args.in_file, args.out_file, args.names_file)


if __name__ == "__main__":
    main()
