import requests
import base64
# from ..config import base_url, api_token

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"
def roc_plot(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/roc"
    headers = {"Authorization":client_token}
    response = requests.post(url, data=data,headers=headers)
    print(response.text)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def advanced_lift_chart(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/advanced-lift-chart"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def advanced_feature_impact(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/advanced-feature-impact"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def partial_dependency(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/partial-dependency"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()




def residual(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/residual"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()



def predict_vs_actual(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/predict-vs-actual"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def word_cloud(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/wordcloud"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def confusion_matrix(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/confusion-matrix"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()



#test

a = roc_plot("3991a687-9f1d-44bd-baea-b1bf91229c38","image","eyJuYW1lIjoiYWFiYiIsImVtYWlsIjoiYWFjY0B5b3BtYWlsLmNvbSJ9:1rGbLp:OOBiKlbYKo98hqXYSIc5U13Ls7CGE9bkbJHTtdRglPE")