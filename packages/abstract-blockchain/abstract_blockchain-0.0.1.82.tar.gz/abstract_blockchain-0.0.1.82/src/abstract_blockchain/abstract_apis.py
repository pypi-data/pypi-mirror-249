from abstract_webtools import DynamicRateLimiterManager
from .abstract_rpcs import RPCGUIManager,RPCBridge
from abstract_utilities import safe_json_loads,is_number,safe_json_loads,make_list
from abstract_utilities.list_utils import remove_from_list,filter_json_list_values,recursive_json_list
from abstract_security import get_env_value
import requests
import os
from abstract_gui import AbstractWindowManager,sg,ensure_nested_list,expandable,make_component,text_to_key
from .abstract_blockchain_functions import *
class APIURLManager:
    def __init__(self,api_mgr):
        self.api_mgr = api_mgr or APIBridge()
        self.url_manager={}
    def add_url(self,url,output):
        if scanner not in self.url_manager:
            self.url_manager[scanner]=[]
        url_parts = url.split('?')
        scanner=strip_web(url_parts[0])
        self.url_manager[scanner].append({"action":"","url":[],"output":[],"inputs":{}})
        self.url_manager[scanner][-1]["url"].append(url)
        self.url_manager[scanner][-1]["output"].append(output)
        for item in url_parts[-1].split('&'):
            item_parts = item.split('=')
            if item_parts[0] == 'action':
                self.url_manager[scanner][-1]['action']=item_parts[-1]
            else:
                self.url_manager[scanner][-1]["inputs"][item_parts[0]]=item_parts[-1]
            
