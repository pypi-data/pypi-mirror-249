import pandas as pd
import polars as pl
import os
from pathlib import Path
import shutil
import inspect
import json
from .localhost import LocalHost
from glob import glob

class VariableDefinitions():
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        self.html_folder = os.path.join(base_dir,'static/html')
        self.length_of_html_folder = [f for f in os.listdir(self.html_folder) if os.path.isfile(os.path.join(self.html_folder, f))]
        self.main_html_path = os.path.join(base_dir,'static/html/main.html')
        self.html_start = """
            <!DOCTYPE html>
                <head>
                    <title>Watson Explorer</title>
                    <link rel="stylesheet" href="../css/main.css">
                </head>
                <body>
                    <table>
                            <tr>
                                <td>
                                    <h1>Watson Explorer</h1>
                                    <hr class="line">
                                </td>
                                <td>
                                    <button class='stopbtn' id="stopButton">Stop Server</button>
                                </td>
                            </tr>
                        </table>
                    <h2 class="select_dataframe">Select your DataFrame:</h2>            
                    <select name='myDropdown' id='myDropdown' class='dropbtn'>
            """
        self. html_body = """
                </select>
                <br>
                <div id="dataframe-container"></div>
                <h4>Created by Cobra Micro-Solutions</h4>
                <script src="../js/stop_server.js"></script>
                <script src="../js/include.js"></script>
                <script src="../js/coloring_int_columns.js"></script>
                """
        self. html_end = """
            </body>
        </html>
        """
        
class Explorer(VariableDefinitions):
    def __init__(self, namespace=None):
        super().__init__()
        self.dataframe_dictionary = None
        if namespace is None:
            caller_frame = inspect.currentframe().f_back
            namespace = caller_frame.f_globals
        self.delete_all_temp_htmls()
        self.retrieve_all_dataframes(namespace)
        if self.dataframe_dictionary is not None:
            self.generate_json_files()
            self.create_main_html()
            LocalHost.run_server()
    
    def delete_all_temp_htmls(self):
        html_files = glob(f'{self.html_folder}/*.html', recursive=True)
        for file in html_files:
            os.remove(file)
            
    def retrieve_all_dataframes(self, namespace):
        if namespace==None:
            print('No namespace is found!')
        else:  
            dataframe_dictionary_pandas = {name: obj for name, obj in namespace.items() if isinstance(obj, pd.DataFrame)}
            dataframe_dictionary_series = {name: obj.reset_index() for name, obj in namespace.items() if isinstance(obj, pd.Series)}
            dataframe_dictionary_polars = {name: obj.to_pandas() for name, obj in namespace.items() if isinstance(obj, pl.DataFrame)}

            self.dataframe_dictionary = {**dataframe_dictionary_pandas, **dataframe_dictionary_polars, **dataframe_dictionary_series}
            for name in self.dataframe_dictionary:
                    self.dataframe_dictionary[name].to_html(os.path.join(self.html_folder,'{}.html'.format(name)))
        return self.dataframe_dictionary

    def generate_json_files(self):
        column_data_types = {df_name: df.dtypes.apply(lambda x: x.name).to_dict() for df_name, df in self.dataframe_dictionary.items()}
        column_data_types_json = json.dumps(column_data_types)
        self.html_script = f"<script>var columnDataTypes = {column_data_types_json};</script>"
        return self.html_script

    def create_main_html(self):
        if len(self.dataframe_dictionary) > 0:
            options = '\n'.join([f"<option value='{name}.html'>{name}</option>" for name in self.dataframe_dictionary])
            full_html = self.html_start + options + self.html_body + self.html_script + self.html_end
            with open(self.main_html_path, "w") as self.main_html_file:
                self.main_html_file.write(full_html)
            return self.main_html_file