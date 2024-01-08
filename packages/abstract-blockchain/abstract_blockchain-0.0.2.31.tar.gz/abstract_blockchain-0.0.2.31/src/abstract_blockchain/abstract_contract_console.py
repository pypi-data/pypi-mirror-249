from abstract_gui import get_push,AbstractWindowManager,make_component
from abstract_rpcs import RPCBridge,RPCGui
from abstract_blockchain.abstract_abis import ABIBridge
from abstract_blockchain.abstract_accounts import ACCTBridge
from abstract_contracts import *
from abstract_blockchain.abstract_blockchain_functions import *
import codecs
abi_mgr = ABIBridge()
rpc_mgr = RPCBridge()
new_bridge_global={}
new_window_mgr = AbstractWindowManager()
def call_function(function_name):
    values = new_window_mgr.get_values()
    inputs = {}
    output_keys= []
    for key, value in values.items():
        if f"-INPUT_{function_name}_" in key:
            input_name = f"{key.split('_')[-2]}"
            input_type = f"{key.split('_')[-1][:-1]}"# Assuming the name of the input is second to the last in the split result
            inputs[input_name] = get_type(input_type,value)
        elif f"-OUTPUT_{function_name}_" in key:
            if key not in output_keys:
                output_keys.append(key)
    try:
        # If there's only one input and it's of type address
        #if len(list(inputs.keys())) == 1:
        #    result = new_bridge_global["abi_manager"].call_function(inputs[list(inputs.keys())[0]],function_name=function_name)
        # For multiple inputs, unpack them as positional arguments
        if inputs:
            args = tuple(inputs.values())  # Convert the dictionary values to a tuple
            contract_bridge = new_bridge_global["abi_manager"].create_functions(*args,function_name=function_name,subsinstance="functions")
        else:
            contract_bridge = new_bridge_global["abi_manager"].create_functions(function_name=function_name,subsinstance="functions")
        if get_funciton_mutability(function_name).lower() in ["pure","view"]:
            result = contract_bridge.call()
        else:
            txn_info = new_bridge_global["account_manager"].build_txn(contract_bridge=contract_bridge)
            result = new_bridge_global["account_manager"].send_transaction(tx_info=txn_info)
        if len(output_keys)>0:
            if len(output_keys) == 1:
                new_window_mgr.update_values(key=output_keys[0], **{"value": str(get_type(output_keys[0].split('_')[-1][:-1],result,output=True))})
            if len(output_keys)>1:
                if not isinstance(result,list):
                    if isinstance(result,str):
                        result=result.split(',')
                    if isinstance(result,set):
                        result=list(result)
                    else:   
                        result = [result]
                for each_output_key in output_keys:
                    num = int(each_output_key[len(f"-OUTPUT_{function_name}_"):].split('_')[0])
                    new_window_mgr.update_values(key=each_output_key, **{"value": str(get_type(each_output_key.split('_')[-1][:-1],result[num],output=True))})
    except Exception as e:
        print(f"Error calling function: {e} \nInputs: {inputs}")
def get_funciton_mutability(function_name):
    for each in new_bridge_global["abi_manager"].abi:
        if each["type"] == "function":
            if each["name"] == function_name:
                return each["stateMutability"]
def contract_win_while(event: str):
    if event == "-CALL_ALL_READ_ONLY-":
        read_only_list = new_bridge_global["abi_manager"].get_read_only_functions()
        for each in read_only_list:
            call_function(each)
    if "-CALL-" in event:
        # Extracting inputs and outputs associated with the function
        call_function(event.split("-")[2])
