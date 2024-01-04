from .abstract_rpcs import RPCBridge
from .abstract_apis import APIBridge
from eth_account import Account
from itertools import zip_longest
from .abstract_wallets import AbstractWallets
from abstract_utilities.type_utils import if_default_return_obj,is_number
from abstract_security import get_env_value
from .abstract_blockchain_functions import *
class ACCTBridge:
    def __init__(self, env_keys=[], wallets=[],rpc=None):
        self.rpc_manager = RPCBridge(rpc_js=rpc)
        self.web3 = self.rpc_manager.w3
        self.addresses=[wallet.get('add') for wallet in wallets]
        self.env_keys = [wallet.get('env') for wallet in wallets]
        self.account_names = [wallet.get('name') for wallet in wallets]
        self.wallets = self._init_wallets(env_keys=env_keys, addresses=self.addresses,account_names=self.account_names)
        self.wallet_mgr = AbstractWallets()
    def _init_wallets(self, env_keys, addresses,account_names):
        self.env_keys=env_keys or []
        self.addresses=addresses or []
        self. account_names = account_names or []
        
        return [
            {
                'private_key': self.check_priv_key(key),
                'address': self.get_address_from_key(self.check_priv_key(key)) or addr,
                'account_name': 'default_account_name',
            }
            for key, addr in zip_longest(self.env_keys, self.addresses, fillvalue=None)
        ]
    def add_wallet(self, create_new_wallet=False,env_key=None, address=None,account_name=None):
        """
        Adds a new wallet to the ACCTBridge.

        :param env_key: Environment key for the wallet's private key.
        :param address: The address of the wallet.
        """
        new_wallet={}
        private_key=None
        account_name = account_name or account_name or f'default_name_{len(self.wallets)}'
        if create_new_wallet:
            wallet = self.wallet_mgr.add_wall(name=account_name)
            private_key = wallet.get('priv')
            address= wallet.get('add')
            account_name=wallet.get('name')
        if env_key:
            if address is None:
                address= self.get_address_from_key(self.check_priv_key(env_key))
            private_key=private_key or self.check_priv_key(env_key)
        else:
            if private_key:
                self.get_address_from_key(private_key)
        if private_key:
            new_wallet = {
                'private_key': private_key,
                'address': address,
                'name': account_name
            }
            self.wallets.append(new_wallet)
        return new_wallet
    def remove_wallet(self, wallet_index):
        """
        Removes a wallet from the ACCTBridge by its index.

        :param wallet_index: Index of the wallet to remove.
        """
        if 0 <= wallet_index < len(self.wallets):
            del self.wallets[wallet_index]
        else:
            raise IndexError("Wallet index out of range.")

    def update_wallet(self, wallet_index, env_key=None, address=None,name=None):
        """
        Updates the details of an existing wallet.

        :param wallet_index: Index of the wallet to update.
        :param env_key: New environment key for the wallet's private key.
        :param address: New address of the wallet.
        """
        if 0 <= wallet_index < len(self.wallets):
            if env_key is not None:
                self.wallets[wallet_index]['private_key'] = self.check_priv_key(env_key)
                self.wallets[wallet_index]['address'] = self.get_address_from_key(self.check_priv_key(env_key))
            if address is not None:
                self.wallets[wallet_index]['address'] = address
            if account_name is not None:
                self.wallets[wallet_index]['name'] = account_name
        else:
            raise IndexError("Wallet index out of range.")
    def check_priv_key(self,private_key):
        obj = get_env_value(key=private_key)
        return obj if obj else private_key
   
    def get_address_from_key(self,private_key: str) -> str:
        if private_key:
            account = Account.from_key(private_key)
            return self.try_check_sum(account.address)
        return 
    def build_txn(self, contract_bridge,from_address:str=None,to_address:str=None,txn_value:int=None,gasPrice:int=None,gas:int=None):
        return contract_bridge.build_transaction(self.get_txn_info(from_address=from_address,to_address=to_address,txn_value=txn_value,gasPrice=gasPrice,gas=gas))
    def get_txn_info(self, to_address:str=None,from_address:str=None,txn_value:int=None,gasPrice:int=None,gas:int=None):
        from_address = str(self.try_check_sum(if_default_return_obj(obj=self.account_address,default=from_address)))
        if not is_number(gasPrice):
            if isinstance(gasPrice,str):
                gasPrice = self.estimate_gas(gas_strategy=gasPrice)
        gas_price = if_default_return_obj(obj=self.estimate_gas(),default=gasPrice)
        if not is_number(gas):
            if isinstance(gas,str):
                gas = self.estimate_gas(gas_strategy=gasPrice)
        gas = if_default_return_obj(obj=self.estimate_gas(gas_strategy="suggestBaseFee"),default=gas)
        txn_info = {
            'from': from_address,
            'gasPrice':gas_price,
            'gas': gas,
            'nonce': self.nonce,
            'chainId': self.rpc_manager.chain_id,
            'nonce':self.nonce}
        if txn_value != None:
            txn_info["value"]=txn_value
        if to_address != None:
            txn_info["to"] = str(self.try_check_sum(to_address))
        return txn_info
    def check_sum(self, address:str=None):
        """
        Convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        """
        #address = if_default_return_obj(obj=self.get_address_from_private_key(self.private_key),default=address)
        return self.rpc_manager.w3.to_checksum_address(address)
    def try_check_sum(self, address:str=None):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        #address = if_default_return_obj(obj=self.get_address_from_private_key(self.private_key),default=address)
        try:
            address = self.check_sum(address)
            return address
        except:
            raise ValueError("Invalid Ethereum Address")
    def get_transaction_count(self, wallet_index=0):
        address = self.wallets[wallet_index]['address']
        return self.web3.eth.get_transaction_count(address)

    def sign_transaction(self, tx_info, wallet_index=0):
        private_key = self.wallets[wallet_index]['private_key']
        return self.web3.eth.account.sign_transaction(tx_info, private_key)
    def send_transaction(self, tx_info, private_key:str=None):
        signed_txn = self.sign_transaction(tx_info=tx_info, private_key=self.check_priv_key(if_default_return_obj(obj=self.private_key,default=private_key)))
        return self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    def estimate_gas(self,gas_strategy:str="safe"):
        api_manager = APIBridge(api_data="module=gastracker&action=gasoracle",rpc=self.rpc_manager.rpc_js)
        for key in api_manager.response.keys():
            if gas_strategy.lower() in key.lower():
                response = api_manager.response[key]
                if key == "suggestBaseFee":
                    return int(float(response)*1000)
                return self.web3.to_wei(int(response), 'gwei')
