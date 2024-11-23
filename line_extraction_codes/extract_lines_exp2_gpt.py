import json
import re
import time

import pandas as pd

# Load the CSV file
input_csv = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp2.csv'
df = pd.read_csv(input_csv)
# print(df,df.columns)
# df=df.dropna(axis=1)
# print(df,df.columns)
filenames=[]

output_data = []  # List to store the reformatted data
for i, row in df.iterrows():
    vulnerabilities=[]
    ccwe=[]
    linee=[]

    filename = row['filename']
    #output_data.append({filename})
    for item in row: 
        item = str(item)
        if 'nan' in item: # Skip nan values
            continue
        if '.py' in item:  # Skip filenames
            continue
        cwe = re.search(r"CWE-\d+", item) 
        line = re.search(r' "\d+"', item) 
        
        if cwe:
            ccwe.append(cwe.group())
        if line:
            linee.append(line.group().strip('" '))

    # Combine line numbers and CWEs into the required format
    while ccwe and linee:
        vulnerabilities.append(f"{linee.pop(0)}({ccwe.pop(0)})")

    # Append the filename and combined vulnerabilities to the output
    output_data.append({
        "filename": filename,
        "vulnerability": ", ".join(vulnerabilities)  # Join with commas between entries
    })

        
        

        # if cwe and line:
           
        #     output_data.append([filename, f"{line_number}({cwe_label})"]) # Format as requested.

        
print("results: ",output_data)



output_df = pd.DataFrame(output_data)

# Save the new DataFrame to a CSV
output_csv = '/Users/ossam/OneDrive/Desktop/Data_mining_project/gpt_output2_exp2_file.csv'
output_df.to_csv(output_csv, index=False)



# output_df = pd.DataFrame(output_data, columns=['filename', 'vulnerability'])  # Create a DataFrame
# print(output_df)

# Save the new DataFrame with the extracted CWE-line pairs to a new CSV
# output_csv = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/output2_exp2_file.csv'
# df.to_csv(output_csv, index=False)

