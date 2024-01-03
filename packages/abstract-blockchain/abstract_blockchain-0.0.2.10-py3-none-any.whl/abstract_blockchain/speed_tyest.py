from abstract_rpcs import RPCBridge
from abstract_abis import ABIBridge
from abstract_apis import APIBridge
from abstract_utilities import get_time_stamp
from abstract_utilities import safe_json_loads,create_and_read_json,safe_dump_to_file,safe_read_from_json
from web3 import Web3


import os
from abstract_utilities.json_utils import safe_read_from_json,closest_dictionary,find_matching_dicts
from abstract_utilities.type_utils import convert_to_number,is_number,make_list
from abstract_utilities.compare_utils import get_closest_match_from_list,get_shared_characters_count,get_common_portions
from abstract_gui import create_row_of_buttons,sg,AbstractWindowManager
from web3 import Web3
script_path = os.path.abspath(__file__)
directory_path = os.path.dirname(script_path)
def if_list_itterate(obj,itteration=0):
    if obj and isinstance(obj,list):
        obj = obj[itteration]
    return obj
import difflib
import difflib
def get_last_comp_list(string,compare_list):
    result_compare=None
    for list_item in compare_list:
        if isinstance(list_item,str):
            if string in list_item:
                result_compare = list_item
    return result_compare
def is_list_obj_in_string(list_objs,string):
    found = []
    for list_obj in make_list(list_objs):
        if list_obj in string:
            found.append(list_obj)
    return found            
def get_longest_common_portion(string, compare_string):
    for i in range(len(string), 0, -1):
        if string[:i] in compare_string:
            return string[:i]
    return ''


def get_common_portions(str1, str2):
    if not str1 or not str2:
        return ""

    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    longest, x_longest = 0, 0

    for x in range(1, len(str1) + 1):
        for y in range(1, len(str2) + 1):
            if str1[x - 1] == str2[y - 1]:
                matrix[x][y] = matrix[x - 1][y - 1] + 1
                if matrix[x][y] > longest:
                    longest = matrix[x][y]
                    x_longest = x
            else:
                matrix[x][y] = 0

    return str1[x_longest - longest: x_longest]

def get_shared_characters_count(string, compare_string):
    # Use a dictionary to count occurrences of each character in compare_string
    char_count = {}
    for char in compare_string:
        char_count[char] = char_count.get(char, 0) + 1

    # For each character in string, reduce its count in the dictionary
    for char in string:
        if char in char_count and char_count[char] > 0:
            char_count[char] -= 1

    # Sum the remaining counts to get the total count of shared characters
    return sum(char_count.values())
def find_max_beginning_match_length(comp_obj, common_portions):
    for portion in common_portions:
        if comp_obj.startswith(portion):
            return len(portion) / len(comp_obj)
    return 0
def get_closest_match_from_list(comp_obj, total_list, case_sensitive=False,highest_out=True,sorted_out=False):
    def get_sorted_output(comparison_data):
        return [obj for _, obj in sorted(comparison_data, key=lambda x: x[0], reverse=True)]
    def get_out(sorted_out,highest_out,comparison_data,obj):
        output = [get_sorted_output(comparison_data),obj]
        if sorted_out and highest_out:
            return output
        elif sorted_out:
            return output[0]
        elif highest_out:
            return output[-1]
    if isinstance(comp_obj, str):
        if not case_sensitive:
            comp_obj = comp_obj.lower()
            processed_list = [obj.lower() if isinstance(obj, str) else obj for obj in total_list]
        else:
            processed_list = [obj for obj in total_list if isinstance(obj, str)]
    else:
        processed_list = [obj for obj in total_list if isinstance(comp_obj, type(obj))]

    for obj in processed_list:
        # Check for perfect match
        if comp_obj == obj:
            return get_out(sorted_out,highest_out,[],obj)
    comparison_data=[]
    highest=None
    for obj in processed_list:
        obj_og = obj
        obj=obj.lower()
                             
        common_portions = get_common_portions(comp_obj,obj)
        if common_portions:
            longest_found_length = len(max(common_portions, key=len, default=''))
            length = len(comp_obj)/len(obj)
            characters_shared = get_shared_characters_count(comp_obj,obj)
            begins_with = find_max_beginning_match_length(comp_obj, common_portions)
            comp_curr_js = {
                "obj": obj,
                "found": common_portions,
                "longest_found": longest_found_length,
                "length": length,
                "beggins_with":beggins_with,
                "characters_shared": characters_shared
            }

            # Using a tuple for comparison
            comparison_criteria = (comp_curr_js["longest_found"], comp_curr_js["length"])
            comparison_data.append((comparison_criteria, obj_og))
            if not highest or comparison_criteria > (highest["longest_found"], highest["length"]):
                highest = comp_curr_js
    return get_out(sorted_out,highest_out,comparison_data,highest['obj'])
def closest_match_in_json(input_word, json_list, key='name'):
    highest_score = 0.0
    closest_obj = None

    for obj in json_list:
        if key in obj:
            current_word = obj[key]
            similarity = difflib.SequenceMatcher(None, input_word, current_word).ratio()
            if similarity > highest_score:
                highest_score = similarity
                closest_obj = obj

    return closest_obj
