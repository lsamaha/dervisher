__author__ = 'lsamaha'

import unittest2 as unittest
import json
from dervisher.event import Event


class EventTest(unittest.TestCase):
    """
    Show what our events are made of.
    """

    def test_json(self):
        e = Event(event_class='start', event_type='service', subtype='mimi', product='foo', env='dev', pretty=True)
        data = e.tojson()
        e2 = json.loads(data)
        self.assertIsNotNone(e2)
        self.assertEquals(e.__dict__['event_class'], e2['event_class'])
        self.assertEquals(e.__dict__['event_type'], e2['event_type'])
        self.assertEquals(e.__dict__['subtype'], e2['subtype'])
        self.assertEquals(e.__dict__['product'], e2['product'])
        self.assertEquals(e.__dict__['env'], e2['env'])

if __name__ == '__main__':
    unittest.main()