def win_while(event: str):
    rpc_win_while(event)
    values = new_window_mgr.get_values()
    rpc_manager = get_rpc()
    if event == "-OK_RPC-":
        new_bridge_global["rpc_manager"]=rpc_manager
        print(new_bridge_global["rpc_manager"].rpc_js)
    if event == "-GET_ABI-":
        contract_address = values["-CONTRACT_ADDRESS-"]
        new_bridge_global["abi_manager"] = ABIBridge(contract_address=contract_address, rpc=rpc_manager.rpc_js)
        function_js = {}
        for each in new_bridge_global["abi_manager"].abi:
            if each["type"] == "function":
                if each["stateMutability"] not in function_js:
                    function_js[each["stateMutability"]] = []
                inputs = _parse_io(each.get("inputs", []),function_name=each["name"])
                outputs = _parse_io(each.get("outputs", []), is_output=True,function_name=each["name"])
                layout = inputs + outputs  # Combine inputs and outputs
                button = [make_component("Button", **{"button_text": f"Call {each['name']}", "key": f"-CALL-{each['name']}-"})]
                layout.append(button)
                function_js[each["stateMutability"]].append(
                    make_component("Frame", **{"title": each["name"], "layout": layout})
                )
        # Organizing framed groups with 4 columns per row
        all_layouts = [make_component("Button", **{"button_text": f"Call All Read Only", "key": "-CALL_ALL_READ_ONLY-"})]
        for state, funcs in function_js.items():
            rows = [funcs[i:i+7] for i in range(0, len(funcs), 7)]
            state_layout = []
            for row in rows:
                state_layout.append(row)
            all_layouts.append([make_component("Frame", **{"title": state, "layout": state_layout})])
        new_window = new_window_mgr.get_new_window(title=f"{new_window_mgr.get_values(window=new_bridge_global['main_window'])['-NETWORK_NAME-']} contract {contract_address}", layout=all_layouts, event_function="contract_win_while")
        new_window_mgr.while_basic(window=new_window)
    if event == "-DERIVE_RPC-":
        new_bridge_global["abi_manager"]=derive_network(address=values["-CONTRACT_ADDRESS-"],initial_network=rpc_js)
        rpc = new_bridge_global["abi_manager"].rpc_manager.rpc_js
        if isinstance(rpc,dict):
            for key,value in rpc.items():
                new_window_mgr.update_values(key=get_rpc_js()[key],**{"value":value})
    if event == "-ASSOCIATE_ACCOUNT-":
        new_bridge_global["account_manager"] = ACCTBridge(env_key=values["-ACCOUNT_ENV_KEY-"],rpc=get_rpc())
        new_window_mgr.update_values(key="-ACCOUNT_ADDRESS-",**{"value":new_bridge_global["account_manager"].account_address})
def _parse_io(io_data,function_name:str, is_output=False):
    layout = []
    for i, io_type in enumerate(io_data):
        text = f"{io_type['name']}({io_type['type']}): "
        key_suffix = "OUTPUT" if is_output else "INPUT"
        key = f"-{key_suffix}_{function_name}_{i}_{io_type['name']}_{io_type['type']}-"
        component_type="Input"
        size = (get_size(io_type['type']), 1)
        if io_type['type'].lower() in ["bytes","string"]:
            component_type = "Multiline"
            size = (get_size(io_type['type']), 3)
        if is_output:
            layout.append([make_component("Text", **{"text": text}),get_push(), make_component(component_type, **{"size": size,"key": key, "disabled": True})])
        else:
            layout.append([make_component("Text", **{"text": text}),get_push(),  make_component(component_type, **{"size": size, "key": key})])
    return layout
def get_account_layout():
    frame_layout = [[make_component("Text", **{"text": "ENV Key:"}),get_push(),make_component("Input",**{"key":"-ACCOUNT_ENV_KEY-"})],
                    [make_component("Text", **{"text": "Account Address"}),get_push(),make_component("Input",**{"default_text":"No Address Found","key":"-ACCOUNT_ADDRESS-","disabled":True})],
                    [make_component("Button", **{"button_text":"Associate Account","enable_events":True,"key":"-ASSOCIATE_ACCOUNT-"})]]
    return [make_component("Frame", "Account", **{"layout":frame_layout})]
# If you need the ABI helper function in the new script, define it here 
def get_abi():
    frame_layout = [make_component("Input",**{"key":"-CONTRACT_ADDRESS-"}),
                    make_component("Button", **{"button_text":"GET ABI","enable_events":True,"key":"-GET_ABI-"}),
                    make_component("Button", **{"button_text":"DERIVE RPC","enable_events":True,"key":"-DERIVE_RPC-"})]
    return make_component("Frame", "ABI", frame_layout)
def get_rpc():
    rpc={}
    rpc_js = get_rpc_js()
    for rpc_key,window_key in rpc_js.items():
        rpc[rpc_key] = new_window_mgr.get_values(window=new_bridge_global["main_window"])[window_key]
    return RPCBridge(rpc)
def determine_correct_rpc(contract_address,rpc_js):
    return derive_network(address=None,initial_network=rpc_js)
def abstract_contract_console_main(rpc_list:list=None):
    rpc_list = rpc_list or get_default_rpc_list()
    new_bridge_global["rpc_list"]=rpc_list
    # Get the rpc_layout and other associated values
    rpc_layout= [[make_component("Frame", "RPC_LAY",**{"layout":RPCGui(rpc_gui=False).get_rpc_layout()})]]
    # Construct the final layout
    new_layout = [[get_account_layout()],get_abi(),rpc_layout]
    # Create and run the window
    
    new_window = window_mgr.add_window(title="New Blockchain Console", layout=[new_layout], event_function=win_while)
    new_window_mgr.while_window(window=new_window)

abstract_contract_console_main()
