from .abstract_apis import APIBridge,APIGui
from .abstract_rpcs import RPCBridge,RPCGui
from .abstract_abis import ABIBridge
from .abstract_wallets import AbstractWallets
from .abstract_accounts import ACCTBridge
from .abstract_blockchain_functions import *
from abstract_utilities import safe_dump_to_file,create_and_read_json
class abstractBlockchainManager:
    def __init__(self,rpc_mgr=None,api_mgr=None,abi_mgr=None,w3_mgr=None,acct_mgr=None,wall_mgr=None,rpc_gui_mgr=None,api_gui_mgr=None,rpc_gui=False):
        
        self.script_path = os.path.abspath(__file__)
        self.directory_path = os.path.dirname(self.script_path)
        self.data_path = makeAllDirs(os.path.join(self.directory_path,'data'))
        self.manager_key_path= makeAllDirs(os.path.join(self.data_path,'manager_keys.json'))
        os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(get_directory_path(), 'data'),exist_ok=True)
        os.makedirs(os.path.join(get_data_directory(), 'source_codes'),exist_ok=True)
        self.address_manager=create_and_read_json(file_path=self.manager_key_path,data={})
        self.w3_mgr = w3_mgr
        if self.w3_mgr == None:
            self.w3_mgr = w3Manager()
        self.rpc_mgr = rpc_mgr
        if self.rpc_mgr == None:
            self.rpc_mgr=RPCBridge()
        self.api_mgr = api_mgr
        if self.api_mgr == None:
            self.api_mgr=APIBridge()
        self.abi_mgr=abi_mgr
        if self.abi_mgr == None:
            self.abi_mgr=ABIBridge()
        self.acct_mgr = acct_mgr
        if self.acct_mgr == None:
            self.acct_mgr = ACCTBridge()
        self.wall_mgr = wall_mgr
        if self.wall_mgr == None:
            self.wall_mgr = AbstractWallets()
        self.rpc_gui_mgr = rpc_gui_mgr
        if self.rpc_gui_mgr == None:
            self.rpc_gui_mgr = RPCGui(rpc_gui=rpc_gui)
        self.api_gui_mgr = api_gui_mgr
        if self.api_gui_mgr == None:
            self.api_gui_mgr = APIGui()
    def derive_address_values(self,address,rpc_js=None):
        source_code_directory = get_source_code_path(address)
        source_code_path = os.path.join(source_code_directory,'source_code.json')
        dict_info_path = os.path.join(source_code_directory,'dict_info.json')
        rpc_path = os.path.join(source_code_directory,'rpc_data.json')
        source_code = read_json(file_path=source_code_path)
        rpc_js = read_json(file_path=rpc_path)
        self.w3_mgr.create_w3(address,rpc=rpc_js)
        abi=source_code[0]['ABI']
        
        normalized_address = get_normalized_address(address)
        contract_info={"normalized_address":normalized_address,
                                                  "checksum_address":address,
                                                  "rpc_js":rpc_js,
                                                  "dict_info_path":dict_info_path,
                                                  "rpc_path":rpc_js,
                                                  "source_code_path":source_code_path,
                                                  "source_code_directory":source_code_directory,
                                                  "function_calls":{},"abi":abi}
        self.update_contract_info(normalized_address,contract_info)
        self.abi_mgr.create_abi_bridge(contract_address=contract_info['checksum_address'],abi=contract_info['abi'],rpc_js=contract_info['rpc_js'])
    def get_contract_info(self,address):
        normalized_address = get_normalized_address(address=address)
        if normalized_address not in self.address_manager:
            self.derive_address_values(address)
        return self.address_manager[normalized_address]
    def get_bridge(self,address):
        contract_info = self.get_contract_info(address)
        return self.abi_mgr.create_abi_bridge(address=contract_info['checksum_address'],abi=contract_info['abi'],rpc_js=contract_info['rpc_js'])
    def update_contract_info(self,address,contract_info):
        normalized_address = get_normalized_address(address=address)
        old_contract_info={}
        for key,value in contract_info.items():
            old_contract_info[key] = value
        self.address_manager[normalized_address]=old_contract_info
        safe_dump_to_file(file_path = self.address_manager[normalized_address]["dict_info_path"],data=self.address_manager[normalized_address])
        safe_dump_to_file(file_path=self.manager_key_path,data=self.address_manager)
    def change_rpc_selection(self,address):
         contract_info = self.get_contract_info(address)
         rpc_gui_mgr = RPCGUIManager(rpc_js=contract_info['rpc_js'])
         contract_info['rpc_js'] = rpc_gui_mgr.rpc_values
         self.update_contract_info(address,contract_info)
         self.rpc_mgr.rpc_js = contract_info['rpc_js']
         self.w3_mgr.create_w3(address, rpc=self.rpc_mgr.rpc_js)
         self.abi_mgr.update_abi_bridge(address,rpc_js=self.rpc_mgr.rpc_js)
    def call_function(self,address,function_name,*args):
        contract_info = self.get_contract_info(address)
        if function_name not in contract_info:
            contract_info['function_calls'][function_name] = []
        response = self.abi_mgr.call_function(address,function_name,*args) 
        contract_info['function_calls'][function_name].append({'args':args,'response':response})
        self.update_contract_info(address,contract_info)
        return response

