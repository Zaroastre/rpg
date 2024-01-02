import unittest
from rpg.objects import Object, QualityType
 
class TestObject(unittest.TestCase):
    __NAME: str = "Name"
    __DESCRIPTION: str = "Description"

    def test_object_name(self):
        object_to_test: Object = Object(TestObject.__NAME, TestObject.__DESCRIPTION)
        self.assertTrue(object_to_test.name == TestObject.__NAME)
 
    def test_object_decription(self):
        object_to_test: Object = Object(TestObject.__NAME, TestObject.__DESCRIPTION)
        self.assertTrue(object_to_test.description == TestObject.__DESCRIPTION)

    def test_object_default_quality(self):
        object_to_test: Object = Object(TestObject.__NAME, TestObject.__DESCRIPTION)
        self.assertTrue(object_to_test.quality == QualityType.POOR)

    def test_object_custom_quality(self):
        object_to_test: Object = Object(TestObject.__NAME, TestObject.__DESCRIPTION, QualityType.LEGENDARY)
        self.assertTrue(object_to_test.quality == QualityType.LEGENDARY)
 
if __name__ == '__main__':
    unittest.main()
