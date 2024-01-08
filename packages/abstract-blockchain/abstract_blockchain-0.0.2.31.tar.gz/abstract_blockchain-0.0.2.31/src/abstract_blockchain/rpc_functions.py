from abstract_utilities.path_utils import makeAllDirs
from abstract_utilities.type_utils import is_number, convert_to_number,make_list
from abstract_utilities.json_utils import closest_dictionary, find_matching_dicts,safe_read_from_json
from abstract_utilities.compare_utils import get_closest_match_from_list

from web3 import Web3
import os
import json

def get_common_chains():
        return ['Arbitrum One', 'Avalanche C-Chain', 'Endurance Smart Chain Mainnet', 'Celo Mainnet', 'Cronos Mainnet', 'Elastos Smart Chain', 'Ethereum Mainnet', 'Fuse Mainnet', 'Gnosis', 'Huobi ECO Chain Mainnet', 'Hoo Smart Chain', 'IoTeX Network Mainnet', 'Catecoin Chain Mainnet', 'Polygon Mainnet', 'Moonriver', 'Nahmii Mainnet', 'OKXChain Mainnet', 'Harmony Mainnet Shard 0', 'PandoProject Mainnet', 'Smart Bitcoin Cash', 'Neon EVM Mainnet', 'Telos EVM Mainnet', 'Ubiq']

def strip_web(url:str):
    if isinstance(url,dict):
        url = url.get('url',url)        
    if url:
        if url.startswith("http://"):
            url = url.replace("http://", '', 1)
        elif url.startswith("https://"):
            url = url.replace("https://", '', 1)
        url = url.split('/')[0]
        return url

def get_total_values_list(rpc_list):
        new_list = []
        for rpc in rpc_list:
                for value in rpc.values():
                        if isinstance(value, (str, int)):
                                new_list.append(value)
        return new_list
def get_default_rpc_list():
    
    rpc_list =read_json(makeAllDirs(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','rpc_list.json')))
    return rpc_list['chains']


def separate_testnet_rpcs(rpc_list):
    """
    Separates testnet and non-testnet RPCs.
    """
    testnet_rpcs = [rpc for rpc in rpc_list if 'testnet' in rpc['name'].lower()]
    non_testnet_rpcs = [rpc for rpc in rpc_list if 'testnet' not in rpc['name'].lower()]
    return testnet_rpcs, non_testnet_rpcs

def get_closest_values(rpc_js,total_values_list):
    rpc_js_new = []
    for i,rpc_value in enumerate(rpc_js):

        value = get_closest_match_from_list(rpc_value, list(total_values_list),sorted_out=False,highest_out=True)
        rpc_js_new.append(value)

    return rpc_js_new

def get_testnet(testnet, rpc_list):
    return [rpc for rpc in rpc_list if ('testnet' in rpc['name'].lower().split(' ')) == testnet]

def get_rpc_urls(rpc_js):
    urls=[]
    rpc=''
    rpcs=[]
    if 'rpc' in rpc_js:
        rpcs = find_matching_dicts(dict_objs=rpc_js['rpc'],keys=['tracking'],values=['none']) or rpc_js['rpc']
    for rpc in rpcs:
        if 'url' in rpc:
            urls.append(rpc['url'])
    return urls

def get_explorers(rpc_js):
    urls=[]
    explorer=''
    explorers=[]
    if 'explorers' in rpc_js:
        explorers=rpc_js['explorers']
    for explorer in explorers:
        if 'url' in explorer:
            urls.append(explorer['url'])
    return urls

def get_default_rpc(Network_Name:str="Ethereum", rpc_list:list=None):
    if rpc_list == None:
        rpc_list =read_json(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','rpc_list.json'))
        rpc_list= rpc_list['chains']
    return closest_dictionary(dict_objs=rpc_list,values=[Network_Name])
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {file_path}")

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

