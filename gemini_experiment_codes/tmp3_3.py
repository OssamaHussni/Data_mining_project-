#working version for experiment 3
import os
import re
import time
import google.generativeai as genai
import pandas as pd
from google.generativeai.types import HarmBlockThreshold, HarmCategory

api_key = "AIzaSyAFqK7Q_e-zardNzW_yr0eRNuZD3oLiiYY"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002",generation_config={
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    },
    safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
})
gemini_api_key = api_key

#df=pd.read_excel(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\PyTy1_final_labels.xlsx')
#directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/labeled_files'


#pyty1
# df=pd.read_excel(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\PyTy1_final_labels.xlsx')
# directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/labeled_files'

#pyty2
#df=pd.read_excel(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT2\PyTy2_final_labels.xlsx')
#directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT2/labeled_files'
#seddiq
df=pd.read_excel(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\Siddiq\siddiq_final_labels.xlsx')
directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/Siddiq/labeled_files'



gemini_response_list=[]

df['Bandit'] = df['Bandit'].astype(str)

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))


for index, row in df.iterrows():
    filename = str(row['Filename'])
    banditLabels = str(row['Bandit'])
    semgrepLabels=str(row['Semgrep'])
    sonarLabels=str(row['Mr. Chekideh'])
    labels=",".join([banditLabels,semgrepLabels,sonarLabels]).replace(',nan','').replace('nan,','')
    print(filename)
    #print(labels)
    #extracting only CWE-x from tools labels
    labelsList=labels.split(',')
    listOfLabels=[]
    for i in labelsList:
        if labels != 'nan':
            res=re.search(r'\(.*\)',i)
            value=res.group(0)
            if value not in listOfLabels:
                listOfLabels.append(value)
    #print(listOfLabels)
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

            list of vulnerabilities: {", ".join(listOfLabels)}

            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each element.
            only answer with JSON.
            """
            response = model.generate_content(prompt)
            gemini_response_list.append(response.text)
            #print(response.text)
            time.sleep(10)
#print(gemini_response_list)
df['gemini_perClass_response']=gemini_response_list
print ('dataframe: ',df['gemini_perClass_response'])

#with pd.ExcelWriter(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\test_exp3_PyTy1_final_labels.xlsx',engine='openpyxl') as writer:
                #df.to_excel(writer, sheet_name='Bakhshandeh')


#with pd.ExcelWriter(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\test_exp3_PyTy2_final_labels.xlsx',engine='openpyxl') as writer:
                #df.to_excel(writer, sheet_name='Bakhshandeh')

with pd.ExcelWriter(rf'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\test_exp3_siddiq_final_labels.xlsx',engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Bakhshandeh')