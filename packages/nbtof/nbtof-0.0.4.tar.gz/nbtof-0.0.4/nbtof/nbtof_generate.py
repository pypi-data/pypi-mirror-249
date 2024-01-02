import tempfile
import os
import datetime
from .nbtof_base import nbtof_base
from .nbtof_concat import nbtof_update_base

def nbtof_generate(
    notebook_file,
    output_py_file=None,
    ):
    """
    This function converts single or multiple notebook files into one .py file.
    This .py file has functions which perform the same processings with notebooks.
    
    Parameters
    ----------
    notebook_file : str or list
        notebooks are should be tagged.
    output_py_file : str
        output .py file with functions.
    
    Returns
    -------
    str
        The outputed .py file.
    """
    
    if output_py_file is None:
        dt_now = datetime.datetime.now()
        output_py_file = 'nbtof_output_' + \
            str(dt_now.year).zfill(4) + str(dt_now.month).zfill(2) + str(dt_now.day).zfill(2) + \
            str(dt_now.hour).zfill(2) + str(dt_now.minute).zfill(2) + str(dt_now.second).zfill(2) + '.py'
    
    if type(notebook_file) == str:
        notebook_file = [notebook_file]
    
    with open(output_py_file, 'w') as f:
        pass
    
    with tempfile.TemporaryDirectory() as td:
        for notebook_file_id, notebook_file_name in enumerate(notebook_file):
            notebook_func_name = os.path.splitext(os.path.basename(notebook_file_name))[0]
            instant_func_file_path = td + '\\' + os.path.split("notebook_file_name.ipynb")[1] + ".ipynb"
            func_file_path, _ = nbtof_base(
                nb_path=notebook_file_name,
                func_name=notebook_func_name,
                func_file_name=instant_func_file_path,
                )
            nbtof_update_base(
                output_py_file,
                func_file_path)
    
    td + '\\' + os.path.split("notebook_file_name.ipynb")[1]

    return output_py_file
