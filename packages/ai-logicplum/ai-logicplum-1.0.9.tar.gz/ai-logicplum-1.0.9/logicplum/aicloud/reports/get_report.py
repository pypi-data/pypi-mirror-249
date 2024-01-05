import requests
import base64
import json 
from ..config import base_url, api_token

def reports(deployment_id,client_token):
    data = {
    "deployment_id": deployment_id
    }

    url = f'{base_url}/plot/report'
    headers = {"Authorization":client_token}
    response = requests.post(url, data=data,headers=headers)
    pdf_data = response.content
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    data = {
        'result': pdf_base64
    }
    json_string = json.dumps(data)
    return json_string