from io import BytesIO
from dotenv import dotenv_values

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import openai
from openai import OpenAI

import time

class TextExtracter():
    def __init__(self, image_path, text_dir):
        self.config = dotenv_values(".env")
        self.VISION_KEY = self.config["VISION_KEY"]
        self.VISION_ENDPOINT = self.config["VISION_ENDPOINT"]
        self.OPENAI_KEY = self.config["OPENAI_KEY"]
        openai.api_key = self.OPENAI_KEY
        self.image_path = image_path
        self.text_dir = text_dir

    def get_image(self, image_path):
        with open(image_path, "rb") as image:
            image_data = image.read()
        image_stream = BytesIO(image_data)

        return image_stream
    
    def get_text(self, text_path):
        with open(text_path, 'r', encoding='utf-8') as file:
            extracted_text = file.read()
        
        return extracted_text
    
    def extract_text(self):
        print("===== [Start] Extract text from Image - Azure CV API =====")
        computervision_client = ComputerVisionClient(self.VISION_ENDPOINT, 
                                            CognitiveServicesCredentials(self.VISION_KEY))
        
        image_data = self.get_image(self.image_path)

        # Call API with URL and raw response (allows you to get the operation location)
        read_response = computervision_client.read_in_stream(image_data,  raw=True)

        # Get the operation location (URL with an ID at the end) from the response
        read_operation_location = read_response.headers["Operation-Location"]

        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for it to retrieve the results 
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        # Print the detected text, line by line
        
        if read_result.status == OperationStatusCodes.succeeded:
            with open(self.text_dir+'extracted_text.txt', 'w') as file:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        file.write(line.text + '\n')
                        file.write(str(line.bounding_box) + '\n')

        print("===== [Finished] Extract text from Image - Azure CV API =====")
        
    def summarize_text(self):
        print("===== [Start] Summarize Text - OpenAI API =====")
        client = OpenAI(api_key=self.OPENAI_KEY)

        extracted_text = self.get_text(self.text_dir+'extracted_text.txt')
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                "content": '以下の[テキスト]を[制約]に従って[出力フォーマット]で出力してください。[制約]* 出力は[出力フォーマット]のみ出力してください。* [出力フォーマット]以外の余計な文章は出力しないでください。[出力フォーマット] { "明細": [{  "商品名": "テスト",  "数量": 1}]} \n[テキスト] '},
                {"role": "user",
                "content": extracted_text }]
            )
        
        # Get the content from the response
        json_content = response.choices[0].message.content

        # Write the content to a JSON file
        # with open('sample/recipt_summary.json', 'w') as json_file:
        #    json_file.write(json_content)
        
        print("===== [Finished] Summarize Text - OpenAI API =====")
        return json_content