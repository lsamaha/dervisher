__author__ = 'lsamaha'

import unittest2 as unittest
from dervisher.stream import Stream
from dervisher.stream import StreamTimeoutException
from boto.kinesis.exceptions import ResourceNotFoundException


class StreamTest(unittest.TestCase):

    """
    Demonstrate stream is created if it does not exist.
    """
    def test_create(self):
        name = 'mystream'
        shards = 2
        conn = MockConn(waits_till_active=1)
        stream = Stream(conn=conn, stream_name=name, shard_count=shards)
        self.assertEquals(1, conn.create_stream_count)
        self.assertTrue(conn.describe_stream_count > 1)
        stream.put(key='a', data='b')
        self.assertEquals(1, conn.put_count)
        self.assertEquals(name, conn.put_stream_name)
        self.assertEquals('a', conn.put_partition_key)
        self.assertEquals('b', conn.put_data)

    """
    Stream create status at timeout effects stream creation.
    """
    def test_timeout(self):
        name = 'mystream'
        shards = 2
        conn = MockConn(waits_till_active=10)
        thrown = None
        try:
            stream = Stream(conn=conn, stream_name=name, shard_count=shards, timeout=0, retry_pause=0)
            self.assertFalse('Stream creation should timeout since mock is not ready on first attempt', True)
        except StreamTimeoutException as e:
            thrown = e
            pass
        self.assertIsNotNone(thrown)
        stream = Stream(conn=conn, stream_name=name, shard_count=shards, timeout=-1, retry_pause=0)
        self.assertIsNotNone(stream)
        self.assertEquals(10, conn.describe_stream_count)
        self.assertTrue(stream.ready())

    """
    Demonstrate data is put on the stream.
    """
    def test_put(self):
        name = 'mystream'
        shards = 1
        conn = MockConn(0)
        stream = Stream(conn=conn, stream_name=name, shard_count=shards, timeout=0, retry_pause=0)
        stream.put(key='a', data='b')
        self.assertEquals(1, conn.put_count)
        self.assertEquals(name, conn.put_stream_name)
        self.assertEquals('a', conn.put_partition_key)
        self.assertEquals('b', conn.put_data)

class MockConn(object):
    waits_till_active = None
    describe_stream_count = 0
    create_stream_count = 0
    put_stream_name = None
    put_partition_key = None
    put_data = None
    put_count = 0
    def __init__(self, waits_till_active = 1):
        self.waits_till_active = waits_till_active
    def create_stream(self, stream_name, shard_count):
        self.create_stream_count += 1
    def put_record(self, stream_name, data, partition_key):
        self.put_count += 1
        self.put_stream_name = stream_name
        self.put_data = data
        self.put_partition_key = partition_key
    def describe_stream(self, stream_name):
        self.describe_stream_count += 1
        # simulate waiting on status change for newly created stream
        if self.describe_stream_count <= 1:
            # first call raises exception which should trigger creation
            e = ResourceNotFoundException({'description':''},{})
            raise e
        else:
            return {'StreamDescription':{'StreamStatus':'CREATING'}} if self.describe_stream_count < self.waits_till_active \
                else {'StreamDescription':{'StreamStatus':'ACTIVE'}}

if __name__ == '__main__':
    unittest.main()
