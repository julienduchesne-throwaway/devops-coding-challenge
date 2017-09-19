import re
import boto3

class BucketLister:
    s3_client = None

    def __init__(self, s3_client=None):
        self.s3_client = s3_client or boto3.client('s3')

    def list_buckets(self, expressions, regions):
        buckets = self.s3_client.list_buckets().get('Buckets')
        for bucket in buckets:
            bucket = self._fetch_bucket_region(self.s3_client, bucket)
        buckets = self._filter_by_region(buckets, regions)
        buckets = self._filter_by_expression(buckets, expressions)
        return buckets

    def _fetch_bucket_region(self, client, bucket):
        response = client.get_bucket_location(Bucket=bucket.get('Name'))
        bucket['Region'] = response.get('LocationConstraint') or 'us-east-1'
        return bucket

    def _filter_by_region(self, buckets, regions):
        if len(regions) > 0:
            buckets = [bucket for bucket in buckets
                       if bucket.get('Region') in regions]
        return buckets

    def _filter_by_expression(self, buckets, expressions):
        if len(expressions) > 0:
            i = 0
            while i < len(buckets):
                bucket = buckets[i]
                if any([re.match('^' + expression + '$', bucket.get('Name'))
                        for expression in expressions]):
                    i += 1
                else:
                    buckets.remove(bucket)
        return buckets
