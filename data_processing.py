# Tony Bui
# Software Engineering Intern at Quantium Virtual Experience Program

import pandas as pd
import glob
import re

candy_type = "pink morsel"
csv_files = glob.glob("data/*.csv")
output_file_path = "data/all_data.csv"
new_header = "sales,date,region\n"

with open(output_file_path, "w") as all_data_file:
    all_data_file.write(new_header)
    for file_name in csv_files:
        with open(file_name, 'r') as file:
            header = file.readline().strip().split(',')
            for line in file:
                product,price ,quantity ,date, region = line.strip().split(',')
                if product == candy_type:
                    quantity = int(quantity)
                    price = float(re.sub(r'\$', '', price))
                    sales = quantity * price
                    all_data_file.write(f"{sales},{date},{region}\n")
                
