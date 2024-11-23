import os
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import os
import time
import pandas as pd
import requests
import re

api_key = "AIzaSyAFqK7Q_e-zardNzW_yr0eRNuZD3oLiiYY"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Write a paragraph about climate change.")
# print(response.text)
# Replace with your Gemini API key
gemini_api_key = api_key  



#df=pd.read_excel(rf'/Users/ossam/OneDrive/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/labels.xlsx')
df_try= pd.read_excel(r'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\labels.xlsx')
df = pd.read_excel(r'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\labels.xlsx',sheet_name=None)
df_bandit = pd.read_excel(r'C:\Users\ossam\OneDrive\Desktop\Data_mining_project\ChatGPTasSAST-main\Data sets\PyT1\labels.xlsx',sheet_name='bandit')
#print("evuwekcjqncioneviowv",df)

for i in df:
    print(i)
directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/labeled_files'

gemini_response_list=[]
#print("columnsssssssss::::::::::::::::",df.columns)
#print(df['bandit'])

df_bandit['label'] = df_bandit['label'].astype(str)

df_bandit['label'] = df_bandit['label'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df_bandit['label'] = df_bandit['label'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))

print(df_bandit)
filename = str(df['bandit']['Filename'])


banditLabels = str(df_bandit['label'])
semgrepLabels=str(df['semgrep']['Vulline'])
sonarLabels=str(df['sonarqube']['Vulline'])
labels=",".join([banditLabels,semgrepLabels,sonarLabels]).replace(',nan','').replace('nan,','')  
print(filename)    
print("LABELSSSS:  ",labels,"DONEEEEEEEEEEEEEEEE")
#extracting only CWE-x from tools labels  
labelsList=labels.split(',')
listOfLabels=[]
for i in labelsList:
    print("Labels list:  = ",i)
    if i!=None:
        res=re.search(r'\(.*\)',i)
        if res:
            value=res.group(0)
            if value not in listOfLabels:
                listOfLabels.append(value)
print("List of labels:    ",listOfLabels)
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

        response = model.generate_content(prompt,safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
})            
        gemini_response_list.append(response.text) 
        print(response)
        time.sleep(20)
print(gemini_response_list)  
df['gemini_perClass_response']=gemini_response_list
with pd.ExcelWriter('/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/PyT1/geminilables.xlsx') as writer:  
                df_try.to_excel(writer, sheet_name='Bakhshandeh')

















