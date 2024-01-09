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


def get_allColumns(deployment_id,client_token):
    url = f"{base_url}/plot/dataset-columns//{deployment_id}"
    headers = {"Authorization":client_token}
    response = requests.get(url,headers=headers)
    return response.json()

def prediction_distribution(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/prediction-distribution"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()