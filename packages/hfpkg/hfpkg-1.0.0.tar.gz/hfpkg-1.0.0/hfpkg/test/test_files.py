import unittest
import os
from hfpkg.src.files import read_csv, write_to_csv

class TestFileHandling(unittest.TestCase):
    def setUp(self):
        self.test_file_path = 'test_file.csv'
        with open(self.test_file_path, 'w') as temp_file:
            temp_file.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
            temp_file.write("2000-01-03,31.15625,31.296875,27.90625,29.53125,24.201658248901367,98114800\n")
            temp_file.write("2000-01-04,28.875,29.65625,26.25,26.921875,22.063207626342773,116824800\n")
            temp_file.write("2000-01-05,25.40625,26.59375,24.0,25.5,20.89794921875,166054000\n")
            temp_file.write("2000-01-06,25.0390625,26.25,23.671875,24.0,19.668651580810547,109880000\n")
            temp_file.write("2000-01-07,23.75,25.875,23.390625,25.84375,21.179662704467773,91755600\n")

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_read_csv(self):
        data = read_csv(self.test_file_path)
        expected_data = [29.53125, 26.921875, 25.5, 24.0, 25.84375]
        self.assertEqual(data, expected_data)

    def test_write_to_csv(self):
        test_data = [1.234, 5.678, 9.012]
        output_file_path = 'output_test_file.csv'
        write_to_csv(test_data, output_file_path)

        with open(output_file_path, 'r') as output_file:
            written_data = output_file.readlines()

        expected_written_data = ["1.234000\n", "5.678000\n", "9.012000\n"]
        self.assertEqual(written_data, expected_written_data)

        os.remove(output_file_path)

if __name__ == '__main__':
    unittest.main()
