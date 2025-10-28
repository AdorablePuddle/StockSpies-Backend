from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage

from openai import OpenAI
from openai import OpenAIError

import os
from datetime import datetime
import base64
from dotenv import load_dotenv

from json import loads

load_dotenv()

tmpfiles = "./tmpfiles/"
'''
print(os.getcwd())
print(os.environ.get("QWEN_AUTH_TOKEN"))
print(os.environ.get("QWEN_COOKIE"))
'''
'''
client = Qwen(
    log_level = "DEBUG",
    api_key = os.environ.get("QWEN_AUTH_TOKEN"),
    cookie = os.environ.get("QWEN_COOKIE"),
)
'''

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

# To-do: Rewrite all this!

def download_image_file(f : InMemoryUploadedFile):
    print(f"[upload] Download image")
    FileSystemStorage(location = tmpfiles).save(f.name, f)
    return f.name
'''
def get_prediction(f : InMemoryUploadedFile):
    file_name = download_image_file(f)
    
    try:
        print(f"[prediction] Upload image {file_name}")
        get_data_image = client.chat.upload_file(
            tmpfiles + file_name
        )
        
        print(f"[prediction] Generate prompt")
        message = [ChatMessage(
            role = "user",
            web_search = False,
            thinking = False,
            blocks = [
                TextBlock(
                    block_type = "text",
                    text = "Please identify the closest produce and its stock level in this image and return a string denoting the name of the produce, followed by a colon and then a decimal number between 0 and 1 with 0 being empty and 1 being fully stocked. If no produce are found, return a single '-1'."
                ),
                ImageBlock(
                    block_type = "image",
                    url = get_data_image.file_url,
                    image_mimetype = get_data_image.image_mimetype
                )
            ],
        )]
        
        print(f"[prediction] Receive response")
        response = client.chat.create(
            messages = message,
            model = "qwen-max-latest",
            stream = True,
        )
        
        print(f"[prediction] Output response")
        output = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            output = output + delta.content
        
        print(output)
        if output == "-1":
            raise ValueError("Image does not contain any produce.")
        
        output_split = output.split(": ")
        return output_split[0], output_split[1]
    
    except QwenAPIError as e:
        print(f"[ERROR] {str(e)}")
        
        raise RuntimeError("The API fucked up. Check backend log to see the precise reason why.")
'''

def get_prediction(f : InMemoryUploadedFile):
    file_name = download_image_file(f)
    prompt = "Please identify the 5 closest produces in this image. Return a JSON styled output in the following style: {'produce name':{'quantity':<an integer denoting the number of units of produce visible>,'stock level':<floating point number between 0 and 1 with 0 being empty and 1 being fully stocked>,'confidence':<floating point number between 0 and 1 with 0 being very uncertain about the result and 1 being completely certain about the result.>}}. If no produce is identified, return a single '-1'."
    
    print(f"[prediction] Upload image {file_name}")
    with open(tmpfiles + file_name, "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    try:
        print(f"[prediction] Requesting response")
        response = client.responses.create(
            model = "gpt-4.1-mini",
            input = [
                {
                    "role" : "user",
                    "content" : [
                        {"type" : "input_text", "text" : prompt},
                        {"type" : "input_image", "image_url" : f"data:image/png;base64,{b64_image}"}
                    ]
                }
            ]
        )
        print(f"[prediction] Receiving response")
        output = response.output_text
    except OpenAIError as e:
        print(f"[ERROR] {str(e)}")
        raise RuntimeError(str(e))
    
    print(f"[prediction] Output response")
    if output == "-1":
        return []
        # raise ValueError("Image does not contain any produce.")
    
    result = dict(loads(output))
    now = datetime.now()
    
    for produce in result.keys():
        result[produce]["timestamp"] = str(now)
    
    formatted_result = []
    for produce in result.keys():
        formatted_result.append({
            "label" : produce,
            "quantity" : result[produce]["quantity"],
            "stock_percentage" : int(result[produce]["stock level"] * 100),
            "confidence" : int(result[produce]["confidence"] * 100),
            "timestamp" : result[produce]["timestamp"],            
        })
    
    print(formatted_result)
    return formatted_result