class ApiGUI:
    def __init__(self,api_url_mgr=None,api_gui=False,api_mgr=None,rpc_mgr=None,
                 rpc_js:dict=None,
                 rpc_gui:bool=False,
                 address:str=None,
                 contract_address:str=None,
                 start_block:str=None,
                 end_block:str=None,
                 api_key:str=None,
                 env_key:str=None):
        self.api_url_mgr = api_url_mgr or APIURLManager(api_mgr=api_mgr)
        self.api_mgr = api_mgr
        if self.api_mgr == None:
            self.api_mgr=APIBridge(rpc_mgr=rpc_mgr,
                 rpc_js=rpc_js,
                 rpc_gui=rpc_gui,
                 address=address,
                 contract_address=contract_address,
                 start_block=start_block,
                 end_block=end_block,
                 api_key=api_key,
                 env_key=env_key)
        self.contract_address = contract_address
        self.address=address
        self.rpc_mgr_gui=RPCGUIManager(rpc_mgr=self.api_mgr.rpc_mgr,gui_window=False)
        self.rpc_gui_keys=[]
        self.section='APIMGR'
        for key in self.rpc_mgr_gui.all_keys:
            self.rpc_gui_keys.append(text_to_key(key,section=self.section))
        api_keys = list(apiCallDesc.keys())
        # Main Window Layout
        output = ensure_nested_list(make_component("Multiline",'',key='-API_OUTPUT-', disabled=True,**expandable()))
        rpc_layout = self.rpc_mgr_gui.get_rpc_layout(section=self.section)
        self.layout = [[rpc_layout],
            [[make_component("Frame","api output",layout=output,**expandable(size=(None,180)))],sg.Text('Select API Call Type:'), sg.Combo(values=api_keys,default_value=api_keys[0], key='API_SELECT', enable_events=True)],
            [sg.Frame('Parameters:', [[sg.Column(self.generate_api_gui(apiCallDesc[api_keys[0]]), key='API_GUI')]])]
        ]
        if api_gui:
            self.pop_up_gui()
        self.windows_mgr=AbstractWindowManager()
        self.window_name = self.windows_mgr.add_window(title='API Call GUI', layout=self.layout,close_events=['Exit',"OK"],event_handlers=[self.while_window])


    def pop_up_gui(self):
        self.windows_mgr.while_window(window_name=self.window_name)
        return self.windows_mgr.search_closed_windows(window_name=self.window_name)['values']['API_URL']
    def generate_api_gui(self,api_desc):
        """
        Function to generate GUI layout based on the selected API description.
        """
        layout = []
        # Add an "Execute" button
        
        layout.append([sg.Column(ensure_nested_list([[sg.Button('Generate URL')],
                                                     [sg.Button("Get Output")]])),
                       sg.Column(ensure_nested_list([[sg.Button("OK")],
                                                     [sg.Exit()]
                                                     ]
                                                    )),
                       sg.Column(ensure_nested_list([
                           [sg.Checkbox(text="input api key",key="-API_KEY_TOGGLE-",default=False,enable_events=True)],
                           [sg.Checkbox(text="select api url",key="-SCANNER_TOGGLE-",default=False,enable_events=True)]
                           ]))])
        # Add a multi-line input box to display the generated API URL
        layout.append([sg.Multiline(size=(50, 5), key='API_URL', disabled=True)])
        # Generate input fields
        for key in options:
            layout.append([sg.Text(f'{key}:'), sg.Input(default_text='',key=f'-{key.upper()}_SELECT-',disabled=True,enable_events=True)])
        for i,each in enumerate(inputs):
            layout.append([sg.T(text=f':',key=f"-{i}_TEXT-",visible=False),sg.Push(),
                           sg.Input(size=(45,1),key=f'-{i}_INPUT-',visible=False),
                           sg.T(text='example:',key=f"-{i}_EXAMPLE_TEXT-",visible=False),
                           sg.Input(size=(45,1),key=f'-{i}_EXAMPLE_INPUT-',disabled=True,visible=False)])

        return layout
    def get_defaults(self,each):
            each_inp =''
            
            if each == 'address':
                each_inp = self.api_mgr.address or ''
            elif each == 'contract_address':
                each_inp = self.api_mgr.contract_address or ''
            elif each == 'end_block':
                each_inp = self.api_mgr.end_block or ''
            elif each == 'start_block':
                each_inp = self.api_mgr.start_block or ''
            elif each == 'apikey':
                each_inp = self.api_mgr.api_key or ''
            elif each == 'env_key':
                each_inp = self.api_mgr.env_key or ''
            return each_inp
    def get_revised_dict(self,desired_keys):
        js_ls = []
        for topic,data in apiCallDesc.items():
            js_ls.append(data["pieces"])
        recursive_list = recursive_json_list(js_ls,desired_keys)
        filtered_list = filter_json_list_values(recursive_list,recursive_list[0].keys())
        for each in filtered_list.keys():
            filtered_list[each] = filtered_list[each][0]
        return filtered_list
    def generate_api_variables(self,values):
        selected_api = values['API_SELECT']
        api_data = apiCallDesc[selected_api]
        generated_url = api_data['example']
        js_all={}
        for each in generated_url.split('?')[-1].split('&'):
            api_key = each.split('=')[0]
            api_val = each.split('=')[1]
            if api_key not in js_all:
                js_all[api_key]= []
            if api_val not in js_all[api_key]:
                js_all[api_key].append(api_val)
        return js_all
    def make_invisible_unless(self,example):
        highest = 0
        for each in self.visible_list:
            if len(each)>highest:
                highest=len(each)
        for i,each in enumerate(self.visible_list):
            extra = highest-len(each)
            self.window[f'-{i}_TEXT-'].update(value=each,visible=True)
            self.window[f'-{i}_INPUT-'].update(visible=True)
            self.window[f'-{i}_EXAMPLE_TEXT-'].update(visible=True)
            self.window[f'-{i}_EXAMPLE_INPUT-'].update(value=example[each][0],visible=True)
        for each in self.values.keys():
            if '_INPUT-' in each:
                num_each = each[1:].split('_')[0]
                if int(num_each) >i:    
                    self.window[f'-{num_each}_TEXT-'].update(visible=False)
                    self.window[f'-{num_each}_INPUT-'].update(visible=False)
                    self.window[f'-{num_each}_EXAMPLE_TEXT-'].update(visible=False)
                    self.window[f'-{num_each}_EXAMPLE_INPUT-'].update(visible=False)
    def get_input_key(self,values,text_value):
        for key,value in values.items():
            if value == text_value:
                return f"-{key[1:-1].split('_')[0]}_INPUT-"
    def get_generated_url_output(self):
        selected_api = self.values['API_SELECT']
        api_data = apiCallDesc[selected_api]
        module = self.values["-MODULE_SELECT-"]
        action = self.values["-ACTION_SELECT-"]
        text='module'+'='+f'{module}'+'&action='+f'{action}'
        js_all=self.generate_api_variables(self.values)
        js_all_keys = list(js_all.keys())
        js_all_keys = js_all_keys[2:] 
        for i,each in enumerate(js_all_keys):
            inputs = self.values['-'+str(i)+'_INPUT-']
            if inputs == '':
                inputs = self.values['-'+str(i)+'_EXAMPLE_INPUT-']
            text+="&"+f"{each}"+"="+f"{inputs}"
        text = text.split('apikey=')[0]+'apikey='
        if self.values["-API_KEY_TOGGLE-"]:
            key = self.get_input_key(self.values,'YourApiKeyToken')
            if key:
                text+=self.values[key]
        if self.values['-SCANNER_TOGGLE-']:
            scanner = self.api_mgr.rpc_mgr.scanner
            if scanner:
                scanner_protocol = f"https://{('api.' if 'api' != scanner else '')}{scanner}/api?"
                text=scanner_protocol+text
        # Here's where you would combine the base URL with the user's inputs 
        # to generate the full API URL. I'm just simulating this step.
        return text
    def toggle_scanner(self):
        output=None
        generated_url= self.values['API_URL']
        value  = self.values['-SCANNER_TOGGLE-']
        scanner,scanner_protocol = self.api_mgr.rpc_mgr.scanner,None
        if scanner:
            scanner_protocol = f"https://{('api.' if 'api' != scanner else '')}{scanner}/api?"
        if value:
            if scanner_protocol:
                if '/api?' in generated_url:
                    generated_url=generated_url.split('/api?')[-1]
                output=f"{scanner_protocol}{generated_url}"
        else:
            if '/api?' in generated_url:
                output=generated_url.split('/api?')[-1]
        return output
    def toggle_api_key(self):
        output=None
        generated_url = self.values['API_URL']
        if generated_url:
            key = self.get_input_key(self.values,'YourApiKeyToken')
            if key:
                value = self.values[key]
                if value:
                    if self.values["-API_KEY_TOGGLE-"]:
                        if generated_url.endswith('apikey='):
                            output=self.values['API_URL']+value
                    else:
                        if generated_url.endswith(value):
                            output=generated_url[:-len(value)]
        return output
    def while_window(self,event,values,window):
        self.event,self.values,self.window=event,values,window

        # If user selects a different API from the dropdown
        if event == "Get Output":
            scanner_toggle,api_key_toggle=self.values['-SCANNER_TOGGLE-'],self.values["-API_KEY_TOGGLE-"]
            self.values['-SCANNER_TOGGLE-'],self.values["-API_KEY_TOGGLE-"]=True,True
            generated_url = self.get_generated_url_output()
            self.values['-SCANNER_TOGGLE-'],self.values["-API_KEY_TOGGLE-"]=scanner_toggle,api_key_toggle
            output = make_request(generated_url)
            self.api_url_mgr.add_url(url=generated_url,output=output)
            window['-API_OUTPUT-'].update(output)
        elif event == 'API_SELECT':
            selected_api = values['API_SELECT']
            window['API_GUI'].update(self.generate_api_gui(apiCallDesc[selected_api]))
            js_all=self.generate_api_variables(values)
            self.visible_list = []
            for each in js_all.keys():
                if each not in ['action','module']:
                   self.visible_list.append(each)
            self.window['-MODULE_SELECT-'].update(value=js_all["module"][0])
            self.window['-ACTION_SELECT-'].update(value=js_all["action"][0])
            self.make_invisible_unless(js_all)
            js_all=self.generate_api_variables(values)
            js_all_keys = list(js_all.keys())
            js_all_keys = js_all_keys[2:]
            for i,each in enumerate(js_all_keys):
                inputs = window['-'+str(i)+'_INPUT-'].update(self.get_defaults(each))
        elif "_SELECT-" in event:
            desired_keys = {event[1:-len("_SELECT-")].lower():[values[event]]}
            filtered_list = self.get_revised_dict(desired_keys)
            self.window['-ACTION_SELECT-'].update(values=filtered_list["action"],value=filtered_list["action"][0])
            self.visible_list = []
            text=''
            for each in filtered_list.keys():
                if each in inputs:
                    self.visible_list.append(each)
                else:
                    value = filtered_list[each]
                    if isinstance(value,list):
                        if len(value)>0:
                            value = value[0]
                    text+=("&" if text != '' else '')+each+"="+value
            self.window['API_URL'].update(value=text)
            self.make_invisible_unless(self.visible_list)
        # Generate the API URL based on the inputs
        elif event == "-API_KEY_TOGGLE-":
            toggle=self.toggle_api_key()
            if toggle:
                window['API_URL'].update(toggle)
        elif event == '-SCANNER_TOGGLE-':
            toggle=self.toggle_scanner()
            if toggle:
                window['API_URL'].update(toggle)
        elif event == 'Generate URL':
            generated_url=self.get_generated_url_output()
            if generated_url:
                self.window['API_URL'].update(generated_url)
        elif event in self.rpc_gui_keys:
           self.rpc_mgr_gui.rpc_win_while(self.event,self.values,self.window)
           rpc_js = self.rpc_mgr_gui.get_rpc_values(values)
           self.api_mgr.rpc_mgr.setup_rpc_attributes(rpc_js)
           self.api_mgr.get_api_key()
