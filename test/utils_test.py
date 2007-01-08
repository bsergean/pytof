from unittest import TestCase
import utils


class TestUtils(TestCase):
    def testRemoveSpecificChars(self):
        testCases = [
            ["test1", "test1"],
            ["test2(", "test2"]]
        for case in testCases:
            self.assertEquals(case[1], utils.RemoveSpecificChars(case[0]))
