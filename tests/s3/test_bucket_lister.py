import unittest
import boto3
from devops_challenge.s3.bucket_lister import BucketLister
from moto import mock_s3

class BucketListerTest(unittest.TestCase):
    BUCKET1 = 'BUCKET1'
    BUCKET2 = 'BUCKET2'
    bucket_lister = BucketLister(boto3.client('s3'))

    @mock_s3
    def test_can_get_buckets(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        client.create_bucket(Bucket=self.BUCKET2)

        buckets = self.bucket_lister.list_buckets([], [])

        self.assertEqual(2, len(buckets))
        self.assertEqual(1, len([bucket for bucket in buckets if bucket['Name'] == self.BUCKET1]))
        self.assertEqual(1, len([bucket for bucket in buckets if bucket['Name'] == self.BUCKET2]))

    @mock_s3
    def test_can_filter_buckets_by_region(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        client.create_bucket(Bucket=self.BUCKET2, CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1'
        })

        self.assertEqual(2, len(self.bucket_lister.list_buckets([], ['us-east-1', 'eu-west-1'])))
        self.assertEqual(1, len(self.bucket_lister.list_buckets([], ['us-east-1'])))
        self.assertEqual(1, len(self.bucket_lister.list_buckets([], ['eu-west-1'])))

    @mock_s3
    def test_can_filter_buckets_by_regex(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        client.create_bucket(Bucket=self.BUCKET2)

        self.assertEqual(2, len(self.bucket_lister.list_buckets(['BUCKET.*'], [])))
        self.assertEqual(1, len(self.bucket_lister.list_buckets(['BUCKET1'], [])))
        self.assertEqual(1, len(self.bucket_lister.list_buckets(['.*T2$'], [])))
