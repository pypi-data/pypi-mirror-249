import requests
from abstract_utilities.json_utils import get_dict_from_string,find_matching_dicts
from abstract_utilities import read_from_file,safe_json_loads,safe_dump_to_file,safe_read_from_json,make_list
def try_request(name):
    try:
        response = requests.get(f"{name}/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey=4VK8PEWQN4TU4T5AV5ZRZGGPFD52N2HTM1")
        if response.status_code in [200,401]:

           print(name)     
    except:
        print(f'{name} did not load')  
    try:
        
        response = response.json()
        print(f'{response}')
    except:
        print(f'{response} did not load as json')
        print(f'{response.text}')

rpc_list = safe_read_from_json('rpc_list.json')
for rpc in rpc_list['chains']:
    for explorer in rpc['explorers']:
       try_request(explorer['url'])
    for key,values in rpc.items():
        if isinstance(values,list):
            for value in values:
                if isinstance(value,dict):
                    url = value.get('url')
                    if url and 'api' in url:
                        spl = url.split('/')
                        while '' in spl:
                            spl.remove('')
                        domain = spl[1].split('?')[0]
                        print(domain)
                        
