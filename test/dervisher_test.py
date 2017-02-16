__author__ = 'lsamaha'

import unittest2 as unittest
from dervisher.dervisher import Dervisher


class DervisherTest(unittest.TestCase):

    """
    Show what dervishers can do.
    """
    def test_start(self):
        post = MockPost()
        d = Dervisher(name='fifi', post=post)
        d.start(30)
        self.assertEquals(1, post.event_count)
        self.assertEquals('start', post.last_event.event_class)
        self.assertEquals('service', post.last_event.event_type)
        d.stop()
        self.assertEquals(2, post.event_count)
        self.assertEquals('stop', post.last_event.event_class)
        self.assertEquals('service', post.last_event.event_type)

class MockPost(object):

    event_count = 0
    last_event = None

    def event(self, event):
        self.last_event = event
        self.event_count += 1

if __name__ == '__main__':
    unittest.main()
