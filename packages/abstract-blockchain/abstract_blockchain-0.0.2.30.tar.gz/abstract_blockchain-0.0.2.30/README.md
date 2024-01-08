## Abstract Blockchain

Abstract Blockchain is a Python package designed to streamline and simplify interactions with blockchain networks and smart contracts. It consists of various utilities that enable users to manage RPC parameters, work with smart contract ABIs, and facilitate user-friendly interactions using graphical user interfaces (GUIs).

## Available Modules

- **abstract_abis.py**: This module provides the `ABIBridge` class, an interface to Ethereum smart contract ABIs. It allows interactions with contract functions and retrieves read-only functions. Additionally, it categorizes RPC parameters for easier blockchain interaction.

- **abstract_apis.py**: Houses the `APIBridge` class for managing API URL creation and their respective calls. It contains GUI-enabled tools to build API URLs or fetch preselected call parameters.

- **abstract_rpcs.py**: This module offers the `RPCBridge` class that manages the RPC parameters for different blockchain networks. It provides a GUI for filtering and selecting RPC parameters and organizes them for easy use.

- **abstract_accounts.py**: The `ACCTBridge` class in this module allows interfacing with your personal wallet. You can build transaction information, derive public keys, and send/verify transactions.

- **abstract_contract_console.py**: This section of the module integrates all classes for a harmonious interaction with smart contracts.

- **abstract_gui.py** : This submodule provides utilities for creating GUIs that enhance user interaction with blockchain-related features.

- **main.py**: This is the entry point of the package where files are uploaded.

## Installation

