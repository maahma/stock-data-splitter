import pandas as pd
from pathlib import Path
import os

def split_by_country(input_csv_file, output_folder):
 
    df = pd.read_csv(input_csv_file, encoding="iso-8859-1")  

    # convert output folder into Path and make sure it exists
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # get the branch column 
    branch_col = df.columns[0]

    # get rows where branch is empty and save it as sample stock
    sample_stock = df[df[branch_col].isnull() | (df[branch_col] == '')]
    # print("Number of sample_stock cols: ", sample_stock.shape[0])

    # save empty rows to "sample_stock.csv"
    sample_stock.to_csv(output_folder / "sample_stock.csv", index=False)

    # get rows with valid branch only i.e. branch isn't empty
    valid_rows = df[~df[branch_col].isnull() & (df[branch_col] != '')]

    # group valid rows by the branch
    groups = valid_rows.groupby(branch_col)
    # print(groups.first())

    # size_branch = groups.size()  # number of entries for each branch 
    # print(size_branch)  

    # save each group to separate CSV file
    for group_name, group_df in groups:
        output_file = output_folder/f"{group_name}.csv"
        group_df.to_csv(output_file, index=False)


    # encodings = ["utf-8","utf-8-sig", "iso-8859-1", "latin1", "cp1252"]
    # for encoding in encodings:
    #     try:
    #         dataframe = pd.read_csv(input_csv_file,encoding=encoding)
    #         print(encoding)
    #         break
    #     except Exception as e:  
    #         pass
    
def main():
    split_by_country("ecom-inventory.csv", "output_csv")

if __name__ == "__main__":
    main()