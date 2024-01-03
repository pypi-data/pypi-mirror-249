"""
abstract_abis.py - ABIBridge Module

This module defines the `ABIBridge` class, which provides functionality for interacting with Ethereum smart contracts' ABIs (Application Binary Interfaces).
It allows you to retrieve and use contract ABIs, call contract functions, and manage rate limiting for API requests.

Classes:
    ABIBridge: A class to interact with Ethereum smart contract ABIs and functions.

Functions:
    default_rpc: Returns a default RPC configuration dictionary.

Example Usage:
    # Create an instance of ABIBridge
    abi_manager = ABIBridge(contract_address='0x3dCCeAE634f371E779c894A1cEa43a09C23af8d5', rpc=default_rpc())
    
    # Retrieve read-only functions from the contract
    read_only_functions = abi_manager.get_read_only_functions()
    
    # Iterate through each read-only function
    for function_name in read_only_functions:
        inputs = abi_manager.get_required_inputs(function_name)
        if len(inputs) == 0:
            result = abi_manager.call_function(function_name)
            print(function_name, result)
        else:
            print(function_name, inputs)
""" 
# Import necessary modules and classes
from .abstract_apis import APIBridge
from .abstract_rpcs import RPCBridge
from abstract_utilities import create_and_read_json
from abstract_utilities.path_utils import makeAllDirs
import os
from typing import Optional
from .abstract_blockchain_functions import *

# Instantiate the rate limiting manager


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
        api_mgr=api_mgr or APIBridge(api_gui=api_gui)
        self.rpc_mgr = RPCBridge()
        self.w3_mgr=w3_mgr or w3Manager()
    def fetch_abi(self,address=None,rpc_js=None):
        """
        Fetches the ABI for the contract.

        :return: ABI of the contract.
        """
        response = safe_json_loads(derive_network(address=address,initial_network=rpc_js))
    
        return response['contract_data'][0]['ABI']
    def update_rpc_mgr(self,rpc_mgr=None,rpc_js=None):
        self.rpc_mgr=rpc_mgr
        self.rpc_js = rpc_js
        if self.rpc_mgr == None:
            self.rpc_mgr = RPCBridge(rpc_js=self.rpc_js)
        elif self.rpc_js:
            self.rpc_mgr.update_rpc_js(rpc_js=self.rpc_js)
        self.api_mgr.update_rpc(rpc_mgr=rpc_mgr)
    def update_api_mgr(self,api_mgr=None,contract_address=None):
        self.api_mgr = api_mgr
        if self.api_mgr == None:
            self.api_mgr= APIBridge(contract_address=self.contract_address)
        contract_address = contract_address or self.contract_address
        self.api_mgr.contract_address=contract_address
        if contract_address == None:
            contract_address = self.api_mgr.contract_address
        self.contract_address=checksum(self.api_mgr.contract_address)
        self.contract_address = contract_address
  
        source_code=derive_network(address=contract_address)
        self.api_mgr.update_rpc(rpc_js=source_code['network'])
        return self.contract_address
    def create_abi_bridge(self,contract_address,abi=None,rpc_js=None):
        """
        Create a contract bridge using the ABI and contract address.

        :return: Contract bridge instance.
        """
        normalized_address = get_normalized_address(contract_address)
        if normalized_address in self.abi_bridges:
            abi_bridge = self.abi_bridges[normalized_address]
            if abi_bridge:
                return abi_bridge
        contract_address = checksum(address=contract_address,rpc_js=rpc_js)
        
        if rpc_js != None:
            if isinstance(rpc_js,dict):
                name = rpc_js['name']
            elif isinstance(rpc_js,type(self.rpc_mgr)):
                name = self.rpc_mgr.name
            else:
                name = None
        else:
            name = None
        if abi == None:
            abi = self.fetch_abi(address=contract_address,rpc_js=name)
        
        self.abi_bridges[normalized_address]=w3_mgr.retrieve_w3(contract_address).eth.contract(address=contract_address, abi=abi)
        return self.abi_bridges[normalized_address]
    
    def list_contract_functions(self,abi:list=None):
        """
        List all contract functions and their details.

        :return: List of contract function details.
        """
        abi=abi or self.abi
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
    def get_read_only_functions(self, abi:list=None):
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
    def call_function(self,contract_address,function_name:str,*args,**kwargs):
        """
        Calls a read-only function on the contract.

        :param function_name: Name of the function to call.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: Result of the function call.
        """
        contract_bridge = self.create_abi_bridge(contract_address)
        contract_function = getattr(contract_bridge.functions, function_name)
        # If there are positional arguments (regardless of how many), use them.
        if len(args) == 1 and not kwargs:
            return contract_function(args[0]).call()
        elif args and not kwargs:
            return contract_function(*args).call()
        # If there are keyword arguments, use them.
        elif kwargs:
            return contract_function(**kwargs).call()
        # If no arguments, just call the function.
        else:
            return contract_function().call()
    def create_functions(self,contract_address,function_name:str,subsinstance:str="functions",*args, **kwargs):
        contract_bridge = self.create_abi_bridge(contract_address)
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

