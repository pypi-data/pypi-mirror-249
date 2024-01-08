from .rpc_functions import *
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

