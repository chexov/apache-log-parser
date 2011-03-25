#!/usr/bin/env python
# encoding: utf-8
import sys
import re


def parse(log_f):
    'Return tuple of dictionaries containing file data.'
    def make_entry(x):
        return {
            'server_ip':x.group('ip'),
            'uri':x.group('uri'),
            'time':x.group('time'),
            'status_code':x.group('status_code'),
            'referral':x.group('referral'),
            'agent':x.group('agent'),
            }

    log_re = '(?P<ip>[.\d]+) - - \[(?P<date>\d\d\/\w\w\w\/\d\d\d\d):(?P<time>.*?)\] "(?P<method>\w+?) (?P<uri>.*?) HTTP/1.\d" (?P<status_code>\d+) \d+ "(?P<referral>.*?)" "(?P<agent>.*?)"'

    search = re.compile(log_re).search

    # read file line by line.
    # in case we have match yield dict
    # otherwise yield empty dict to make it looks consistant
    while True:
        try:
            line = log_f.next()
        except StopIteration:
            break
        match = search(line)
        if match:
            yield match.groupdict()
        else:
            print "no match for", line
            yield {}


def print_selected_keys(filename, key_list):
    parsed_log = parse(filename)
    while True:
        try:
            log_item = parsed_log.next()
        except StopIteration:
            break

        # Filters incomming log_item dict()
        # returns new dict() with only key_list keys in it
        #result_dict = dict(filter(lambda _kv: _kv[0] in key_list,
        #    log_item.items()))
        for key in key_list:
            print log_item.get(key),
        print ""


def main():
    if len(sys.argv) <= 1:
        print "Usage: %s <key> [<key>,<key>,..]" % sys.argv[0]
        print "Available keys: ip time uri agent statys_code referral"
        print "Input log goes to stdin"
        sys.exit(1)

    print_selected_keys(sys.stdin, sys.argv[1:])

if __name__ == '__main__':
    main()

