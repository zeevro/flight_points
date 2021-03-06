import argparse
import json

from gpxpy.gpx import GPX, GPXWaypoint


KINDS = {
    'חובה': 'CRP',
    'דרישה': 'NCRP',
    'ARP': 'ARP',
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--in-file', type=argparse.FileType('r', encoding='utf-8'), default='-')
    p.add_argument('-o', '--out-file', type=argparse.FileType('w', encoding='utf-8'), default='-')
    args = p.parse_args()

    gpx_doc = GPX()
    gpx_doc.creator = 'Flight points GPX creator'
    gpx_doc.name = 'Israel flying navigation points'

    points = json.load(args.in_file)

    for point in points:
        wpt = GPXWaypoint(
            latitude=point['lat'],
            longitude=point['lon'],
            name=point['name'],
            description=point['code'],
            type=KINDS.get(point['kind'], point['kind'])
        )
        gpx_doc.waypoints.append(wpt)

    args.out_file.write(gpx_doc.to_xml())

    print('Done.')


if __name__ == '__main__':
    main()
