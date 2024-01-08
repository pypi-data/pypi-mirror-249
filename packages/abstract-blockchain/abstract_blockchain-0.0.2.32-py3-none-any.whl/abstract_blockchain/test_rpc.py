import os
from abstract_utilities.json_utils import safe_read_from_json,safe_dump_to_file,closest_dictionary,find_matching_dicts
from abstract_utilities.list_utils import filter_json_list_values,recursive_json_list
from abstract_utilities.type_utils import convert_to_number,is_number,if_default_return_obj,make_list,is_number
from abstract_utilities.compare_utils import is_list_obj_in_string,get_closest_match_from_list
from abstract_gui import get_push,create_row_of_buttons,get_menu,get_push,sg,AbstractWindowManager
from web3 import Web3
script_path = os.path.abspath(__file__)
directory_path = os.path.dirname(script_path)
rpc_list =safe_read_from_json(os.path.join(directory_path,'data','rpc_list.json'))['chains']

class RPCBridge: 
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """
    def __init__(self, rpc_js:dict=None,testnet=False,rpc_list=None):
        """
        Initializes the RPCBridge instance with RPC parameters.

        :param rpc_js: Dictionary containing RPC parameters.
        """
        self.rpc_list= rpc_list or self.get_default_rpc_list()
        if rpc_js == None:
            self.rpc_js = self.get_default_rpc()
        else:
            self.valid_rpcs = self.get_testnet(testnet,self.rpc_list)
            self.total_values_list = self.get_total_values_list(self.valid_rpcs)
            self.rpc_js = self.get_closest_values(rpc_js,self.total_values_list)
            self.rpc_js = closest_dictionary(dict_objs = self.valid_rpcs,values=self.rpc_js)
        self.symbol = self.rpc_js['chain']
        self.network_name = self.rpc_js['name']
        self.block_explorer = self.get_explorer(self.rpc_js)
        self.rpc = self.get_rpc_url(self.rpc_js)
        self.chain_id = self.rpc_js['chainId']
        self.scanner = self.strip_web(self.block_explorer)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))
    @staticmethod
    def get_total_values_list(rpc_list):
        return {
            convert_to_number(value) 
            for rpc in rpc_list 
            for value in rpc.values() 
            if isinstance(value, (str, int))
        }
    @staticmethod
    def get_closest_values(rpc_js,total_values_list):
        for i,rpc_value in enumerate(rpc_js):
            value = get_closest_match_from_list(rpc_value, total_values_list)
            rpc_js[i] = convert_to_number(value)
        return rpc_js
    @staticmethod
    def get_testnet(testnet, rpc_list):
        test_net_string = 'testnet'
        return [
            rpc for rpc in rpc_list
            if (test_net_string in rpc['name'].lower().split(' ')) == testnet]
    @staticmethod
    def get_rpc_url(rpc_js):
        url=None
        rpc=''
        rpcs=[]
        if 'rpc' in rpc_js:
            rpcs = find_matching_dicts(dict_objs=rpc_js['rpc'],keys=['tracking'],values=['none']) or self.rpc_js['rpc']
        if isinstance(rpcs,list):
            rpc = rpcs[0]
        if 'url' in rpc:
            url = rpc['url']
        return url
    @staticmethod
    def get_explorer(rpc_js):
        url=None
        explorer=''
        explorers=[]
        if 'explorers' in rpc_js:
            explorers=rpc_js['explorers']
        if isinstance(explorers,list):
            explorer = explorers[0]
        if 'url' in explorer:
            url = explorer['url']
        return url
    def get_rpc_values(self,rpc_js):
        if rpc_js and not isinstance(rpc_js,dict):
            rpc_js=closest_dictionary(dict_objs=self.rpc_list,values=rpc_js)
        return rpc_js or self.get_default_rpc()
    @staticmethod
    def strip_web(url:str):
        if url.startswith("http://"):
            url = url.replace("http://", '', 1)
        elif url.startswith("https://"):
            url = url.replace("https://", '', 1)
        url = url.split('/')[0]
        return url
    def update_rpc_list(self,rpc_list):
        self.rpc_list = rpc_list
    def return_rpc_js(self,rpc_js:dict=None):
        return if_default_return_obj(obj=self.rpc_js,default=rpc_js)
    def get_default_rpc(self,Network_Name:str="Ethereum", rpc_list:list=None):
        rpc_list= self.rpc_list or rpc_list
        return closest_dictionary(dict_objs=rpc_list,values=[Network_Name])
    @staticmethod  
    def get_default_rpc_list():
        rpc_list =safe_read_from_json(os.path.join(directory_path,'data','rpc_list.json'))
        return rpc_list['chains']

