#read data from the CSV file
def read_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    #extract relevant data from the CSV file
    data_lines = [line.strip().split(',') for line in lines[1:]]  #skip header line
    close_prices = [float(line[4]) for line in data_lines]  #extract 'Close' prices
    return close_prices 

#write results to CSV files
def write_to_csv(data, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for row in data:
            output_file.write(f"{row:.6f}\n") #write each value to the file
