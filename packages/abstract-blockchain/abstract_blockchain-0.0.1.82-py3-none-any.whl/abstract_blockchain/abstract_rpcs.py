import os
from abstract_utilities.json_utils import closest_dictionary, find_matching_dicts,safe_read_from_json
from abstract_utilities.compare_utils import get_closest_match_from_list
from abstract_utilities.type_utils import is_number, convert_to_number,make_list
from abstract_gui import AbstractWindowManager,sg,make_component,create_row_of_buttons,text_to_key,get_event_key_js
from web3 import Web3
class RPCBridge: 
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """

    def __init__(self, rpc_js: dict = None, testnet=False, rpc_list=None, rpc_gui=False):
        """
        Initializes the RPCBridge instance with RPC parameters.
        """
        self.script_path = os.path.abspath(__file__)
        self.directory_path = os.path.dirname(self.script_path)
        self.rpc_list = rpc_list or self.get_default_rpc_list()
        self.testnet_rpcs, self.non_testnet_rpcs = self.separate_testnet_rpcs(self.rpc_list)
        self.non_testnet_values = self.get_total_values_list(self.non_testnet_rpcs)
        self.testnet_values = self.get_total_values_list(self.testnet_rpcs)
        self.rpc_values = {"False":[self.non_testnet_values,self.non_testnet_rpcs],"True":[self.testnet_values,self.testnet_rpcs]}
        self.common_chains = self.get_common_chains()
        self.rpc_js = self.update_rpc_js(rpc_js=rpc_js, testnet=testnet,rpc_gui=rpc_gui)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc)) if self.rpc else None
    def update_rpc_js(self, rpc_js: dict = None, testnet=False,rpc_gui=False):
        """
        Updates the RPC JavaScript object.
        """
        if rpc_gui:
            rpc_js = RPCGUIManager()
        if not isinstance(rpc_js,dict):
            if rpc_js == None:
                rpc_js = self.get_default_rpc()
            else:
                closest_rpc_items = self.get_closest_values(make_list(rpc_js),self.rpc_values[str(testnet)][0])
                rpc_js = closest_dictionary(dict_objs = self.rpc_values[str(testnet)][1],values=closest_rpc_items)
        self.rpc_js = rpc_js or self.get_default_rpc()
        self.setup_rpc_attributes()
        return self.rpc_js
    def setup_rpc_attributes(self,rpc_js: dict = None,):
        """
        Sets up various RPC attributes.
        """
        self.rpc_js = rpc_js or self.rpc_js
        self.symbol = self.rpc_js.get('chain', '')
        self.name = self.rpc_js.get('name', '')
        self.explorers = self.rpc_js.get('explorers', self.get_explorers(self.rpc_js))
        self.explorer = self.explorers[0] if self.explorers else None
        self.rpcs = self.rpc_js.get('rpcs',self.get_rpc_urls(self.rpc_js))
        self.rpc = self.rpcs[0] if self.rpcs else None
        self.chainId = int(self.rpc_js['chainId']) if is_number(self.rpc_js['chainId']) else None
        self.scanner = self.strip_web(self.explorer)
    @staticmethod
    def get_common_chains():
            return ['Arbitrum One', 'Avalanche C-Chain', 'Endurance Smart Chain Mainnet', 'Celo Mainnet', 'Cronos Mainnet', 'Elastos Smart Chain', 'Ethereum Mainnet', 'Fuse Mainnet', 'Gnosis', 'Huobi ECO Chain Mainnet', 'Hoo Smart Chain', 'IoTeX Network Mainnet', 'Catecoin Chain Mainnet', 'Polygon Mainnet', 'Moonriver', 'Nahmii Mainnet', 'OKXChain Mainnet', 'Harmony Mainnet Shard 0', 'PandoProject Mainnet', 'Smart Bitcoin Cash', 'Neon EVM Mainnet', 'Telos EVM Mainnet', 'Ubiq']

    @staticmethod
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
    @staticmethod
    def get_total_values_list(rpc_list):
        return {convert_to_number(value) for rpc in rpc_list for value in rpc.values() if isinstance(value, (str, int))}
    @staticmethod  
    def get_default_rpc_list():
        rpc_list =safe_read_from_json(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','rpc_list.json'))
        return rpc_list['chains']

    @staticmethod
    def separate_testnet_rpcs(rpc_list):
        """
        Separates testnet and non-testnet RPCs.
        """
        testnet_rpcs = [rpc for rpc in rpc_list if 'testnet' in rpc['name'].lower()]
        non_testnet_rpcs = [rpc for rpc in rpc_list if 'testnet' not in rpc['name'].lower()]
        return testnet_rpcs, non_testnet_rpcs
    @staticmethod
    def get_closest_values(rpc_js,total_values_list):
        rpc_js_new = []
        for i,rpc_value in enumerate(rpc_js):
            
            value = get_closest_match_from_list(rpc_value, list(total_values_list),sorted_out=False,highest_out=True)
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
    @staticmethod
    def get_default_rpc(Network_Name:str="Ethereum", rpc_list:list=None):
        if rpc_list == None:
            rpc_list =safe_read_from_json(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','rpc_list.json'))
            rpc_list= rpc_list['chains']
        return closest_dictionary(dict_objs=rpc_list,values=[Network_Name])
class RPCGUIManager:
    def __init__(self, rpc_mgr=None,rpc_list:list=None,rpc_js=None,rpc_gui=True,gui_window=True):
        self.rpc_list = rpc_list
        self.rpc_mgr = rpc_mgr
        if self.rpc_mgr == None:
            self.rpc_mgr = RPCBridge(rpc_js=rpc_js,rpc_list=rpc_list)
        self.rpc_js = rpc_js or self.rpc_mgr.rpc_js
        self.original_query=''
        self.rpc_list = self.rpc_mgr.rpc_list
        self.relevant_list = self.rpc_list
        self.section="RPCmgr"
        self.network_names = list({item.get('name') for item in self.rpc_list})
        self.rpc_key_value_js = {"name":"-NETWORK_NAME-",'Network':"-NETWORK-",'chain':"-SYMBOL-",'chainId':"-CHAINID-",'rpc':"-RPC-",'explorer':"-BLOCK_EXPLORER-"}
        self.all_keys = list(self.rpc_key_value_js.values())+['-SEARCH-',"-OK_RPC-","-EXIT_RPC-"]
        self.network_names.sort()
        self.new_network_names=self.network_names
        self.window_mgr = AbstractWindowManager()
        if gui_window:
            self.window_name = self.window_mgr.add_window(title='RPC Selector',layout=self.get_rpc_layout(),close_events=[text_to_key("-OK_RPC-",section=self.section),text_to_key("-EXIT_RPC-",section=self.section)],event_handlers=[self.rpc_win_while],suppress_raise_key_errors=False, suppress_error_popups=False, suppress_key_guessing=False,finalize=True)
            self.window=self.window_mgr.get_window()
            self.window_mgr.while_window(window_name=self.window_name)
            self.values = self.window_mgr.search_closed_windows(window_name=self.window_name,window=self.window)['values']
            self.rpc_values = self.get_rpc_values(self.values)
    def get_rpc_layout(self,section=None):
        relevant_list=self.rpc_mgr.rpc_list
        rpc_js = self.rpc_mgr.rpc_js
        names = [item.get('name') for item in relevant_list]
        name = names[0]
        names,name,rpc_js=self.get_rpc_js_vars(relevant_list,names=names,name=name,rpc_js=rpc_js)
        name,networks,network,chain_ids,rpcs,rpc,explorers,explorer,symbol=self.get_static_variables(rpc_js)
        layout = [
            [sg.Text('SEARCH'), sg.Input('', key=text_to_key('SEARCH',section=self.section),size=(20,1), enable_events=True)],
            [sg.Text('Network Name:'), sg.Combo(self.network_names,default_value=name, key=text_to_key('NETWORK_NAME',section=self.section), enable_events=True)],
            [sg.Text('Network:'), sg.Combo(networks,default_value=network,key=text_to_key('NETWORK',section=self.section),size=(20,1), enable_events=True)],
            [sg.Text('RPC:'), sg.Combo(rpcs,default_value=rpc, key=text_to_key('RPC',section=self.section),size=(20,1), enable_events=True)],
            [sg.Text('ChainID:'), sg.InputText(chain_ids,key=text_to_key('CHAINID',section=self.section),size=(20,1), disabled=True)],  # Make this an InputText to display ChainID
            [sg.Text('Block Explorer:'), sg.Combo(explorers,default_value=explorer, key=text_to_key('BLOCK_EXPLORER',section=self.section),size=(20,1), enable_events=True)],
            [sg.Text('Symbol:'), sg.InputText(symbol,key=text_to_key('SYMBOL',section=self.section),size=(20,1), disabled=True)]  # Make this an InputText to display Symbol
        ]
        layout.append(create_row_of_buttons({"button_text":"OK","enable_event":True,"key":text_to_key("OK_RPC",section=self.section)},
                                            {"button_text":"Show","enable_event":True,"key":text_to_key("SHOW_RPC",section=self.section)},
                                            {"button_text":"Reset","enable_event":True,"key":text_to_key("RESET_RPC",section=self.section)},
                                            {"button_text":"Exit","enable_event":True,"key":text_to_key("EXIT_RPC",section=self.section)}))
        return layout
    def get_testnet_or_mainnet(self,string):
        return 'Testnet' if 'Testnet'.lower() in str(string).lower() else 'Mainnet'
    def get_key_from_value(self,value):
            """
            Fetches the key for a given value from the `get_rpc_js()` mapping.
            
            Parameters:
            - value: The value for which the key needs to be found.
            
            Returns:
            - The key corresponding to the value.
            """
            for key,key_value in self.rpc_key_value_js.items():
                if key_value == value:
                    return key
    def get_static_variables(self,rpc_js):
        name,networks,network,chain_ids,rpcs,rpc,explorers,explorer,symbol='',[],'','',[],'',[],'',''
        if rpc_js:
            name = rpc_js['name']
            network=self.get_testnet_or_mainnet(name)
            networks=[network]
            chain_ids = rpc_js['chainId']
            rpcs = self.rpc_mgr.get_rpc_urls(rpc_js)
            if rpcs:
                rpc=rpcs[0]
            explorers = self.rpc_mgr.get_explorers(rpc_js)
            if explorers:
                explorer=explorers[0]
            symbol = rpc_js['chain']
        return name,networks,network,chain_ids,rpcs,rpc,explorers,explorer,symbol
    def get_rpc_js_vars(self,relevant_list,names=None,rpc_js=None,name=None):
        relevant_list= make_list(relevant_list or  self.rpc_mgr.rpc_list)
        
        if names ==None:
            names = [item['name'] for item in relevant_list]
        if name == None:
            name = names[0]
        if rpc_js == None:
            rpc_js = [item for item in relevant_list if item['name'] == name][0]
        return names,name,rpc_js
    def update_network_name(self,relevant_list,names=None,rpc_js=None,name=None):
        names,name,rpc_js=self.get_rpc_js_vars(relevant_list,names=names,rpc_js=rpc_js,name=name)
        self.window[self.script_event_js['-NETWORK_NAME-']].update(values=names,value=name)
        name,networks,network,chain_ids,rpcs,rpc,explorers,explorer,symbol=self.get_static_variables(rpc_js)
        self.window[self.script_event_js['-NETWORK-']].update(network)
        self.window[self.script_event_js['-RPC-']].update(values=rpcs,value=rpc)
        self.window[self.script_event_js['-CHAINID-']].update(value=chain_ids)
        self.window[self.script_event_js['-BLOCK_EXPLORER-']].update(values=explorers,value=explorer)
        self.window[self.script_event_js['-SYMBOL-']].update(value=symbol)

    def get_back_values(self,num_list,values):
        rpc_values = []
        for num in num_list:
            rpc_values.append(values[num])
        return rpc_values
    def rpc_win_while(self,event,values,window):
        self.event,self.values,self.window=event,values,window
        self.script_event_js = get_event_key_js(self.event,key_list=self.all_keys)
        value = None
        if self.script_event_js['found'] == '-SEARCH-':
            query = values[self.script_event_js['-SEARCH-']]
            if query == '' or len(query) < len(self.original_query):
                self.relevant_list = self.rpc_mgr.rpc_list
            else:
                self.relevant_list = [item for item in self.rpc_mgr.rpc_list if query.lower() in item['name'].lower()]
            name = self.values[self.script_event_js['-NETWORK_NAME-']]
            self.update_network_name(name=name,relevant_list=self.relevant_list)
                    #self.update_network_name(values=values,value=value,relevant_list=self.relevant_list)
            
        if self.script_event_js['found'] in ['-NETWORK_NAME-','-NETWORK-']:
            name = self.values[self.script_event_js['-NETWORK_NAME-']]
            relevant_list = self.rpc_mgr.rpc_list
            if self.script_event_js['found'] == '-NETWORK_NAME-':
                rpc_js = [item for item in self.rpc_mgr.rpc_list if item['name'] ==name][0] 
            else:
                network = self.get_testnet_or_mainnet(name)
                rpc_js = [item for item in self.rpc_mgr.rpc_list if item.get('name') ==name and self.get_testnet_or_mainnet(item.get('name')) == network][0] 
            selected_network = self.values[self.script_event_js['-NETWORK-']]
            self.update_network_name(rpc_js=rpc_js,names=self.new_network_names,name=name,relevant_list=relevant_list)
      
    def get_rpc_values(self,values) -> dict or None:
        rpc=[]
        section_keys = [self.script_event_js['-NETWORK_NAME-'],
                        self.script_event_js['-SYMBOL-'],
                        self.script_event_js['-CHAINID-'],
                        self.script_event_js['-NETWORK-'],
                        self.script_event_js['-BLOCK_EXPLORER-'],
                        self.script_event_js['-RPC-']]
        rpc_js = [item for item in self.rpc_mgr.rpc_list if item['name'] == values[section_keys[0]]][0]
        rpc_js['user_settings']={}
        for original_key in ['-NETWORK_NAME-','-SYMBOL-','-CHAINID-','-NETWORK-','-BLOCK_EXPLORER-','-RPC-']:
            event_js_key = self.script_event_js[original_key]
            rpc_key = self.get_key_from_value(original_key)
            value = values[event_js_key]
            rpc_js['user_settings'][rpc_key]=value
        
        return rpc_js

