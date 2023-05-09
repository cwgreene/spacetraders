import supersecret
import requests

token = supersecret.getSecret('spacetraders','apitoken')
root_url = 'https://api.spacetraders.io/v2'

def get_apicall(path):
    return requests.get("/".join([root_url, path]), headers={
        "Authorization":  f"Bearer {token}"
    })

def post_apicall(path, data):
    return requests.post("/".join([root_url, path]),
        data=data,
        headers={
        "Authorization":  f"Bearer {token}"
    })

def contracts():
    return get_apicall("/my/contracts").json()

def ships():
    return get_apicall("/my/ships").json()

def systems():
    return get_apicall("/systems").json()

def accept(contract_id):
    return post_apicall(f"/my/contracts/{contract_id}/accept",data={}).json()
