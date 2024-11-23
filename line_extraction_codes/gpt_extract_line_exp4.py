import pandas as pd
import os
import re

# Input and output file paths
txt_file = "/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp_4_gpt_result_withoutclass.csv"
code_directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/all_data_sets'
output_file = '/Users/ossam/OneDrive/Desktop/Data_mining_project/3_exp4_output.csv'

# Read the .csv file
df = pd.read_csv(txt_file, on_bad_lines='warn', engine='python')
nums=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21']

# Create a list to store processed data
output_data = []

# Initialize the NOT FOUND counter
not_found_counter = 0

# Function to clean JSON-like strings and extract details
def extract_vulnerabilities(detected):
    vulnerabilities = []
    if pd.isna(detected) or not detected.strip():
        return vulnerabilities

    # Extract CWE labels and associated lines of code
    cwes = re.findall(r'CWE-\d+', detected)
    code_lines = re.findall(r'"line of Code":\s*["\'](.*?)["\']', str(detected))  # Extract corresponding code snippets

    # Return paired CWE and code line snippets
    return list(zip(cwes, code_lines))

# Process each row in the DataFrame
for index, row in df.iterrows():
    filename = row['filename']
    filepath = os.path.join(code_directory, filename)  # Build the full file path

    detected = str(row['detected'])
    vulnerabilities = extract_vulnerabilities(detected)

    # Prepare a list to store formatted vulnerabilities
    formatted_vulnerabilities = []

    if os.path.isfile(filepath):
        # Open the file and read its lines
        with open(filepath, 'r', encoding='utf-8') as file:
            file_lines = file.readlines()

        # Flag to check if any vulnerability was found for this file
        found_match = False

        for cwe, code_snippet in vulnerabilities:
            code_snippet=re.sub(r'[^\w\s=]', '', code_snippet)
            for line_number, line_content in enumerate(file_lines, 1):
                line_content=re.sub(r'[^\w\s=]', '', line_content)

                # Check if the code snippet exists in the current line (checking part of the line to be lenient)
                numberdata=code_snippet.replace('-','')
                if numberdata[0].isdigit():
                    print("unique case literl line: ",code_snippet)
                    formatted_vulnerabilities.append(f"{line_number}({cwe})")
                    found_match = True
                    break
                if code_snippet.strip()[:14] in line_content.strip()[:14]:  # Checking the first few characters
                    print(code_snippet,"file content: ",line_content)
                    formatted_vulnerabilities.append(f"{line_number}({cwe})")
                    found_match = True
                    break

        if not found_match:
            not_found_counter += 1  # Increment the NOT FOUND counter
            formatted_vulnerabilities.append("NOT FOUND")
    else:
        print(f"File not found: {filename}")
        formatted_vulnerabilities.append("File not found")
        not_found_counter += 1  # Increment for file not found

    # Combine the results into a single string
    output_data.append({
        "filename": filename,
        "vulnerability": ", ".join(formatted_vulnerabilities)
    })

# Convert the output data into a DataFrame
output_df = pd.DataFrame(output_data)

# Save the processed data to a CSV file
output_df.to_csv(output_file, index=False)

# Print NOT FOUND count in the terminal
print(f"Total 'NOT FOUND' vulnerabilities: {not_found_counter}")

print(f"Data successfully processed and saved to: {output_file}")
