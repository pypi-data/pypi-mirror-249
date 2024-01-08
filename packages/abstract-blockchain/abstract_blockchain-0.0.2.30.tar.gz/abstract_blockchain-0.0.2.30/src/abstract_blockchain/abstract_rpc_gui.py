from abstract_gui import AbstractWindowManager,sg,make_component,create_row_of_buttons,text_to_key,get_event_key_js
from .abstract_rpcs import RPCBridge
from .rpc_functions import *
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
