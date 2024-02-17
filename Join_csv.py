import pandas as pd

def concatenate_csv_files(file1_path, file2_path, output_file_path):

    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    concatenated_df = pd.concat([df1, df2], axis=1)
    
    concatenated_df.to_csv(output_file_path, index=False)
    
    print("CSV files concatenated successfully!")

file1_path = "wifi_data.csv"
file2_path = "location_data.csv"
output_file_path = "./Data.csv"

concatenate_csv_files(file1_path, file2_path, output_file_path)