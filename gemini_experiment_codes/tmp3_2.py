import os
import time
import pandas as pd
import re
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

api_key = "AIzaSyAFqK7Q_e-zardNzW_yr0eRNuZD3oLiiYY"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
gemini_api_key = api_key  
gemini_response_list=[]

	
#df = pd.read_excel(r'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\labels.xlsx')
df = r'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\labels.xlsx'
directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/Labeled_files'

df_bandit = pd.read_excel(df, sheet_name='bandit')
df_semgrep = pd.read_excel(df, sheet_name='semgrep')
df_sonarqube = pd.read_excel(df, sheet_name='sonarqube') 
# Sort all DataFrames by 'Filename'
df_bandit = df_bandit.sort_values('Filename').reset_index(drop=True)
df_semgrep = df_semgrep.sort_values('Filename').reset_index(drop=True)
df_sonarqube = df_sonarqube.sort_values('Filename').reset_index(drop=True)

gpt_response_list=[]



df_bandit['label'] = df_bandit['label'].astype(str)
df_bandit['label'] = df_bandit['label'].str.replace(r'\b0+(\d+)\b', r'\1', regex=True)
df_bandit['label'] = df_bandit['label'].str.replace(r'(CWE-\d+)-0+(\d+)', r'\1-\2', regex=True)


for index, row in df_bandit.iterrows():  # Iterate through bandit DataFrame
    filename = str(row['Filename'])

    bandit_label = df_bandit.loc[df_bandit['Filename'] == filename, 'label'].iloc[0]
    semgrep_labels = df_semgrep.loc[df_semgrep['Filename'] == filename, 'Vulline']
    semgrep_label = pd.Series(semgrep_labels.values) # or use .to_series()



    sonar_labels = df_sonarqube.loc[df_sonarqube['Filename'] == filename, 'Vulline']
    sonar_label = pd.Series(sonar_labels.values)


    all_labels = pd.concat([pd.Series([bandit_label]), semgrep_label, sonar_label], ignore_index=True)


    all_labels = all_labels.astype(str)

    # Cleaning the labels (inlined from the previous function)
    #MIGHT NOT BE NECCESSARY!
    #all_labels = all_labels.str.replace(r'\b0+(\d+)\b', r'\1', regex=True)
    #all_labels = all_labels.str.replace(r'(CWE-\d+)-0+(\d+)', r'\1-\2', regex=True)

    list_of_labels = []
    for label in all_labels:
            if pd.notna(label): # Correctly checks for NaN values in strings/numeric types
                matches = re.findall(r'CWE-\d+', label) # Find ALL CWE matches in the string!
                for match in matches: # Add each match to the list.
                    if match not in list_of_labels: # Still avoid duplicates
                        list_of_labels.append(match)

    print(all_labels)
    print(filename)
    print("List of Labels:", list_of_labels)
    #give the model the python file along with the labels of each python file
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        with open(f,'r') as file:
            Vul_code=file.read()         
            prompt = f"""
            which of the following vulnerabilities from list of vulnerabilities exist in the python code which
            is delimited with triple backticks. also give the line of the vulnerability in the code.

            python code: '''{Vul_code}'''

            list of vulnerabilities: {", ".join(list_of_labels)}

            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each element.
            only answer with JSON.
            """   
            response = model.generate_content(prompt,safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
    })
            gemini_response_list.append(response.text)
            print(response.text)
            time.sleep(10)
print(gemini_response_list)
#df['gpt_perClass_response']=gemini_response_list
with pd.ExcelWriter('/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/PyT1_final_labels.xlsx') as writer:
                df.to_excel(writer,sheet_name='Bakhshandeh')


