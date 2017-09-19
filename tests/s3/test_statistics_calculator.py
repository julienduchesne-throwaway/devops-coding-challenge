import unittest
from datetime import datetime, timedelta
from devops_challenge.s3.statistics_calculator import StatisticsCalculator
from mock import Mock


class StatisticsCalculatorTest(unittest.TestCase):
    STANDARD_TYPE = 'STANDARD'
    INFREQUENT_ACCESS_TYPE = 'STANDARD_IA'
    bucket_lister = Mock()
    object_lister = Mock()
    args = Mock()
    statistics_calculator = StatisticsCalculator(bucket_lister, object_lister)

    def setUp(self):
        self._setup_tests()

    def test_can_calculate_total_statistics(self):
        self.args.groups = ['TOTAL']

        stats = self.statistics_calculator.calculate_statistics(self.args)

        total_stats = stats['TOTAL'][0]
        self.assertEqual(datetime.now().date(), total_stats['Last modified'].date())
        self.assertEqual(5, total_stats['Average size'])
        self.assertEqual(20, total_stats['Total size'])
        self.assertEqual(4, total_stats['Number of files'])

    def test_can_calculate_statistics_by_region(self):
        self.args.groups = ['BY_REGION']

        stats = self.statistics_calculator.calculate_statistics(self.args)

        region_stats = next(stat for stat in stats['BY_REGION'] if stat['Region name'] == 'us-east-1')
        self.assertEqual(datetime.now().date(), region_stats['Last modified'].date())
        self.assertEqual(17/3, region_stats['Average size'])
        self.assertEqual(17, region_stats['Total size'])
        self.assertEqual(3, region_stats['Number of files'])

    def test_can_calculate_statistics_by_bucket(self):
        self.args.groups = ['BY_BUCKET']

        stats = self.statistics_calculator.calculate_statistics(self.args)

        bucket_stats = next(stat for stat in stats['BY_BUCKET'] if stat['Bucket name'] == 'Bucket2')
        self.assertEqual(datetime.now().date(), bucket_stats['Last modified'].date())
        self.assertEqual((datetime.now() - timedelta(days=365)).date(),
                         bucket_stats['Bucket creation date'].date())
        self.assertEqual(8, bucket_stats['Average size'])
        self.assertEqual(16, bucket_stats['Total size'])
        self.assertEqual(2, bucket_stats['Number of files'])

    def test_can_calculate_size_share(self):
        self.args.groups = ['BY_BUCKET']
        stats = self.statistics_calculator.calculate_statistics(self.args)
        bucket_stats = next(stat for stat in stats['BY_BUCKET'] if stat['Bucket name'] == 'Bucket2')
        self.assertEqual('80.00%', bucket_stats['Size share'])

        self.args.groups = ['BY_REGION']
        stats = self.statistics_calculator.calculate_statistics(self.args)
        bucket_stats = next(stat for stat in stats['BY_REGION'] if stat['Region name'] == 'us-west-1')
        self.assertEqual('15.00%', bucket_stats['Size share'])


    def _setup_tests(self):
        object1 = {'Region': 'us-east-1', 'BucketName': 'Bucket1', 'Size': 1,
                   'StorageClass': self.INFREQUENT_ACCESS_TYPE, 'LastModified': datetime.now()}
        object2 = {'Region': 'us-east-1', 'BucketName': 'Bucket2', 'Size': 8,
                   'StorageClass': self.INFREQUENT_ACCESS_TYPE, 'LastModified': datetime.now()}
        object3 = {'Region': 'us-east-1', 'BucketName': 'Bucket2', 'Size': 8,
                   'StorageClass': self.STANDARD_TYPE, 'LastModified': datetime.now() - timedelta(days=365)}
        object4 = {'Region': 'us-west-1', 'BucketName': 'Bucket3', 'Size': 3,
                   'StorageClass': self.STANDARD_TYPE, 'LastModified': datetime.now() - timedelta(days=365)}
        bucket1 = {'Name': 'Bucket1', 'CreationDate': datetime.now()}
        bucket2 = {'Name': 'Bucket2', 'CreationDate': datetime.now() - timedelta(days=365)}
        bucket3 = {'Name': 'Bucket3', 'CreationDate': datetime.now() - timedelta(days=365)}
        self.bucket_lister.list_buckets = Mock(return_value=[bucket1, bucket2, bucket3])
        self.object_lister.list_objects = Mock(return_value=[object1, object2, object3, object4])
