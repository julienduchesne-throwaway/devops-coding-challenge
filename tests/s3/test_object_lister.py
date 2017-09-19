import unittest
import boto3
from devops_challenge.s3.object_lister import ObjectLister
from moto import mock_s3

class ObjectListerTest(unittest.TestCase):
    BUCKET1 = 'BUCKET1'
    OBJECT1 = 'OBJECT1'
    OBJECT2 = 'OBJECT2'
    MAX_OBJECTS_PER_QUERY = 1000
    STANDARD_TYPE = 'STANDARD'
    INFREQUENT_ACCESS_TYPE = 'STANDARD_IA'
    object_lister = ObjectLister(boto3.client('s3'))

    @mock_s3
    def test_can_get_objects(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        client.put_object(Bucket=self.BUCKET1, Key=self.OBJECT1)
        client.put_object(Bucket=self.BUCKET1, Key=self.OBJECT2)

        buckets = [{'Name': self.BUCKET1, 'Region': 'us-east-1'}]
        objects = self.object_lister.list_objects(buckets, '', [])

        self.assertEqual(2, len(objects))
        self.assertEqual(1, len([obj for obj in objects if obj['Key'] == self.OBJECT1]))
        self.assertEqual(1, len([obj for obj in objects if obj['Key'] == self.OBJECT2]))

    @mock_s3
    def test_can_get_lots_of_objects(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        for i in range(0, self.MAX_OBJECTS_PER_QUERY + 1):
            client.put_object(Bucket=self.BUCKET1, Key=str(i))

        buckets = [{'Name': self.BUCKET1, 'Region': 'us-east-1'}]
        objects = self.object_lister.list_objects(buckets, '', [])

        self.assertEqual(self.MAX_OBJECTS_PER_QUERY + 1, len(objects))

    @mock_s3
    def test_can_filter_objects_by_prefix(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        client.put_object(Bucket=self.BUCKET1, Key=self.OBJECT1)
        client.put_object(Bucket=self.BUCKET1, Key=self.OBJECT2)

        buckets = [{'Name': self.BUCKET1, 'Region': 'us-east-1'}]
        objects1 = self.object_lister.list_objects(buckets, 'OBJ', [])
        objects2 = self.object_lister.list_objects(buckets, 'OBJECT1', [])

        self.assertEqual(2, len(objects1))
        self.assertEqual(1, len(objects2))

    @mock_s3
    def test_can_filter_objects_by_storage_type(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket=self.BUCKET1)
        client.put_object(Bucket=self.BUCKET1, Key=self.OBJECT1, StorageClass=self.STANDARD_TYPE)
        client.put_object(Bucket=self.BUCKET1, Key=self.OBJECT2,
                          StorageClass=self.INFREQUENT_ACCESS_TYPE)

        buckets = [{'Name': self.BUCKET1, 'Region': 'us-east-1'}]
        objects1 = self.object_lister.list_objects(buckets, '', [self.STANDARD_TYPE])
        objects2 = self.object_lister.list_objects(buckets, '', [self.INFREQUENT_ACCESS_TYPE])

        self.assertEqual(1, len(objects1))
        self.assertEqual(1, len([obj for obj in objects1 if obj['Key'] == self.OBJECT1]))
        self.assertEqual(1, len(objects2))
        self.assertEqual(1, len([obj for obj in objects2 if obj['Key'] == self.OBJECT2]))
