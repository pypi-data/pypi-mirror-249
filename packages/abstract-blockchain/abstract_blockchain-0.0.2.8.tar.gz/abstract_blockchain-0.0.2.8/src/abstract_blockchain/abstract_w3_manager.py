from .abstract_rpcs import RPCBridge
from web3 import Web3
class w3Manager:
    def __init__(self):
        self.w3_management = {}
        self.default_rpc_js = get_default_rpc(Network_Name="Ethereum")  # Assuming get_default_rpc is defined elsewhere
        self.default_rpc_mgr = RPCBridge(rpc_js=self.default_rpc_js)  # Assuming get_new_rpc_bridge is defined elsewhere
        self.default_w3 = self.default_rpc_mgr.w3

    def add_to_list(self, address, w3=None, rpc=None,rpc_js=None):
        normalized_address = get_normalized_address(address)
        if not w3 and rpc:
            w3 = self.create_w3(address, rpc=rpc)
        self.w3_management[normalized_address] = {'w3': w3 or self.default_w3, 'rpc': rpc or self.default_rpc_mgr.rpc,'rpc_js':rpc_js or self.default_rpc_js}

    def retrieve_w3(self, address):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        return self.w3_management[normalized_address]['w3']
    def retrieve_rpc(self, address):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        return self.w3_management[normalized_address]['rpc']
    def retrieve_rpc_js(self, address):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        return self.w3_management[normalized_address]['rpc_js']
    def create_w3(self, address, rpc=None):
        if isinstance(rpc, dict):
            self.ammend_to_list(get_normalized_address(address), ['rpc_js'], [rpc])
            rpc = rpc.get('user_settings', rpc.get('rpc', self.default_rpc_mgr.rpc))
            if rpc and 'rpc' in rpc and isinstance(rpc,dict):
                rpc=rpc.get('rpc')
            
        elif rpc is None:
            rpc = self.default_rpc_mgr.rpc

        try:
            new_w3 = Web3(Web3.HTTPProvider(rpc))
            self.ammend_to_list(address, ['w3', 'rpc'], [new_w3, rpc])
            return new_w3
        except Exception as e:
            print(f"Error creating w3 from rpc {rpc}: {e}")
            self.add_to_list(address)  # Fallback to default w3
            return self.default_w3

    def ammend_to_list(self, address, keys, values):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        for i, key in enumerate(keys):
            self.w3_management[normalized_address][key] = values[i]
