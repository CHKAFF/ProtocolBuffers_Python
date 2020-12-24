import unittest
from proto_parser import proto_parser

class proto_parser_test(unittest.TestCase):
    def setUp(self):
        self.test_data = []
        test1 = {'name' : 'test_proto_files\\test1.proto' , 'data' : proto_parser('test_proto_files\\test1.proto').parse(), 'class_count' : 2, 'properties_count' : 7, 'enum_count' : 1, 'subclass_count' : 1}
        test2 = {'name' : 'test_proto_files\\test2.proto' , 'data' : proto_parser('test_proto_files\\test2.proto').parse(), 'class_count' : 4, 'properties_count' : 7, 'enum_count' : 0, 'subclass_count' : 0}
        test3 = {'name' : 'test_proto_files\\test3.proto' , 'data' : proto_parser('test_proto_files\\test3.proto').parse(), 'class_count' : 3, 'properties_count' : 3, 'enum_count' : 0, 'subclass_count' : 3}
        test4 = {'name' : 'test_proto_files\\test4.proto' , 'data' : proto_parser('test_proto_files\\test4.proto').parse(), 'class_count' : 1, 'properties_count' : 0, 'enum_count' : 3, 'subclass_count' : 2}
        self.test_data.append(test1)
        self.test_data.append(test2)
        self.test_data.append(test3)
        self.test_data.append(test4)

    def tearDown(self):
        pass

    def test_class_count(self):
        for test in self.test_data:
            self.assertEqual(len(test['data']), test['class_count'], msg=f"Error on {test['name']}:  Wrong class count")

    def test_properties_count(self):
        for test in self.test_data:
            count = 0
            for c in test['data']:
                count += self.get_count(c, 'properties')
            self.assertEqual(count, test['properties_count'], msg=f"Error on {test['name']}:  Wrong properies count")
    
    def test_enum_count(self):
        for test in self.test_data:
            count = 0
            for c in test['data']:
                count += self.get_count(c, 'enums')
            self.assertEqual(count, test['enum_count'], msg=f"Error on {test['name']}:  Wrong enum count")

    def test_subclass_count(self):
        for test in self.test_data:
            count = 0
            for c in test['data']:
                count += self.get_count(c, "classes")
            self.assertEqual(count, test['subclass_count'], msg=f"Error on {test['name']}:  Wrong subclass count")

    def get_count(self, c, name):
        count = len(c[name])
        for subc in c['classes']:
            count += self.get_count(subc, name)
        return count


if __name__ == "__main__":
    unittest.main()