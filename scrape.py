#! /usr/bin/env python
# coding=utf-8
import argparse
import sys
from collections import defaultdict
import pickle
import getpass
try:
    import readline
except:
    pass

import requests
from pyquery import PyQuery

import distill

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Scrape LiU Studentportalen for course registrations.")
    parser.add_argument(
        '-u', 
        '--username',
        help='LiU login (abcde123)')
    parser.add_argument(
        '-p', 
        '--password', 
        default=None,
        help='asked for if not given as an argument')
    parser.add_argument(
        '-o', 
        '--output',
        default=None,
        help='output file (pickled); default INPUT.p')
    parser.add_argument(
        'input', 
        metavar='INPUT', 
        help='a file in which each line is a LiU id (abcde123)')

    args = parser.parse_args()

    if args.password:
        password = args.password
    else:
        password = getpass.getpass()

    portal_url = 'https://www3.student.liu.se/portal'

    with requests.session() as session:
        r = session.post('%s/login' % portal_url, data={
            'user': args.username, 
            'pass': password})
        liu_ids = []
        with open(args.input, 'rp') as f:
            liu_ids = [l.strip() for l in f.read().splitlines()]

        dump = {}
        dump['course_names'] = {} # course code to course name mapping
        dump['course_regs'] = defaultdict(list) # regged ids
        dump['course_reg_counts'] = defaultdict(int) # no of regged ids

        for liu_id in liu_ids:
            r = session.get('%s/search' % portal_url, params={
                'searchtext': liu_id,
                'search': 'Sök',
                })
            r = session.get('%s/search' % portal_url, params={
                'detailpage': 'true',
                'advancedsearch': 'true',
                'offset': 0,
                'mail': "%s@student.liu.se" % liu_id,
                'displayedresults': ''})
            pq = PyQuery(r.content)
            regsib = pq('td i:contains("Kursregistreringar:")')
            if not regsib:
                sys.stderr.write('no regs for %s\n' % liu_id)
                sys.stderr.flush()
                continue
            reghtml = regsib.parent().next().html()
            blocks = [" ".join(b.split()) for b in reghtml.split('<br/>')]
            for block in blocks:
                lparen = block.find('(')
                rparen = block.find(')')
                name = block[0:lparen-1]
                code = block[lparen+1:rparen]
                dump['course_names'][code] = name
                dump['course_regs'][code].append(liu_id)
                dump['course_reg_counts'][code] += 1

        if args.output:
            out_file = args.output
        else:
            out_file = "%s.p" % args.input
        pickle.dump(dump, open(out_file, 'wb'))
        sys.stdout.write('\nSummary:\n')
        sys.stdout.write(distill.summary(dump))
        sys.stdout.flush()
