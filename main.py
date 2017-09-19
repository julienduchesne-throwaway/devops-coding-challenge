#!/usr/bin/env python3
from devops_challenge.utils import arg_parser, statistics_printer
from devops_challenge.s3.bucket_lister import BucketLister
from devops_challenge.s3.object_lister import ObjectLister
from devops_challenge.s3.statistics_calculator import StatisticsCalculator
import boto3

def main():
    args = arg_parser.parse()
    s3_client = boto3.client('s3')
    bucket_lister = BucketLister(s3_client)
    object_lister = ObjectLister(s3_client)
    statistics_calculator = StatisticsCalculator(bucket_lister, object_lister)
    stats = statistics_calculator.calculate_statistics(args)


    statistics_printer.print_stats(stats, args)

if __name__ == "__main__":
    main()