The package is available on [PyPI](https://pypi.org/project/abstract-blockchain/). You can install it using pip with `pip install abstract-blockchain`.

The package is available on [PyPI](https://pypi.org/project/abstract-blockchain/). You can install it using pip with `pip install abstract-blockchain`.
![Screenshot from 2023-09-11 09-46-43](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/ae2017c7-542d-4353-be3d-9c71945bb3ab)
![Screenshot from 2023-09-11 09-46-37](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/a102e01c-cee0-4c55-903f-bf490be74ae4)
![Screenshot from 2023-09-04 05-07-39](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/70df9d24-62d0-4172-8870-b0df272748ce)
![Screenshot from 2023-09-04 05-07-06](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/002cd61a-427b-4642-8d4d-14594cf22cd1)

## Example Usage

```python
from abstract_abis import ABIBridge
from abstract_apis import Choose_RPC_Parameters_GUI, RPCData

# Example usage of ABIBridge
abi_manager = ABIBridge(contract_address='0x3dCCeAE634f371E779c894A1cEa43a09C23af8d5', rpc=default_rpc())
read_only_functions = abi_manager.get_read_only_functions()
for each in read_only_functions:
    inputs = abi_manager.get_required_inputs(each)
    if len(inputs) == 0:
        result = abi_manager.call_function(each)
        print(each, result)
    else:
        print(each, inputs)

# Example usage of RPCData and GUI
rpc_data = Choose_RPC_Parameters_GUI()
rpc_manager = RPCData(rpc_data)
w3 = rpc_manager.w3

# Your blockchain interactions using w3...
```

## Installation

The `abstract_blockchain` package can be installed using pip:

```bash
pip install abstract_blockchain
```


## Module - abstract_accounts.py

This module, under the `abstract_blockchain` package, includes the `ACCTBridge` class, providing an interface to the user's personal wallet. It interacts with Ethereum accounts, allowing the user to perform transactions, estimate gas, retrieve transaction counts, sign and send transactions, and handle Ethereum addresses.

The module primarily leverages other modules and classes from `abstract_rpcs.py` and `abstract_apis.py`, requiring the `eth_account` package to interact with Ethereum accounts.

The critical methods within the `ACCTBridge` class include:

- `__init__`: Initializes the `ACCTBridge` object, establishing an RPC bridge for interaction and retrieves the private key and account address.

- `check_priv_key` & `get_address_from_private_key`: Manages operations related to the private key and converts it into an Ethereum address.

- `build_txn` & `get_txn_info`: Allows the user to build a transaction, accounting for multiple variables.

- `check_sum` & `try_check_sum`: Manages the conversion of the address to a checksum address.

- `get_transaction_count`: Fetches the transaction count of the Ethereum account.

- `sign_transaction` & `send_transaction`: Handles the signing and sending of transactions.

- `estimate_gas`: Estimates the gas fee for Ethereum transactions.

The module employs a rate limiting manager to manage the frequency of requests, preventing the exceeding of API rate limits.
## Module - abstract_abis.py

Part of the `abstract_blockchain` package, the `abstract_abis.py` module is a critical component intended to streamline interactions with Ethereum smart contracts, providing a Pythonic interface to their Application Binary Interfaces (ABIs). The core of this module is the `ABIBridge` class, which offers an encompassing interface for managing Ethereum contract ABIs.

Just like the `abstract_accounts.py` module, `abstract_abis.py` performs various tasks in collaboration with other modules, principally `abstract_rpcs.py` and `abstract_apis.py`.

It houses several methods responsible for:

- `Validating` Ethereum addresses
- Creating `ABI bridges`
- `Enumerating` contract functions
- `Accessing` read-only functions from contract ABIs
- `Invoking` contract functions
- `Acquiring` and `categorizing` RPC parameters that are crucial for interaction with the blockchain
- `Managing` rate limiting for API requests

The `ABIBridge` class also emphasizes contracts' functions, offering tools to list all functions, obtain necessary input details, and invoke functions smoothly. It also provides mechanisms to create functions ready to be executed in future operations.

A default_rpc() function is also included, providing a default RPC configuration used when an instance of ABIBridge is created. This function underlines how to utilize the ABIBridge class for tasks like interacting with Ethereum contracts, managing user interaction, retrieving read-only functions, obtaining required input details, and invoking contract functions.
# Module - abstract_api_gui.py

Part of the `abstract_blockchain` package, `abstract_api_gui.py` is a module that builds a Graphical User Interface (GUI) to simplify interactions with APIs. This module utilises `PySimpleGUI` for creating the GUI, and `abstract_utilities.list_utils` for utility functions. The primary features of this module include:

- Declaring hard-coded API descriptions through `apiCallDesc`
- Defining options for API actions using `options`
- Streamlining API parameters with `inputs`

Additionally, it introduces several functions to generate API GUI and manage user interactions:

1. `get_revised_dict()`: This function modifies a dictionary based on required keys.
2. `generate_api_variables()`: This function produces API variables based on user input.
3. `generate_api_gui(api_desc)`: Generates the GUI layout with the given API description.
4. `make_invisible_unless(window,values,visible_list,example)`: Manages UI elements' visibility based on user input.
5. `choose_api_gui()`: Renders the main GUI displaying available APIs, parameters, and execution results.

In the main application execution, `choose_api_gui` function gets called to display the user interface. As user actions are detected in the dropdown or interaction buttons, relevant changes are made in the GUI, providing a user-friendly environment for API interaction.
# The `abstract_apis.py` Script

The `abstract_apis.py` script is a core component of the abstract-blockchain module. This script houses the `APIBridge` class which serves as the robust engine for API URL construction and execution, and efficient GUI management for RPC parameters.


## Key Components

- `APIBridge` class: This primary class initializes with optional parameters, `api_data`, `rpc`, and `address`. To ensure smooth functionality and improve efficiency, the class imports from external modules namely, `abstract_webtools` and `abstract_utilities`.


### Methods of the `APIBridge` class include:

- `get_api_data_string`: This method prepares the appropriate API data string based on the provided `api_data_type` and `address`.

- `api_keys`: An essential method that retrieves API keys from the environment settings contingent on the scanner in use.

- `get_http_variants`, `get_api_variants`: These methods lend a hand in navigating different versions of the API URL based on request requirements.

- `try_api_url`: As the name suggests, this method obtains the API request URL.

- `get_try`, `get_request`: Key in sending a request to the API URL with a focus on 'Rate-Limiting'.

- `get_response`: This method parses the JSON response from the API.

- `check_sum`, `try_check_sum`: Integral in ensuring the validity of an Ethereum address and converting it to a checksum address.

- `safe_json_loads`: A safety-oriented method that loads JSON data as a dictionary or a list.

-------

Remember to study the functional activities of this module and understand its relevance in the larger abstract-blockchain module. Join us in the next section where we detail another integral part of the module, the abstract-api-gui.py script.
# abstract_contract_console.py

The `abstract_contract_console.py` module within the `abstract-blockchain` package offers a Graphical User Interface(GUI). This GUI is ideal for users interested in engaging interactively with the Smart Contracts on the Ethereum Blockchain. At its core, it is designed to provide a user-friendly console for interacting with Ethereum Smart Contract functions.

The module imports required dependencies and presents helper functions to perform data conversions and error checks. This setup lays the foundation for an interface that allows users to input a contract address on the Ethereum Blockchain. Once the address is provided, the interface makes a connection with a network node that will process the desired transactions and fetch available contract functions.

All available functions are displayed in the GUI, which features input fields and buttons to facilitate interaction. The GUI shows the return value for functions having 'read' or 'pure' mutability; for transaction-triggering functions, the transaction hash is displayed.

Notably, this module also permits users to manually input their account details, vital for signing transactions when calling non-read-only functions. Determining the Endpoint URL to connect to an Ethereum node is made simple with the `get_account_layout` and `determine_correct_rpc` functions.

Operating within a GUI Event Loop, the interface maintains responsiveness and interactive capabilities. When a button associated with a contract function is clicked, input values are collected, the function is executed, and the output is displayed.

In summary, `abstract_contract_console.py` emulates a local Ethereum interaction console, simplifying users' interactions with the Ethereum Blockchain and providing an all-in-one abstraction service.

Furthermore, the module features an `abstract_contract_console_main()`. This function leverages various classes from the package for smart contract interaction and accepts an optional 'rpc_list' argument. If no argument is provided, it defaults to the RPC list from the RPCBridge class. To launch a new window titled 'New Blockchain Console,' it retrieves the RPC layout and values, constructs a final layout consisting of the account, ABI, and RPC layouts. The new_window_mgr object's `while_basic()` method responsibly handles the main application loop, managing events and rendering.
## Overview

The `abstract_contracts.py` script is a part of the `abstract_blockchain` module which is designed to facilitate the interaction of users with the Ethereum network. The script is built around a suite of utility functions which assist users in communicating with smart contracts on the blockchain, providing an easy and effective way to perform a variety of tasks from simple data conversions to transaction generation.

## Key Features

1. **Versatile Utility Functions:** The script offers utility functions which handle a wide range of features including estimation of average gas price for transactions, verification and handling of different input types (e.g., boolean, integers, and addresses), and user interaction management through GUIs.

2. **Data Type Conversion:** It supports conversion of different data types (e.g., addresses, integers, bytes, boolean values, and strings) to their required format for interaction with the Ethereum blockchain.

3. **User-friendly Interaction:** The script provides a comfortable user interface, allowing for inputs confirmation for a smart contract function or generation of a new transaction.

4. **Error Handling and Validation:** It manages various situations and edge cases, such as checking the validity of a potential Ethereum address and dealing with batch inputs. It provides intuitive feedback and correction options throughout the code execution.
## abstract_contract Module

The `abstract_contracts.py` script within the abstract_blockchain module is designed to enhance user interaction with blockchain contracts associated with the Ethereum network. This script extensively uses the web3 module to enable these interactions while also leveraging PySimpleGUI to deliver a simple yet effective graphical user interface.

The script initiates with the importation of needed modules and subsequently defines several utility functions. These functions specialize in aiding users in contract communication and boosting their utilization of smart contracts within the Ethereum network.

Several features are encompassed by these functions such as average gas price estimation for transactions, verification and management of multiple input types including boolean, integers, and addresses, user interaction facilitation via GUIs, and tasks like check-summing for Ethereum addresses. Further, they empower users to interact directly with the blockchain, such as confirming inputs for a smart contract function or even producing a new transaction.

The script introduces functions to convert a diverse range of data types to a format that is suitable for the interaction with the Ethereum blockchain. Data types like addresses, integers, bytes, boolean values, and strings are all catered to. They also support list processing of these data types, allowing for batch operations.

The functions are coded to handle a broad array of situations and edge cases such as validating potential Ethereum addresses and managing batch inputs. The code regularly provides intuitive feedback and correction options. Overall, this script serves as a comprehensive suite of tools for users interested in interacting with smart contract careers on the Ethereum network.

## abstract_rpcs Module
The abstract_rpcs.py script is part of the Abstract Blockchain package and it offers the RPCBridge class that is designed to manage RPC parameters for different blockchain networks. RPC parameters are necessary for remote procedure calls (RPC), a protocol that one program can use to request a service from a program located in another computer on a network without having to understand the network's details. In the context of blockchain, RPC parameters are used to interact with the blockchain network.

The RPCBridge class in abstract_rpcs.py provides several key functionalities. It allows users to filter and select RPC parameters through a graphical user interface (GUI), streamlining the process of defining these parameters. This makes it user-friendly even for those without deep knowledge of RPC parameters.

The RPCBridge class also categorizes and organizes RPC parameters, so that they can easily be used in blockchain interactions. Information is thus made more accessible, and the usage of blockchain technology is simplified as a result.

Overall, the abstract_rpcs.py script plays a crucial role in the Abstract Blockchain package by providing efficient and streamlined ways to manage RPC parameters, one of the essential parts of interacting with blockchain networks.


In conclusion, `abstract_blockchain` is a powerful tool that allows developers to interact with Ethereum networks and contracts. While the package is easy to install and use, we always recommend carefully reading the documentation and understanding how blockchain technologies work before getting started. Happy coding!

For more info regarding license, please visit [here](https://github.com/AbstractEndeavors/abstract_blockchain/blob/main/LICENSE).




