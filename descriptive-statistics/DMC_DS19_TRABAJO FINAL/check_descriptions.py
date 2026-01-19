
import pandas as pd

def get_descriptions(file_name, sheet_name, variables):
    try:
        df_dic = pd.read_excel(file_name, sheet_name=sheet_name)
        print("Columns found:", df_dic.columns.tolist())
        
        # Normalize columns if needed (strip spaces)
        df_dic.columns = df_dic.columns.str.strip()
        
        # Check again
        if 'DESCRIPCIÓN' in df_dic.columns:
            subset = df_dic[df_dic['VARIABLE'].isin(variables)]
            print(subset[['VARIABLE', 'DESCRIPCIÓN']])
        else:
            print("Still can't find 'DESCRIPCIÓN' column.")
            # Print head to see what's there
            print(df_dic.head())
        
    except Exception as e:
        print(f"Error: {e}")

vars_to_check = ['P208A', 'P207', 'P208B', 'P209', 'P301A', 'P401', 'P4191', 'NIVEL', 'TIEMPO_PAUSA_FELICIDAD'] # The last one is just a check

if __name__ == "__main__":
    get_descriptions('data.xlsx', 'Diccionario Enaho 400', vars_to_check)
