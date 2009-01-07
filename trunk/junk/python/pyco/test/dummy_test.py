from unittest import TestCase

# The module I'm testing
from dummy import foo, bar, baz

class TestDummyTestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_foo(self):
        self.assertEquals(foo(), 'foo')

    def test_bar(self):
        self.assertEquals(bar(), 'bar')

    def test_baz_incomplete_coverage(self):
        self.assertEquals(baz(), 'baz')

    def _test_baz_good(self):
        self.assertEquals(baz(), 'baz')
        self.assertEquals(baz(None), 'baz')
        self.assertEquals(baz('quiet'), 'quiet')

