from .abstract_apis import APIBridge,APIGUI
from .abstract_rpcs import RPCBridge,RPCGUIManager
from abstract_blockchain_functions import *
from abstract_utilities import make_list,safe_json_loads,safe_dump_to_file,safe_read_from_json,create_and_read_json
import json
from typing import Optional
class ABIBridge:
    """


    ABIBridge class provides functionality to interact with Ethereum smart contract ABIs and functions.
    """

    def __init__(self, address: Optional[str] = None, api_mgr=None, api_gui: bool = False, rpc_js: Optional[dict] = None,w3_mgr=None):
        """
        Initializes the ABIBridge instance.

        :param address: Ethereum contract address. Default is None.
        :param api_mgr: API manager instance. Default is None.
        :param api_gui: Boolean flag for API GUI. Default is False.
        :param rpc_js: RPC configuration dictionary. Default is an empty dictionary.
        """
        # Use os.path.join for path concatenation to ensure cross-platform compatibility
        self.abi_bridges = {}
        self.w3_mgr=w3_mgr or w3Manager()
    def fetch_abi(self,address=None,rpc_js=None):
        """
        Fetches the ABI for the contract.

        :return: ABI of the contract.
        """
        response = safe_json_loads(derive_network(address=address,initial_network=rpc_js))
    
        return response['contract_data'][0]['ABI']
    def get_abi_data(self,address=None):
        address=address or self.address
        if address:
            abi = self.fetch_abi(address)
            self.contract_functions = self.list_contract_functions(address)
            return abi
    def create_abi_bridge(self, address, abi=None, rpc_js=None):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.abi_bridges:
            self.update_abi_bridge(address=address,abi=abi,rpc_js=rpc_js)
        return self.abi_bridges[normalized_address]
    def update_abi_bridge(self,address,abi=None,rpc_js=None):
        normalized_address = get_normalized_address(address)
        rpc = rpc_js.get('user_settings',rpc_js)
        if rpc and rpc.get('rpc'):
            address = checksum(address=address, rpc=rpc.get('rpc'))
        else:
            address = checksum(address=address, rpc=rpc)
        abi = abi or self.get_abi_data(address=address)
        self.abi_bridges[normalized_address] = self.w3_mgr.create_w3(address=address, rpc=rpc).eth.contract(address=address, abi=abi)
    def list_contract_functions(self,address,abi:list=None):
        """
        List all contract functions and their details.

        :return: List of contract function details.
        """
        abi=abi or self.fetch_abi(address=address)
        if isinstance(abi,list):
            functions = []
            if abi != None:
                for item in abi:
                    if item.get('type') == 'function':
                        function_details = {
                            "name": item.get('name'),
                            "inputs": [(i.get('name'), i.get('type')) for i in item.get('inputs')],
                            "outputs": [(o.get('name'), o.get('type')) for o in item.get('outputs')]
                        }
                        functions.append(function_details)
            self.contract_functions = functions
            return self.contract_functions
    def get_read_only_functions(self, address,abi:list=None):
        """
        Get a list of read-only functions from the ABI.

        :param abi: ABI to analyze (default is None, uses instance ABI).
        :return: List of read-only function names.
        """
        abi=abi or self.abi
        if isinstance(abi,list):
            read_only_functions = []
            for item in abi:
                if item.get('type') == 'function' and item.get('stateMutability') in ['view','pure']:
                    read_only_functions.append(item.get('name'))
            return read_only_functions

    def get_required_inputs(self, function_name: str, abi: list = None):
        """
        Get the required inputs for a specific function from the ABI.

        :param function_name: Name of the function.
        :param abi: ABI to analyze (default is None, uses instance ABI).
        :return: List of required inputs for the function.
        """
        abi=abi or self.abi
        if isinstance(abi,list):
            for item in abi:
                if item.get('type') == 'function' and item.get("name") == function_name:
                    return item.get("inputs")
    def call_function(self, address, function_name, *args, **kwargs):
        contract_bridge = self.create_abi_bridge(address)
        contract_function = getattr(contract_bridge.functions, function_name)

        if len(args) == 1 and not kwargs:
            return contract_function(args[0]).call()
        elif args and not kwargs:
            return contract_function(*args).call()
        elif kwargs:
            return contract_function(**kwargs).call()
        else:
            return contract_function().call()
    def create_functions(self,*args,function_name:str,subsinstance:str="functions",contract_bridge=None, **kwargs):
        contract_bridge = contract_bridge or self.contract_bridge
        # Access the subsinstance (like "functions" in the contract)
        sub_instance = getattr(contract_bridge, subsinstance)  # use self.contract_bridge
            
        # Get the desired function from the subsinstance
        contract_function = getattr(sub_instance, function_name)

        # If there's only one positional argument and no keyword arguments, use it directly.
        # Otherwise, use kwargs as named arguments.
        if len(args) == 1 and not kwargs:
            return contract_function(args[0])
        elif args and not kwargs:
            return contract_function(*args)
        # If there are keyword arguments, use them.
        elif kwargs:
            return contract_function(**kwargs)
        # If no arguments, just call the function.
        else:
            return contract_function()
class abstractBlockchainManager:
    def __init__(self,rpc_mgr=None,api_mgr=None,abi_mgr=None,w3_mgr=None):
        self.w3_mgr=w3_mgr or w3Manager()
        self.script_path = os.path.abspath(__file__)
        self.directory_path = os.path.dirname(self.script_path)
        self.data_path = makeAllDirs(os.path.join(self.directory_path,'data'))
        self.manager_key_path= makeAllDirs(os.path.join(self.data_path,'manager_keys.json'))
        os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(get_directory_path(), 'data'),exist_ok=True)
        os.makedirs(os.path.join(get_data_directory(), 'source_codes'),exist_ok=True)
        self.address_manager=create_and_read_json(file_path=self.manager_key_path,data={})
        self.rpc_mgr = rpc_mgr
        if self.rpc_mgr == None:
            self.rpc_mgr=RPCBridge()
        self.api_mgr = api_mgr
        if self.api_mgr == None:
            self.api_mgr=APIBridge()
        self.abi_mgr=abi_mgr
        if self.abi_mgr == None:
            self.abi_mgr=ABIBridge(w3_mgr=self.w3_mgr)
    def derive_address_values(self,address,rpc_js=None):
        source_code_directory = get_source_code_path(address)
        source_code_path = os.path.join(source_code_directory,'source_code.json')
        dict_info_path = os.path.join(source_code_directory,'dict_info.json')
        rpc_path = os.path.join(source_code_directory,'rpc_data.json')
        source_code = read_json(file_path=source_code_path)
        rpc_js = read_json(file_path=rpc_path)
        self.w3_mgr.create_w3(address,rpc=rpc_js)
        abi=source_code[0]['ABI']
        self.get_bridge(address,abi=abi)
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
    def get_contract_info(self,address):
        normalized_address = get_normalized_address(address=address)
        if normalized_address not in self.address_manager:
            self.derive_address_values(address)
        return self.address_manager[normalized_address]
    def get_bridge(self,address):
        contract_info = self.get_contract_info(address)
        return self.abi_mgr.create_abi_bridge(address,abi=contract_info['abi'],rpc_js=contract_info['rpc_js'])
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