class APIBridge:
    def __init__(self,rpc_mgr:str=None,
                 api_gui_mgr=None,
                 api_data_type:str=None,
                 api_key:str=None,
                 env_key:str=None,
                 service_name:str=None,
                 api_url_data:str=None,
                 rpc_js:dict=None,
                 address:str=None,
                 contract_address:str=None,
                 start_block:str=None,
                 end_block:str=None,
                 low_limit:int=10,
                 high_limit:int=30,
                 rpc_gui:bool=False,
                 api_gui:bool=False):
        
        self.get_api_key_network=[]
        self.rate_limiter = DynamicRateLimiterManager()
        self.api_gui_mgr = api_gui_mgr or ApiGUI(api_mgr=self)
        
        self.rpc_mgr=rpc_mgr
        self.rpc_js=rpc_js
        self.rpc_gui=rpc_gui
        self.update_rpc(rpc_mgr=rpc_mgr,rpc_js=rpc_js,rpc_gui=rpc_gui)
        
        self.env_key=env_key
        self.api_key=self.get_api_key(api_key=api_key,env_key=env_key)

        self.api_service_tracker={}
        self.update_service_name(service_name=service_name, low_limit=low_limit, high_limit=high_limit)
        
        self.contract_address=contract_address
        self.address=address
        
        self.update_address(address=address,contract_address=contract_address)
        
        self.start_block=start_block
        self.api_data_type = api_data_type
        self.api_url_data = api_url_data
        self.start_block=start_block
        self.end_block=end_block
        self.update_api_call_partameters(address=self.address,contract_address=self.contract_address,start_block=self.start_block,end_block=self.end_block,api_data_type=self.api_data_type,api_gui=api_gui)
    def update_rpc(self,rpc_mgr=None,rpc_js=None,rpc_gui=False):
        if rpc_gui:
            self.rpc_gui_mgr = RPCGUIManager(rpc_mgr=rpc_mgr)
            self.rpc_mgr = self.rpc_gui_mgr.rpc_mgr
        if self.rpc_mgr == None:
            if rpc_mgr:
                self.rpc_mgr = rpc_mgr
            else:
                self.rpc_mgr = RPCBridge(rpc_js=rpc_js)
        elif rpc_mgr or rpc_js:
            if rpc_mgr and self.rpc_mgr != rpc_mgr:
                self.rpc_mgr = rpc_mgr
            else:
                if rpc_js != self.rpc_mgr.rpc_js:
                   self.rpc_mgr.update_rpc_js(rpc_js=rpc_js)
                   
    def update_service_name(self, service_name=None, low_limit=10, high_limit=30):
        self.service_name = service_name
        if self.service_name == None:
            api_key_identifier = hash(self.api_key)  # or some other unique identifier
            self.service_name = f"{self.rpc_mgr.scanner}_{api_key_identifier}"
        # Register service name and API key
        self.api_service_tracker[self.service_name] = self.api_key
        # Configure rate limiter for the service
        self.rate_limiter.add_service(service_name=self.service_name, low_limit=low_limit, high_limit=high_limit)
        return self.service_name
    def update_address(self,address=None,contract_address=None):
        if address == False:
            self.address=None
        else:
            self.address=address or self.address
            if self.address:
                self.address=checksum(self.address)
            
        if contract_address == False:
            self.contract_address=None
        else:
            if self.contract_address != contract_address and contract_address != None:
                self.contract_address = checksum(self.contract_address)
        return self.contract_address
    def update_api_call_partameters(self,rpc_mgr=None,rpc_js=None,address=[],contract_address=None,start_block=None,end_block=None,api_data_type=None,api_gui=None,**kwargs):
        if rpc_mgr or rpc_js:
            self.update_rpc(rpc_mgr=rpc_mgr,rpc_js=rpc_js)
            self.get_api_key()
        self.update_address(address=address,contract_address=contract_address)
        self.api_data_type = None if api_data_type == False else api_data_type or self.api_data_type
        self.start_block =  None if start_block == False else start_block or self.start_block
        self.end_block = None if end_block == False else end_block or self.end_block
        self.api_data_type =  None if api_data_type == False else api_data_type or self.api_data_type
        
        address=make_list(self.address)
        for each in make_list(self.contract_address):
            address.append(self.contract_address)
        self.api_url=get_generated_url_output(address=address,**kwargs)
        self.make_api_call(self,api_gui=api_gui,api_url_data=self.api_url_data)
    def get_api_key(self,api_key=None,env_key=None):
        if api_key:
             self.api_key = api_key
             return self.api_key
        return get_api_key(scanner=self.rpc_mgr.scanner,env_key=env_key)
    def make_api_call(self,api_url=None,api_gui=False,api_url_data=None):
        self.api_url_data = api_url_data or self.api_url_data
        if api_gui:
            self.api_url=self.api_gui_mgr.pop_up_gui()
        try:
            if self.api_url == None:
                self.api_url = f"https://{('api.' if 'api' != self.rpc_mgr.scanner[:len('api')] else '')}{self.rpc_mgr.scanner}/api?{self.api_url_data}&apikey={self.api_key}"
            self.response = make_request(url=self.api_url)
            #self.response = self.request_manager.get_limited_request(request_url=self.api_url,service_name=self.service_name)               
            return self.response
        except Exception as e:
            print(e)
    def _make_request(self, url):
            # Utilize the rate limiter manager to make the request
            try:
                return self.rate_limiter.get_limited_request(self.rate_limiter.services[self.service_name], url, self.service_name)
            except Exception as e:
                logging.error(f"Error in making request: {e}")
                return None
            
