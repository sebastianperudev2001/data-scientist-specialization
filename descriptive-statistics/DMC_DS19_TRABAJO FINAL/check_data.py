
import pandas as pd

def check_data_quality(file_name, variables):
    try:
        # Read a sample or full. File is small enough (6MB), but let's read all to be sure.
        df = pd.read_excel(file_name, sheet_name=0) # Data sheet presumed first
        
        print("Data Shape:", df.shape)
        
        for var in variables:
            if var in df.columns:
                print(f"\n--- {var} ---")
                print("Missing:", df[var].isnull().sum())
                print("Unique values:", df[var].nunique())
                if df[var].dtype == 'object' or df[var].nunique() < 20:
                    print("Value Counts:\n", df[var].value_counts().head())
                else:
                    print("Describe:\n", df[var].describe())
            else:
                print(f"\n--- {var} NOT FOUND in Data Sheet ---")

    except Exception as e:
        print(f"Error: {e}")

vars_to_check = ['P208A', 'P207', 'P301A', 'P401', 'P4191', 'NIVEL']

if __name__ == "__main__":
    check_data_quality('data.xlsx', vars_to_check)
