import pytest
from time import sleep

from test.s3_client import S3Client
from test.s3_server import S3ServerMinio


@pytest.fixture
def bucket_name():
    return 'testbucket'

@pytest.fixture
def s3_server(tmpdir):
    server = S3ServerMinio(tmpdir)
    server.start()
    sleep(5)
    yield server
    server.stop()
    sleep(1)

@pytest.fixture
def s3_client(s3_server, bucket_name):
    client = S3Client(endpoint=s3_server.endpoint_ip + ":" + str(s3_server.port),
                      access_key=s3_server.accesskey,
                      secret_key=s3_server.secretkey,
                      secure=False)

    # Clear bucket
    client.remove_bucket_r(bucket_name=bucket_name)
    client.make_bucket(bucket_name=bucket_name)

    return client
