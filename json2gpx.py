import argparse
import json
import sys

from gpxpy.gpx import GPX, GPXWaypoint


KINDS = {
    'חובה': 'CRP',
    'דרישה': 'NCRP',
    'ARP': 'ARP',
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('in_files', metavar='input-file', type=argparse.FileType('r', encoding='utf-8'), default=[sys.stdin], nargs='*')
    p.add_argument('-o', '--out-file', type=argparse.FileType('w', encoding='utf-8'), default=sys.stdout)
    args = p.parse_args()

    all_points = []
    for f in args.in_files:
        points = json.load(f)
        if not all_points:
            all_points.extend(points)
            continue
        for point in points:
            for existing_point in all_points


    gpx_doc = GPX()
    gpx_doc.creator = 'Flight points GPX creator'
    gpx_doc.name = 'Israel flying navigation points'

    points = json.load(args.in_file)

    for point in points:
        wpt = GPXWaypoint(
            latitude=point['lat'],
            longitude=point['lon'],
            name=point['name'],
            type=KINDS[point['type']]
        )
        gpx_doc.waypoints.append(wpt)

    args.out_file.write(gpx_doc.to_xml())

    print('Done.')


if __name__ == '__main__':
    main()
