import unittest
import os
from hfpkg.src.calculations import calculate_sma, calculate_rsi
from hfpkg.src.files import read_csv, write_to_csv

class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.test_file_path = 'test_file.csv'
        with open(self.test_file_path, 'w') as temp_file:
            temp_file.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
            temp_file.write("2000-01-03,31.15625,31.296875,27.90625,29.53125,24.201658248901367,98114800\n")
            temp_file.write("2000-01-04,28.875,29.65625,26.25,26.921875,22.063207626342773,116824800\n")
            temp_file.write("2000-01-05,25.40625,26.59375,24.0,25.5,20.89794921875,166054000\n")
            temp_file.write("2000-01-06,25.0390625,26.25,23.671875,24.0,19.668651580810547,109880000\n")
            temp_file.write("2000-01-07,23.75,25.875,23.390625,25.84375,21.179662704467773,91755600\n")
            temp_file.write("2000-01-10,27.0,29.0,26.375,28.9375,23.715070724487305,91518000\n")
            temp_file.write("2000-01-11,28.15625,28.6875,27.375,28.09375,23.023597717285156,86585200\n")
            temp_file.write("2000-01-12,28.0625,28.0625,25.921875,26.40625,21.64063835144043,83443600\n")
            temp_file.write("2000-01-13,27.125,27.46875,25.875,26.265625,21.52539825439453,55779200\n")
            temp_file.write("2000-01-14,27.25,27.84375,26.1875,26.703125,21.883939743041992,57078000\n")
            temp_file.write("2000-01-18,26.96875,28.625,26.40625,27.8125,22.79309844970703,66780000\n")
            temp_file.write("2000-01-19,28.0625,29.125,27.0,28.5625,23.407747268676758,49198400\n")
            temp_file.write("2000-01-20,29.5,30.125,29.0625,29.625,24.278501510620117,54526800\n")
            temp_file.write("2000-01-21,30.75,30.75,29.5,29.84375,24.457767486572266,50891000\n")
            temp_file.write("2000-01-24,30.125,30.1875,27.0,27.09375,22.204072952270508,50022400\n")
            temp_file.write("2000-01-25,27.53125,28.75,27.4375,28.21875,23.126033782958984,53059200\n")
            temp_file.write("2000-01-26,28.375,29.46875,27.5,27.53125,22.562612533569336,47569200\n")
            temp_file.write("2000-01-27,27.90625,28.34375,25.0,25.90625,21.230876922607422,61054000\n")
            temp_file.write("2000-01-28,25.75,25.96875,23.3125,23.6875,19.41255760192871,86394000\n")
            temp_file.write("2000-01-31,23.96875,25.0625,23.53125,24.9765625,20.468976974487305,68148000\n")

    def tearDown(self):
        os.remove(self.test_file_path)
   
    def test_calculate_sma(self):
        expected_sma = [26.359375, 26.240625, 26.475, 26.65625, 27.109375, 27.28125, 27.05625,
                        27.15, 27.79375, 28.509375, 28.5875, 28.66875, 28.4625, 27.71875, 26.4875, 26.0640625]
        close_prices = read_csv(self.test_file_path)
        actual_sma = calculate_sma(close_prices, value=5)
        self.assertEqual(actual_sma, expected_sma)


    def test_calculate_rsi(self):
        expected_rsi = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.050847457627114, 2.990797546012274, 
                        2.848101265822791, 2.661388665308138, 6.496655915057545]
        close_prices = read_csv(self.test_file_path)
        actual_rsi = calculate_rsi(close_prices, value=14)
        self.assertEqual(actual_rsi, expected_rsi)
        

if __name__ == '__main__':
    unittest.main()