import boto3

class ObjectLister:
    s3_client = None

    def __init__(self, s3_client=None):
        self.s3_client = s3_client or boto3.client('s3')

    def list_objects(self, buckets, prefix, types):
        objects = []
        for bucket in buckets:
            objects += self._list_objects_by_bucket(self.s3_client, bucket, prefix)
        if len(types):
            objects = self._filter_objects_by_storage_type(objects, types)
        return objects

    def _list_objects_by_bucket(self, client, bucket, prefix):
        objects = []
        response = client.list_objects_v2(
            Bucket=bucket.get('Name'),
            Prefix=prefix,
        )
        if 'Contents' in response:
            objects += response.get('Contents')
        while response.get('IsTruncated'):
            response = client.list_objects_v2(
                Bucket=bucket.get('Name'),
                Prefix=prefix,
                ContinuationToken=response.get('NextContinuationToken')
            )
            if 'Contents' in response:
                objects += response.get('Contents')
        for obj in objects:
            obj['BucketName'] = bucket.get('Name')
            obj['Region'] = bucket.get('Region')
        return objects

    def _filter_objects_by_storage_type(self, objects, storage_types):
        return [obj for obj in objects if obj.get('StorageClass') in storage_types]
