from . import constants
from tabulate import tabulate

def print_stats(stats, args):
    for key in stats:
        for elem in stats[key]:
            elem = _format_size_fields(elem, args.unit)
            elem = _format_date_fields(elem)
    if args.return_format == constants.JSON:
        _print_as_json(stats)
    elif args.return_format == constants.TABLE:
        _print_as_table(stats)
    elif args.return_format == constants.CSV:
        _print_as_csv(stats)

def _print_as_json(stats):
    for group in stats:
        stats[group] = [dict(elem) for elem in stats[group]]
    print(stats)

def _print_as_table(stats):
    for group in stats:
        print(group)
        values = []
        headers = [header for header in stats[group][0].keys()]
        for elem in stats[group]:
            values.append([value for value in elem.values()])
        print(tabulate(values, headers, tablefmt="grid"))
        print('\n')

def _print_as_csv(stats):
    for group in stats:
        print(group)
        print(','.join(stats[group][0].keys()))
        for elem in stats[group]:
            print(','.join([str(value) for value in elem.values()]))
        print('\n')

DATE_FIELDS_TO_FORMAT = ['Last modified', 'Bucket creation date']
def _format_date_fields(elem):
    for field in [field for field in DATE_FIELDS_TO_FORMAT if field in elem]:
        elem[field] = elem[field].strftime('%d/%m/%y %H:%M:%S')
    return elem

SIZE_FIELDS_TO_FORMAT = ['Total size', 'Average size']
def _format_size_fields(elem, unit):
    for field in [field for field in SIZE_FIELDS_TO_FORMAT if field in elem]:
        elem[field] = _format_size(elem[field], unit)
    return elem

SIZE_MULTIPLIER = {
    "B": 1024**0,
    "KB": 1024**1,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4
}
def _format_size(size, unit):
    if unit == 'B':
        return str(size) + 'B'
    else:
        return "{:.2f}".format(size / SIZE_MULTIPLIER[unit]) + unit
