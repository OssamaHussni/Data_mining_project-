import os
import time
import urllib.parse
import requests
import re
import google.generativeai as genai
import pandas as pd
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import csv

#from IPython import display,HTML
#from dotenv import load_dotenv,find_dotenv
#directory = '/home/user/Desktop/python vul Datasets/Siddiq/Labeled_files'
directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/all_data_sets'

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
gemini_api_key = api_key


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(filename)
        with open(f,'r') as file:
            Vul_code=file.read()
            prompt3 = f"""
            your task is to determine whether the following python code which is delimited with triple backticks,is vulnerable or not?
            identify the following items:
                - CWE of its vulnerabilities. \
                - lines of vulnerable code. \
            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each vulnerability.
            If the information isn't present, use "unknown" \
            as the value.
            Make your response as short as possible and only answer with JSON. .
            python code: '''{Vul_code}'''
            """

            #print(prompt3)

            response = model.generate_content(prompt3)
            output_file_path = r"/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp_4_gpt_result_withoutclass.csv"

            # Open the file in append mode
            with open(output_file_path, mode="a", newline="", encoding="utf-8") as output_file:
                # Define the fieldnames for the CSV columns
                fieldnames = ["filename", "content"]
                
                # Create a CSV writer
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                
                # Prepare the data
                s = str(response.text).replace('\n', ' ').strip()  # Clean and format the content
                data_row = {
                    "filename": filename,  # First column
                    "content": s           # Second column
                }
                
                # Write the data to the file
                writer.writerow(data_row)

            
            # with open("/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test_exp_4_gpt_result_withoutclass.csv", "a") as output:
            #     s=str(response.text).replace('\n',' ').strip()
            #     output.write(rf'{filename},{s}')
            #     output.write('\n')
            #print(response.text)
            time.sleep(10)

