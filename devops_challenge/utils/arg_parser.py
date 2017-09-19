import argparse
from .constants import *

def parse():
    parser = argparse.ArgumentParser(description='Analyze S3 files')
    parser.add_argument('--unit', '-u', type=str, default=KILOBYTES,
                        help='Size unit (default: KB)',
                        choices=[BYTES, KILOBYTES, MEGABYTES, GIGABYTES, TERABYTES])
    parser.add_argument('--regions', '-r', type=str, nargs='+', default='',
                        help='List of regions to fetch (default: all)')
    parser.add_argument('--storage-types', '-t', type=str, nargs='+', default='',
                        help='List of storage types to fetch (default: all)',
                        choices=[STANDARD, INFREQUENT_ACCESS, REDUCED_REDUNDANCY])
    parser.add_argument('--buckets', '-b', type=str, nargs='+', default='',
                        help='List of buckets to fetch, accepts regex (default: all)')
    parser.add_argument('--key-prefix', '-p', type=str, default='',
                        help='Object prefix (default: none)')
    parser.add_argument('--groups', '-g', type=str, nargs='+',
                        default=[TOTAL, BY_BUCKET, BY_REGION, BY_STORAGE_TYPE],
                        help='Groups to calculate stats for (default: all)',
                        choices=[TOTAL, BY_BUCKET, BY_REGION, BY_STORAGE_TYPE])
    parser.add_argument('--return-format', '-rf', type=str, default=JSON,
                        help='JSON, TABLE or CSV (default: JSON)',
                        choices=[JSON, CSV, TABLE])

    return parser.parse_args()
