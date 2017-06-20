#!/usr/bin/python

import time
import argparse
import json
import os
from sys import exit
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

DEBUG = int(os.environ.get('DEBUG', '0'))


class SaltCollector(object):

    def __init__(self, filename, port):
        self.filename = filename
        self.port = port

    def collect(self):
        record = self._request_data()
        self._setup_empty_prometheus_metrics(record)

        for metric in self._prometheus_metrics.values():
            yield metric

    def _request_data(self):
        return json.loads(open(self.filename, 'r').read().strip())

    def _setup_empty_prometheus_metrics(self, record):
        # The metrics we want to export.
        names = set(['is_running', 'minions'])
        self._prometheus_metrics = {}
        for k, v in record.iteritems():
            if k not in names:
                continue
            if k != 'minions':
                self._prometheus_metrics[k] = GaugeMetricFamily('salt_master_{}'.format(k),
                                                                       'salt_master_{}'.format(k),
                                                                       value=v,
                                                                       labels=None)
            else:
                for k1, v1 in v.iteritems():
                    self._prometheus_metrics["minions_{}".format(k1)] = GaugeMetricFamily('salt_master_minions_{}'.format(k1),
                                                                                          'salt_master_minions_{}'.format(k1),
                                                                                          value=v1,
                                                                                          labels=None)

def parse_args():
    parser = argparse.ArgumentParser(
        description='salt master exporter args filename path'
    )
    parser.add_argument(
        '--filename',
        metavar='filename',
        required=False,
        help='Filename and path',
        default='/tmp/salt_metrics.json'
    )
    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default='9118'
    )
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        port = int(args.port)
        REGISTRY.register(SaltCollector(args.filename, args.port))
        start_http_server(port)
        print "Polling %s. Serving at port: %s" % (args.filename, port)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)

if __name__ == "__main__":
    main()
