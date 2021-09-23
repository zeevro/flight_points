#!/usr/bin/python3
import argparse
import csv
import json
import os

def process_file(in_file, out_file, names_file):
    points = []
    for row in csv.DictReader(in_file):
        lat_d, lat_m, lat_s, lat_ns, lon_d, lon_m, lon_s, lon_ew = row['Coordinates'].split()

        points.append({
            'code': row['Code'],
            'name': row['Name'].replace('-', ' '),
            'kind': row['Type'],
            'lat': round((int(lat_d[:-1]) + int(lat_m[:-1]) / 60 + int(lat_s[:-1]) / 3600) * {'N': 1, 'S': -1}[lat_ns], 6),
            'lon': round((int(lon_d[:-1]) + int(lon_m[:-1]) / 60 + int(lon_s[:-1]) / 3600) * {'E': 1, 'W': -1}[lon_ew], 6),
        })

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
