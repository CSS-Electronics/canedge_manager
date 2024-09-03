import io
from minio import Minio


class S3Client(Minio):

    # Remove bucket recursively (bucket with content)
    def remove_bucket_r(self, bucket_name):

        # Check if bucket exists
        if self.bucket_exists(bucket_name):

            # List all object paths in bucket
            objects = self.list_objects_v2(bucket_name, recursive=True)

            # Remove objects
            for obj in objects:
                self.remove_object(obj.bucket_name, obj.object_name)

            # Remove bucket
            self.remove_bucket(bucket_name)

    # Get list of objects (not iterator)
    def list_objects_as_list(self, bucket_name, prefix=""):
        return list(self.list_objects_v2(bucket_name, prefix=prefix, recursive=True))

    # Put object string
    def put_object_string(self, bucket_name, object_name, string):
        data = io.BytesIO(string.encode())
        nob = data.getbuffer().nbytes
        self.put_object(bucket_name, object_name, data, nob)
    
    pass
