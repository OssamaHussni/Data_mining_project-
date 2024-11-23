import pandas as pd
import os


excel_file = "/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp_4_gpt_result_withoutclass.txt" # Replace with the actual path to your Excel file.
code_directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/all_data_sets'  # Replace with the directory containing your code files.
output_file = '/Users/ossam/OneDrive/Desktop/Data_mining_project/exp4_output.csv'


df = pd.read_csv(excel_file,on_bad_lines='warn', engine='python')  # No sheet_name if it's the first sheet.

df['extracted_lines'] = ""  # Create a new column for the results

def clean_line(line):
    return line.strip().strip('\'"') 

for index, row in df.iterrows():
    filename = row['filename']
    filepath = os.path.join(code_directory, filename)
    target_line=[]
    for col in df.columns:
        if col not in ['filename', 'extracted_lines'] and pd.notna(row[col]):
            target_line.append(clean_line(str(row[col])))


    extracted_lines = []
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):  # Enumerate file lines with line numbers
                cleaned_line = clean_line(line)  # Clean each file line
                for target in target_line:
                    if target in cleaned_line:  # Check if the target exists in the cleaned file line
                        extracted_lines.append(i)
                        break
                    print(filename,target_line,i)
    df.loc[index, 'extracted_lines'] = ", ".join(map(str, extracted_lines)) # Put the output in the column at the correct row.

df.to_csv(output_file, index=False) # Save updated DataFrame to CSV
