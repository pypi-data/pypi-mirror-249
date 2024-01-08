from .rpc_functions import *
import json

class RPCBridge: 
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """

    def __init__(self, rpc_js: dict = None, testnet=False, rpc_list=None, rpc_gui=False):
        """
        Initializes the RPCBridge instance with RPC parameters.
        """
        self.rpc_js=rpc_js or get_default_rpc()
        self.rpc_list = rpc_list or get_default_rpc_list()
        if isinstance(rpc_js,str):
            sets = [(item.get('name'),item) for item in self.rpc_list]
            names = [item[0] for item in sets]
            closest_match = get_closest_match_from_list(rpc_js,names)
            self.rpc_js = [item[1] for item in sets if item[0] == closest_match][0]
        self.script_path = os.path.abspath(__file__)
        self.directory_path = os.path.dirname(self.script_path)
        
        self.testnet_rpcs, self.non_testnet_rpcs = separate_testnet_rpcs(self.rpc_list)
        self.non_testnet_values = get_total_values_list(self.non_testnet_rpcs)
        self.testnet_values = get_total_values_list(self.testnet_rpcs)
        self.rpc_values = {"False":[self.non_testnet_values,self.non_testnet_rpcs],"True":[self.testnet_values,self.testnet_rpcs]}
        self.common_chains = get_common_chains()
        self.symbol = self.rpc_js.get('chain', '')
        self.name = self.rpc_js.get('name', '')
        self.explorers = self.rpc_js.get('explorers', [])
        self.explorer = self.explorers[0] if self.explorers else None
        self.rpcs = get_rpc_urls(self.rpc_js)
        self.rpc= self.rpcs[0] if self.rpcs else None
        self.chainId = int(self.rpc_js.get('chainId')) if is_number(self.rpc_js.get('chainId')) else None
        self.scanner = strip_web(self.explorer.get('url'))
        self.w3 = Web3(Web3.HTTPProvider(self.rpc)) if self.rpc else None
        self.rpc_js['user_settings'] = {'symbol':self.symbol,
                                        'name':self.name,
                                        'explorers':self.explorers,
                                        'explorer':self.explorer,
                                        'rpcs':self.rpcs,
                                        'rpc':self.rpc,
                                        'chainId':self.chainId,
                                        'scanner':self.scanner,
                                        'w3':self.w3}
    def update_rpc_js(self, rpc_js: dict):
        """
        Directly updates the RPC JavaScript object with new settings.
        """
        self.rpc_js=rpc_js or self.rpc_js or get_default_rpc()
        self.rpc_list = self.rpc_list or get_default_rpc_list()
        if isinstance(rpc_js,str):
            sets = [(item['name'],item) for item in self.rpc_list]
            names = [item[0] for item in sets]
            closest_match = get_closest_match_from_list(rpc_js,names)
            self.rpc_js = [item[1] for item in sets if item[0] == closest_match][0]
        if isinstance(rpc_js, dict):
            self.rpc_js = rpc_js
        self.setup_rpc_attributes()
        return self.rpc_js
    def setup_rpc_attributes(self):
        """
        Sets up various RPC attributes based on the current rpc_js.
        """
        # Extract values from rpc_js and set them to the instance attributes
        self.symbol = self.rpc_js.get('chain', '')
        self.name = self.rpc_js.get('name', '')
        self.explorers = self.rpc_js.get('explorers', [])
        self.explorer = self.explorers[0] if self.explorers else None
        self.rpcs = get_rpc_urls(self.rpc_js)
        self.rpc= self.rpcs[0] if self.rpcs else None
        self.chainId = int(self.rpc_js['chainId']) if is_number(self.rpc_js['chainId']) else None
        self.scanner = strip_web(self.explorer['url'])
        self.w3 = Web3(Web3.HTTPProvider(self.rpc)) if self.rpc else None
        self.rpc_js['user_settings'] = {'symbol':self.symbol,
                                        'name':self.name,
                                        'explorers':self.explorers,
                                        'explorer':self.explorer,
                                        'rpcs':self.rpcs,
                                        'rpc':self.rpc,
                                        'chainId':self.chainId,
                                        'scanner':self.scanner,
                                        'w3':self.w3}
    def update_settings(self, new_settings):
        """
        Updates the RPCBridge instance settings based on the provided new settings.

        Parameters:
        new_settings (dict): A dictionary containing the new settings.
        """
        # Update relevant attributes based on new settings
        self.rpc_js = new_settings.get('rpc_js', self.rpc_js)
        self.rpc = self.get_rpc_url(self.rpc_js)  # Assuming a method to extract the main RPC URL
        self.w3 = Web3(Web3.HTTPProvider(self.rpc)) if self.rpc else None
        # Add other necessary updates based on new settings

    # Helper method to extract the main RPC URL from rpc_js
    def get_rpc_url(self, rpc_js):
        return rpc_js['rpc'][0] if 'rpc' in rpc_js and len(rpc_js['rpc']) > 0 else None


class RPCGui:
    def __init__(self, rpc_mgr=None,rpc_list:list=None,rpc_js=None,rpc_gui=True,gui_window=True):
        self.rpc_list = rpc_list
        self.rpc_mgr = rpc_mgr
        if self.rpc_mgr == None:
            self.rpc_mgr = RPCBridge(rpc_js=rpc_js,rpc_list=rpc_list)
        
        self.rpc_js = rpc_js or self.rpc_mgr.rpc_js
        self.user_selection =  self.rpc_js
        self.original_query=''
        
        self.relevant_list = self.rpc_list
        self.section="RPCmgr"
        self.rpc_list = self.rpc_mgr.rpc_list
        self.rpc_sets = [(item['name'],item) for item in self.rpc_list]
        self.rpc_names = list({item[0] for item in self.rpc_sets})
        self.rpc_testnets = [item for item in self.rpc_sets if 'testnet' in item[0].lower()]
        self.rpc_mainnets = [item for item in self.rpc_sets if 'testnet' not in item[0].lower()]
        self.rpc_key_value_js = {"name":"-NETWORK_NAME-",'Network':"-NETWORK-",'chain':"-SYMBOL-",'chainId':"-CHAINID-",'rpc':"-RPC-",'explorer':"-BLOCK_EXPLORER-"}
        self.all_keys = list(self.rpc_key_value_js.values())+['-SEARCH-',"-OK_RPC-","-EXIT_RPC-"]
        self.rpc_names.sort()
        self.window_mgr = AbstractWindowManager()
        if rpc_gui:
            self.run_gui_window()
    def run_gui_window(self):
            self.window_name = self.window_mgr.add_window(title='RPC Selector',
                                                          layout=self.get_rpc_layout(),
                                                          close_events=[text_to_key("-OK_RPC-",section=self.section),
                                                                        text_to_key("-EXIT_RPC-",section=self.section)],
                                                          event_handlers=[self.rpc_win_while],
                                                          suppress_raise_key_errors=False,
                                                          suppress_error_popups=False,
                                                          suppress_key_guessing=False,
                                                          finalize=True)
            self.window=self.window_mgr.get_window()
            self.window_mgr.while_window(window_name=self.window_name)
            self.values = self.window_mgr.search_closed_windows(window_name=self.window_name,
                                                                window=self.window)['values']
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
            [sg.Text('Network Name:'), sg.Combo(self.rpc_names,default_value=name, key=text_to_key('NETWORK_NAME',section=self.section), enable_events=True)],
            [sg.Text('Network:'), sg.Combo(['Mainnet','Testnet'],default_value=network,key=text_to_key('NETWORK',section=self.section),size=(20,1), enable_events=True)],
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
            rpcs = get_rpc_urls(rpc_js)
            if rpcs and isinstance(rpcs,list):
                rpc=rpcs[0]
            explorers = get_explorers(rpc_js)
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
            rpc_js = [item for item in relevant_list if item.get('name') == name][0]
        return names,name,rpc_js
    def update_network_name(self,relevant_list,names=None,rpc_js=None,name=None):
        #names,name,rpc_js=self.get_rpc_js_vars(relevant_list,names=names,rpc_js=rpc_js,name=name)
        self.window[self.script_event_js['-NETWORK_NAME-']].update(values=names,value=name)
        name,networks,network,chain_ids,rpcs,rpc,explorers,explorer,symbol=self.get_static_variables(rpc_js)
        self.window[self.script_event_js['-RPC-']].update(values=rpcs,value=rpc)
        self.window[self.script_event_js['-CHAINID-']].update(value=chain_ids)
        self.window[self.script_event_js['-BLOCK_EXPLORER-']].update(values=explorers,value=explorer)
        self.window[self.script_event_js['-SYMBOL-']].update(value=symbol)
    def get_names(self,relevant_list):
        names = [item[0] for item in relevant_list]
        name = self.values[self.script_event_js['-NETWORK_NAME-']]
        if names:
            name=names[0]
            
        if self.script_event_js['found'] in ['-NETWORK_NAME-','-NETWORK-']:
            name = self.values[self.script_event_js['-NETWORK_NAME-']]
            if self.script_event_js['found'] == '-NETWORK-':
                name = get_closest_match_from_list(name,names)
                if name == None and names:
                    name = names[0]
        else:
            if self.query:
                name = get_closest_match_from_list(self.query,names)
        return name, names
    def get_relevant_list(self):
        relevant_list = self.rpc_mainnets
        if self.values[self.script_event_js['-NETWORK-']] == 'Testnet':
            relevant_list = self.rpc_testnets
        self.query = self.values[self.script_event_js['-SEARCH-']]
        if self.query == '' or len(self.query) < len(self.original_query):
            pass
        else:
            relevant_list = [item for item in relevant_list if self.query.lower() in item[0]]
        return relevant_list
    def get_rpc_js(self,relevant_list,name):
        rpc_js = [item for item in relevant_list if str(item.get('name')).lower() == str(name).lower()]
        if rpc_js and isinstance(rpc_js,list):
            rpc_js=rpc_js[0]
        return rpc_js
    def get_back_values(self,num_list,values):
        rpc_values = []
        for num in num_list:
            rpc_values.append(values[num])
        return rpc_values
    def rpc_win_while(self,event,values,window):
        self.event,self.values,self.window=event,values,window
        self.script_event_js = get_event_key_js(self.event,key_list=self.all_keys)
        relevant_list = self.get_relevant_list()
        name, names = self.get_names(relevant_list)
        relevant_list=[item[1] for item in relevant_list]
        rpc_js=self.get_rpc_js(relevant_list,name)
        self.update_network_name(rpc_js=rpc_js,names=names,name=name,relevant_list=relevant_list)
        if self.script_event_js['found'] == '-OK_RPC-':
            self.apply_selected_rpc_settings(self.get_rpc_values(values))
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
    def apply_selected_rpc_settings(self, gui_values):
        """
        Applies the selected RPC settings to the RPC manager based on the GUI values.
        """
        # Extract the necessary information from gui_values
        selected_rpc_js = self.extract_rpc_settings_from_gui(gui_values)
        if selected_rpc_js:
            # Update the RPC manager with the selected settings
            self.rpc_mgr.update_rpc_js(selected_rpc_js)
            # Reinitialize the Web3 instance with the new RPC
            self.rpc_mgr.w3 = Web3(Web3.HTTPProvider(self.rpc_mgr.rpc))

    def extract_rpc_settings_from_gui(self, gui_values):
        # Logic to extract and format the settings from the GUI values
        # Return the formatted settings
        self.rpc_mgr.rpc_js = self.user_selection = gui_values
        return self.rpc_mgr.rpc_js

