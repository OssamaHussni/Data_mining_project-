import os
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import time

api_key = "AIzaSyAFqK7Q_e-zardNzW_yr0eRNuZD3oLiiYY"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002",generation_config={
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
},safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
})
# response = model.generate_content("Write a paragraph about climate change.")
# print(response.text)
# Replace with your Gemini API key
gemini_api_key = api_key  



#directory = '/home/user/Desktop/python vul Datasets/misc/labeled_files'
directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/all_data_sets'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    print(filename)
    if os.path.isfile(f):
        with open(f, 'r',encoding='utf-8') as file:
            vul_code = file.read()
            binary_classification_prompt = f"""
            You will be provided with a python code delimited by triple backticks. 
            If it contains any security vulnerability, identify the lines of vulnerable code and only write the line in quotation.
            If the code does not contain a vulnerability, 
            then simply write "None."
            python code: '''{vul_code}'''
            """

            response = model.generate_content(binary_classification_prompt)
            
            

            with open("/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp1.csv", "a",encoding='utf-8') as output:
                s = str(response.text).replace('\n', ' ').strip()
                output.write(rf'{filename},{s}')
                output.write('\n')
            print(response.text)
            # OR : print(response.candidates[0].content.parts[0].text)
            time.sleep(10)  # Consider adjusting sleep time

