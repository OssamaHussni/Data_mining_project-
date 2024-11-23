import os
import time
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

labels3 = [
    
    "CWE-379","CWE-384","CWE-385","CWE-400","CWE-406","CWE-414","CWE-425","CWE-434","CWE-454"
    ,"CWE-462","CWE-477","CWE-488","CWE-502","CWE-521","CWE-522","CWE-595","CWE-601","CWE-605"
    ,"CWE-611","CWE-641","CWE-643","CWE-703","CWE-730","CWE-732","CWE-759","CWE-760","CWE-776"
    ,"CWE-798","CWE-827","CWE-835","CWE-841","CWE-918","CWE-941","CWE-943","CWE-352","CWE-409"
    ,"CWE-266","CWE-311","CWE-315","CWE-1240"
    ,"CWE-79", "CWE-489", "CWE-78", "CWE-94","CWE-15","CWE-22","CWE-89","CWE-1004"
    ,"CWE-614","CWE-95","CWE-20","CWE-80","CWE-90","CWE-99","CWE-113","CWE-116","CWE-117"
    ,"CWE-1204","CWE-193","CWE-200","CWE-209","CWE-215","CWE-250","CWE-252","CWE-259","CWE-269"
    ,"CWE-283","CWE-284","CWE-285","CWE-295","CWE-297","CWE-306","CWE-312","CWE-319","CWE-321"
    ,"CWE-326","CWE-327","CWE-329","CWE-330","CWE-331","CWE-339","CWE-347","CWE-367","CWE-377"
]


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


#directory = '/home/user/Desktop/python vul Datasets/misc/labeled_files'
directory = '/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/all_data_sets'



for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(filename)
        with open(f,'r') as file:
            Vul_code=file.read()
            
            multiClass_prompt = f"""
            which of the following vulnerabilities from list of vulnerabilities exist in the python code which
            is delimited with triple backticks. also give the line of the vulnerability in the code.

            python code: '''{Vul_code}'''

            list of vulnerabilities: {", ".join(labels3)}

            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each element.
            only answer with JSON.
            """
            response = model.generate_content(multiClass_prompt)
            with open('/Users/ossam/OneDrive/Desktop/Data_mining_project/ChatGPTasSAST-main/Data sets/test2_exp2.csv', "a") as output:
                s=str(response.text).replace('\n',' ').strip()
                output.write(rf'{filename},{s}')
                output.write('\n')
            print(response.text)
            time.sleep(17)



