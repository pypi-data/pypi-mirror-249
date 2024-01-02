from rpy2.robjects import r
import os

# List of your R script files in current dir that have extension .R
r_script_files = [os.path.join('R', x) for x in os.listdir('R') if x.endswith('.R')]

# Load all the R scripts
for file_path in r_script_files:
    with open(file_path, 'r') as f:
        r_script = f.read()
        r(r_script)

# Import the R functions you want to expose to Python
build_time_series = r['build_time_series']
download_series = r['download_series']
EasyData_key_setup = r['EasyData_key_setup']
get_Easydata_key = r['get_Easydata_key']
get_info_on_series = r['get_info_on_series']
plot_time_series = r['plot_time_series']
session_has_Easydata_key = r['session_has_Easydata_key']

__all__ = ['build_time_series', 'download_series', 'EasyData_key_setup', 'get_Easydata_key', 'get_info_on_series', 'plot_time_series', 'session_has_Easydata_key']