class RPCBridge: 
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """
    def __init__(self, rpc_js:dict=None,testnet=False,rpc_list=None,rpc_gui=False):
        """
        Initializes the RPCBridge instance with RPC parameters.

        :param rpc_js: Dictionary containing RPC parameters.
        """
        self.rpc_list= rpc_list or self.get_default_rpc_list()
        self.testnet_rpcs, self.non_testnet_rpcs = self.get_testnet_and_non_testnet(self.rpc_list)
        self.non_testnet_values = self.get_total_values_list(self.non_testnet_rpcs)
        self.testnet_values = self.get_total_values_list(self.testnet_rpcs)
        self.rpc_values = {"False":[self.non_testnet_values,self.non_testnet_rpcs],"True":[self.testnet_values,self.testnet_rpcs]}
        self.common_chains = ['Arbitrum One', 'Avalanche C-Chain', 'Endurance Smart Chain Mainnet', 'Celo Mainnet', 'Cronos Mainnet', 'Elastos Smart Chain', 'Ethereum Mainnet', 'Fuse Mainnet', 'Gnosis', 'Huobi ECO Chain Mainnet', 'Hoo Smart Chain', 'IoTeX Network Mainnet', 'Catecoin Chain Mainnet', 'Polygon Mainnet', 'Moonriver', 'Nahmii Mainnet', 'OKXChain Mainnet', 'Harmony Mainnet Shard 0', 'PandoProject Mainnet', 'Smart Bitcoin Cash', 'Neon EVM Mainnet', 'Telos EVM Mainnet', 'Ubiq']
        if rpc_gui:
            rpc_js = RPCGUIManager()
        self.update_rpc_js(rpc_js=rpc_js,testnet=testnet)
        
    def update_rpc_list(self,rpc_list):
        self.rpc_list = rpc_list
    def get_rpc_js(self,rpc_item=None,testnet=False):
        if not isinstance(rpc_item,dict):
            if rpc_item == None:
                rpc_item = self.get_default_rpc()
            else:
                #rpc_item = closest_match_in_json(rpc_item[0], self.rpc_list)
                closest_rpc_items = self.get_closest_values(make_list(rpc_item),self.rpc_values[str(testnet)][0])
                rpc_item = closest_dictionary(dict_objs = self.rpc_values[str(testnet)][1],values=closest_rpc_items)
        return rpc_item
    def update_rpc_js(self,rpc_js:dict=None,testnet=False):
        self.rpc_js=self.get_rpc_js(rpc_item=rpc_js,testnet=testnet)
        print(self.rpc_js)
        self.symbol = self.rpc_js['chain']
        self.name = self.rpc_js['name']
        self.explorers = self.get_explorers(self.rpc_js)
        self.explorer  = if_list_itterate(self.explorers)
        self.rpcs = self.get_rpc_urls(self.rpc_js)
        self.rpc  = if_list_itterate(self.rpcs)
        self.chainId = self.rpc_js['chainId']
        self.scanner = self.strip_web(self.explorer)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))
        return self.rpc_js
    def return_rpc_js(self,rpc_js:dict=None):
        return rpc_js or self.rpc_js
    def get_default_rpc(self,Network_Name:str="Ethereum", rpc_list:list=None):
        rpc_list= rpc_list or self.rpc_list
        return closest_dictionary(dict_objs=rpc_list,values=[Network_Name])
    def derive_rpc(self,new_rpc,testnet=False):
        derive_rpc_js = new_rpc
        for key in ['rpc','explorers']:
            if key in derive_rpc_js:
                del derive_rpc_js[key]
        if 'chainId' in new_rpc:
            if is_number(new_rpc['chainId']):
                new_rpc['chainId'] = int(new_rpc['chainId'])
        self.update_rpc_js(rpc_js=new_rpc,testnet=testnet)
        new_rpc['rpcs'] = new_rpc.get('rpcs',self.rpcs)
        self.rpcs=new_rpc['rpcs']
        new_rpc['rpc'] = new_rpc.get('rpc',if_list_itterate(self.rpcs))
        self.rpc=new_rpc['rpc']
        new_rpc['w3'] = Web3(Web3.HTTPProvider(self.rpc))
        self.w3 = new_rpc['w3']
        new_rpc['explorers'] = new_rpc.get('explorers',self.explorer)
        self.explorer = new_rpc['explorers']
        new_rpc['scanner'] = self.strip_web(self.explorer)
        self.scanner = new_rpc['explorers']
        new_rpc['chainId'] = new_rpc.get('chainId',self.chainId)
        self.chainId = new_rpc['chainId']
        new_rpc['name'] = new_rpc.get('name',self.name)
        self.name=new_rpc['name']
        new_rpc['chain'] = new_rpc.get('chain',self.symbol)
        self.symbol=new_rpc['chain']
        return new_rpc
    @staticmethod
    def strip_web(url:str):
        if url:
            if url.startswith("http://"):
                url = url.replace("http://", '', 1)
            elif url.startswith("https://"):
                url = url.replace("https://", '', 1)
            url = url.split('/')[0]
            return url
    @staticmethod
    def get_total_values_list(rpc_list):
        return {convert_to_number(value) for rpc in rpc_list for value in rpc.values() if isinstance(value, (str, int))}
    @staticmethod  
    def get_default_rpc_list():
        rpc_list =safe_read_from_json(os.path.join(directory_path,'data','rpc_list.json'))
        return rpc_list['chains']
    @staticmethod
    def get_testnet_and_non_testnet(rpc_list):
        testnet_rpcs = []
        non_testnet_rpcs = []

        for rpc in rpc_list:
            if 'testnet' in rpc['name'].lower().split(' '):
                testnet_rpcs.append(rpc)
            else:
                non_testnet_rpcs.append(rpc)

        return testnet_rpcs, non_testnet_rpcs
    @staticmethod
    def get_closest_values(rpc_js,total_values_list):
        rpc_js_new = []
        for i,rpc_value in enumerate(rpc_js):
            value = get_closest_match_from_list(rpc_value, total_values_list,sorted_out=False,highest_out=True)
            rpc_js_new.append(convert_to_number(value))
        return rpc_js_new
    @staticmethod
    def get_testnet(testnet, rpc_list):
        return [rpc for rpc in rpc_list if ('testnet' in rpc['name'].lower().split(' ')) == testnet]
    @staticmethod
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
    @staticmethod
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
def get_rpc_js_from_read():
    return  safe_read_from_json("""/home/joben/Documents/modules/abstract_blockchain/src/abstract_blockchain/data/source_codes/0x9d4492907cb050cd6567011ef7fb9e2b3d23c60b/Avalanche_C-Chain/rpc_data.json""")

def get_w3_read_rpc():

    return Web3(Web3.HTTPProvider(rpc))
def update_rpc_bridge(derive_network=True,rpc_mgr=None):
    return rpc_mgr.update_rpc_js(get_rpc_js_from_read())
def get_w3_from_rpc_mgr(derive_network=True):
    if derive_network:
        w3 = RPCBridge(rpc_js=['Avalanche']).w3
    else:
        w3 = RPCBridge(rpc_js=get_rpc_js_from_read()).w3
    return w3
def get_function_derivation():
    contract_address = '0x9D4492907cb050cd6567011ef7fb9e2b3D23c60B'
    abi = safe_json_loads(api_mgr.derive_network(contract_address=contract_address,api_data_type='sourcecode',multiple=False,initial_network='Avalanche')['contract_data'][0])['ABI']
    contract_bridge = w3.eth.contract(address=contract_address, abi=abi)
    function = getattr(contract_bridge.functions, 'totalSupply')
    return function().call()
def get_function_return_legacy(read_rpc=True):
    if read_rpc:
        w3=get_w3_read_rpc()
    
    contract_address=w3.to_checksum_address('0x9D4492907cb050cd6567011ef7fb9e2b3D23c60B')
    abi = safe_json_loads(safe_read_from_json("""/home/joben/Documents/modules/abstract_blockchain/src/abstract_blockchain/data/source_codes/0x9d4492907cb050cd6567011ef7fb9e2b3d23c60b/Avalanche_C-Chain/source_code.json""")[0])["ABI"]
    contract_bridge = w3.eth.contract(address=contract_address, abi=abi)
    function = getattr(contract_bridge.functions, 'totalSupply')
    return function().call()
    
def get_function_return_abi_bridge():
    abi_mgr = ABIBridge(contract_address='0x9D4492907cb050cd6567011ef7fb9e2b3D23c60B')
    bridge = abi_mgr.contract_bridge
    return abi_mgr.call_function(function_name='totalSupply',contract_bridge=bridge)

def get_time_for_function(function,function_name,**kwargs):
    start_time =get_time_stamp()
    result = function(**kwargs)
    end_time =get_time_stamp()
    lapsed_time = end_time - start_time
    string_output = f"{function_name} with "
    for key,value in kwargs.items():
        string_output +=f"{key} as {str(value)} "
    times = str(lapsed_time).split('.')
    if len(times[1])>3:
        times[1] = times[1][:3]
    string_output += f"ran for {times[0]}.{times[1]} seconds"
    print(string_output)
    return result
rpc_mgr=get_time_for_function(RPCBridge,function_name='RPCBridge')
get_time_for_function(function=update_rpc_bridge,function_name="update_rpc_bridge",rpc_mgr=rpc_mgr)
get_time_for_function(function=get_w3_from_rpc_mgr,function_name='get_w3_from_rpc_mgr',derive_network=True)
get_time_for_function(function=get_w3_from_rpc_mgr,function_name='get_w3_from_rpc_mgr',derive_network=False)
get_time_for_function(function=get_function_derivation,function_name='get_function_derivation')
get_time_for_function(function=get_function_return_legacy,function_name='get_function_return_legacy')
get_time_for_function(function=get_function_return_abi_bridge,function_name='get_function_return_abi_bridge')
