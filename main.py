#!/usr/bin/env python3
from devops_challenge.utils import arg_parser, statistics_printer
from devops_challenge.s3.statistics_calculator import StatisticsCalculator

def main():
    args = arg_parser.parse()
    statistics_calculator = StatisticsCalculator()
    stats = statistics_calculator.calculate_statistics(args)


    statistics_printer.print_stats(stats, args)

if __name__ == "__main__":
    main()
