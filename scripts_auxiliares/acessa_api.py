import requests
import json

gazettes_endpoint = "https://queridodiario.ok.org.br/api/gazettes?"
available_cities = "https://queridodiario.ok.org.br/api/cities?levels=3"

params = {
    "territory_ids": None,            
    "published_since" : None,
    "published_until" : None,
    "querystring": None,            # string
    "excerpt_size": 1000,            # int
    "number_of_excerpts": 50,        
    "pre_tags": "",            
    "post_tags": "",           
    "size": 200,
    "offset": None,
    "sort_by": "ascending_date"
}

part = params["excerpt_size"]/4

def request_url(params):
    url = gazettes_endpoint
    for key in params.keys():
        if params[key] is None:
            continue
        elif params[key] == "":
            continue
        else:
            url += f"{key}={params[key]}&"
    return url[:-1]

def get_response(url): 
    response = requests.get(url)
    return json.loads(response.text)