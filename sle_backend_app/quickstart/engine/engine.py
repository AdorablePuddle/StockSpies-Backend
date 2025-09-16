from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from qwen_api.client import Qwen
from qwen_api.core.exceptions import QwenAPIError
from qwen_api.core.types.chat import ChatMessage, TextBlock, ImageBlock
import os
from dotenv import load_dotenv

load_dotenv()

tmpfiles = "./tmpfiles/"
'''
print(os.getcwd())
print(os.environ.get("QWEN_AUTH_TOKEN"))
print(os.environ.get("QWEN_COOKIE"))
'''
client = Qwen(
    log_level = "DEBUG",
    api_key = os.environ.get("QWEN_AUTH_TOKEN"),
    cookie = os.environ.get("QWEN_COOKIE"),
)

def download_image_file(f : InMemoryUploadedFile):
    print(f"[upload] Download image")
    FileSystemStorage(location = tmpfiles).save(f.name, f)
    return f.name

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
                    text = "What is in this image?"
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
        
        # Generally speaking, the output isn't working atm.
        return 0
    except QwenAPIError as e:
        print(f"[ERROR] {str(e)}")
        
        raise RuntimeError("The API fucked up. Check backend log to see the precise reason why.")
        