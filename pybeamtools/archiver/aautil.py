import argparse
import logging
import sys

from pybeamtools.archiver.aalib import AAClient

logger = logging.getLogger(__name__)

VALID_COMMANDS = ['status', 'pvadd', 'pvinfo', 'pvexport', 'pvsearch']

def main(argv=None):
    argv = argv or sys.argv
    logger.info('Starting aatool with [{}]'.format(sys.argv))

    if len(argv) < 2:
        print('Not enough arguments!')
        print(f'Usage: aatool <subcommand> [options]')
        print(f'Valid subcommands are {VALID_COMMANDS}')
        sys.exit(1)

    aa = AAClient()
    parser = argparse.ArgumentParser(prog='aatool')
    parser.add_argument('--verbose', action='store_true', help='verbose output')

    subparsers = parser.add_subparsers(help=f'available subcommands: {VALID_COMMANDS}')

    parser_a = subparsers.add_parser('export', help='export archiver data for specific PVs')
    parser_a.add_argument('pv', type=str, help='PV name or alias')
    parser_a.add_argument('--start', type=str, help='start time')
    parser_a.add_argument('--end', type=str, help='end time')
    parser_a.add_argument('--output', type=str, help='output file name')
    parser_a.add_argument('--format', type=str, help='output format')
    parser_a.set_defaults(func=export)


    p_search = subparsers.add_parser('search', help='search for PV names or patterns')
    p_search.add_argument('pattern', type=str, help='search pattern', nargs='+')
    p_search.set_defaults(func=search)


def search(args):
    logger.info(f'Searching for {args.pattern}')

def export(argv):
    argparser = argparse.ArgumentParser(description='Export data from the archiver')
    argparser.add_argument('categories', type=str, nargs='+', help='Categories to export')


if __name__ == "__main__":
    main()