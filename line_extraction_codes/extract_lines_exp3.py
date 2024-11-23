import re
import pandas as pd

# Input and output file paths
input_excel = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp3_PyTy2_final_labels.xlsx'
output_csv = '/Users/ossam/OneDrive/Desktop/Data_mining_project/pyty2_output_exp3_file.csv'

# Load the Excel file
df = pd.read_excel(input_excel)

# List to store the reformatted data
output_data = []

# Iterate over each row
for i, row in df.iterrows():
    vulnerabilities = []

    # Extract filename
    filename = row['Filename']

    # Extract and process the gemini response column
    raw = row['gemini_perClass_response']
    raw = str(raw)
    check=re.search(r"CWE-\d+", raw)

    if 'nan' in raw or not raw.strip() or check==None:  # Handle rows with invalid or empty data
        vulnerabilities.append("None")
    else:
        # Use regular expressions to extract line numbers and CWEs
        lines = re.findall(r'"(\d+)"', raw)  # Extract line numbers (e.g., "14")
        cwes = re.findall(r'CWE-\d+', raw)  # Extract CWE IDs (e.g., CWE-78)

        # Combine line numbers and CWEs into the desired format
        while lines and cwes:
            vulnerabilities.append(f"{lines.pop(0)}({cwes.pop(0)})")

    # Add the extracted data to the output
    output_data.append({
        "filename": filename,
        "vulnerability": ", ".join(vulnerabilities)  # Join all pairs with commas
    })

# Convert the output data into a DataFrame
output_df = pd.DataFrame(output_data)

# Save the DataFrame to a CSV file
output_df.to_csv(output_csv, index=False)

print("Data successfully processed and saved to:", output_csv)
