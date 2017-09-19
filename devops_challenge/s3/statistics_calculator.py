from collections import OrderedDict
from devops_challenge.utils import constants

class StatisticsCalculator:
    bucket_lister = None
    object_lister = None

    def __init__(self, bucket_lister, object_lister):
        self.bucket_lister = bucket_lister
        self.object_lister = object_lister

    def calculate_statistics(self, args):
        buckets = self.bucket_lister.list_buckets(args.buckets, args.regions)
        objects = self.object_lister.list_objects(buckets, args.key_prefix, args.storage_types)
        stats = {}
        for stat_group in args.groups:
            stats[stat_group] = []
            if stat_group == constants.TOTAL:
                stats[stat_group].append(self._create_list_group(objects, {}))
            elif stat_group == constants.BY_BUCKET:
                distinct_buckets = sorted(set([obj['BucketName'] for obj in objects]))
                for bucket_name in distinct_buckets:
                    bucket_objects = [obj for obj in objects if obj['BucketName'] == bucket_name]
                    creation_date = next(bucket for bucket in buckets
                                         if bucket['Name'] == bucket_name)['CreationDate']
                    stats[stat_group].append(self._create_list_group(bucket_objects, OrderedDict([
                        ('Bucket name', bucket_name),
                        ('Bucket creation date', creation_date)
                    ])))
            elif stat_group == constants.BY_REGION:
                distinct_regions = sorted(set([obj['Region'] for obj in objects]))
                for region in distinct_regions:
                    region_objects = [obj for obj in objects if obj['Region'] == region]
                    stats[stat_group].append(self._create_list_group(region_objects, {
                        'Region name': region
                    }))
            elif stat_group == constants.BY_STORAGE_TYPE:
                distinct_types = sorted(set([obj['StorageClass'] for obj in objects]))
                for storage_type in distinct_types:
                    type_objects = [obj for obj in objects if obj['StorageClass'] == storage_type]
                    stats[stat_group].append(self._create_list_group(type_objects, {
                        'Storage type': storage_type
                    }))
        self._calculate_size_shares(objects, stats)
        return stats

    def _create_list_group(self, objects, group_properties):
        properties = OrderedDict(group_properties)
        properties.update([
            ('Number of files', len(objects)),
            ('Average size', self._get_average_size(objects)),
            ('Total size', self._get_total_size(objects)),
            ('Last modified', self._get_last_modified(objects))
        ])
        return properties

    def _calculate_size_shares(self, objects, stats):
        total_size = float(self._get_total_size(objects))
        for group in stats:
            if group != constants.TOTAL:
                for elem in stats[group]:
                    size = float(elem['Total size'])
                    elem['Size share'] = "{:.2f}".format(size / total_size * 100) + '%'

    def _get_total_size(self, objects):
        return sum([obj['Size'] for obj in objects])

    def _get_average_size(self, objects):
        return int(self._get_total_size(objects) / len(objects))

    def _get_last_modified(self, objects):
        return max([obj['LastModified'] for obj in objects])
