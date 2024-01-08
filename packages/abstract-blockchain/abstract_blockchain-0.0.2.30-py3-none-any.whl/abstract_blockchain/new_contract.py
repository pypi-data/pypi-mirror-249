from abstract_gui import get_push,AbstractWindowManager,make_component
from abstract_blockchain.abstract_rpcs import RPCBridge,RPCGui
from abstract_blockchain.abstract_abis import ABIBridge
from abstract_blockchain.abstract_accounts import ACCTBridge
from abstract_blockchain.abstract_contracts import *
from abstract_blockchain.abstract_wallets import AbstractWallets
from abstract_blockchain.abstract_blockchain_functions import *
import codecs
from eth_account import Account
from abstract_security import get_env_value
class ContractConsole:
    def __init__(self):
        self.abi_mgr = ABIBridge()
        self.rpc_mgr = RPCBridge()
        self.acct_mgr = ACCTBridge()
        self.new_bridge_global={}
        self.window_mgr = AbstractWindowManager()
        self.wallet_mgr = AbstractWallets()
        self.window_name = self.window_mgr.add_window(title="New Blockchain Console", layout=[[[self.get_abi()],[self.get_account_layout()],[RPCGui(rpc_gui=False).get_rpc_layout()]]], event_handlers=[self.while_win])
        self.window_mgr.while_window(window_name=self.window_name)
    def get_account_layout(self):
        frame_layout = [[make_component("Text", **{"text": "ENV Key:"}),get_push(),make_component("Input",key="-ACCOUNT_ENV_KEY-",enable_events = True)],
                        [make_component("Text", **{"text": "Account Address"}),get_push(),make_component("Combo",[],default_text="No Address Found",key="-ACCOUNT_ADDRESS-",enable_events=True,size=(get_size('address'),1))],
                        [make_component("Text", **{"text": "Wallet Name:"}),get_push(),make_component("Input",key="-ACCOUNT_NAME-",enable_events = True)],
                        [make_component("Button", **{"button_text":"Associate Account","enable_events":True,"key":"-ASSOCIATE_ACCOUNT-"}),
                         make_component("Button", **{"button_text":"Name Account","enable_events":True,"key":"-ESTABLISH_ACCOUNT_NAME-"}),
                         make_component("Button", **{"button_text":"Create Wallet","enable_events":True,"key":"-CREATE_NEW_WALLET-"})]]
        return [make_component("Frame", "Account", **{"layout":frame_layout})]
    # If you need the ABI helper function in the new script, define it here 
    def get_abi(self):
        frame_layout = [make_component("Input",**{"key":"-CONTRACT_ADDRESS-"}),
                        make_component("Button", **{"button_text":"GET ABI","enable_events":True,"key":"-GET_ABI-"}),
                        make_component("Button", **{"button_text":"DERIVE RPC","enable_events":True,"key":"-DERIVE_RPC-"})]
        return make_component("Frame", "ABI", frame_layout)
    def get_rpc(self):
        rpc={}
        rpc_js = get_rpc_js()
        for rpc_key,window_key in rpc_js.items():
            rpc[rpc_key] = window_mgr.get_values(window=new_bridge_global["main_window"])[window_key]
        return RPCBridge(rpc)
    def determine_correct_rpc(self,contract_address,rpc_js):
        return derive_network(address=None,initial_network=rpc_js)
    def abstract_contract_console_main(self,rpc_list:list=None):
        rpc_list = rpc_list or get_default_rpc_list()
        new_bridge_global["rpc_list"]=rpc_list
        # Get the rpc_layout and other associated values
        rpc_layout= [[make_component("Frame", "RPC_LAY",**{"layout":RPCGui(rpc_gui=False).get_rpc_layout()})]]
        # Construct the final layout
        new_layout = [[get_account_layout()],get_abi(),rpc_layout]
        # Create and run the window
        new_window = window_mgr.add_window(title="New Blockchain Console", layout=[new_layout], event_function=win_while)
        window_mgr.while_window(window=new_window)
    def update_wallet_name(self,new_name,address=None):
        if address == None:
            address = self.values["-ACCOUNT_ADDRESS-"]
        wallet_index = [i for i in enumerate(acct_mgr.wallets) if wallet['address'].lower() == address.lower()]
        if wallet_index:
            wallet_index=wallet_index[0]
        
        name = [wallet['account_name'] for wallet in acct_mgr.wallets if wallet['address'].lower() == address.lower()]
        if name:
            name = name[0]
            self.window["-ACCOUNT_NAME-"].update(name)
        self.acct_mgr.update_wallet(wallet_index,account_name=new_name)
    def while_win(self,event,values,window):
        self.event,self.values,self.window=event,values,window
        if event == "-ESTABLISH_ACCOUNT_NAME-":
            self.update_wallet_name(self.values["-ACCOUNT_NAME-"])
        if event == "-ACCOUNT_ADDRESS-":
            address = self.values["-ACCOUNT_ADDRESS-"]
            name = [wallet['name'] for wallet in self.acct_mgr.wallets if wallet['address'].lower() == address.lower()]
            self.window["-ACCOUNT_NAME-"].update(name)
            
        if event == "-CREATE_NEW_WALLET-":
            wallet = self.acct_mgr.add_wallet(create_new_wallet=True)
            #wallet_info = [(wallet['name'],wallet['address']) for wallet in self.acct_mgr.wallets if wallet['address'].lower() == wallet.get('address').lower()]
            self.window["-ACCOUNT_ADDRESS-"].update(values=[wallet['address'] for wallet in self.acct_mgr.wallets],value=wallet.get('address'))
            self.window["-ACCOUNT_NAME-"].update(wallet.get('name','default_name'))
        if event == "-ACCOUNT_ENV_KEY-":
            env_key = values["-ACCOUNT_ENV_KEY-"]
            env_value = get_env_value(env_key)
            if env_value:
                #account = Account.from_key(env_value)
                #address = checksum(account.address)
                try:
                    wallet=acct_mgr.add_wallet(env_key=env_value)
                    self.window["-ACCOUNT_ADDRESS-"].update(values=addresses,value=wallet.get('address'))
                    self.window["-ACCOUNT_NAME-"].update(wallet.get('name','default_name'))
                except Exception as e:
                    print(f"unable to access the wallet with the env_key {env_key}: {e}")
                
        if event == "-GET_ABI-":
            bridge = ABIBridge().create_abi_bridge(contract_address =values["-CONTRACT_ADDRESS-"])
            input(bridge.functions.symbols)
ContractConsole()
