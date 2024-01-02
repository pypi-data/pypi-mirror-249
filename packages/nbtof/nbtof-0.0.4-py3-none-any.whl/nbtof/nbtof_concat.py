import ast, copy
import numpy as np
import pandas as pd
import os
def body_dig(node, i = -1):
    return_name_table = []
    for j, node_u in enumerate(node.body):
        if type(node_u) == ast.Import:
            for name in node_u.names:
                if name.asname is not None:
                    return_name_table.append([name.asname, j * (i<0) + i * (i>=0), type(node_u), None, name.name, name.asname])
                else:
                    return_name_table.append([name.name, j * (i<0) + i * (i>=0), type(node_u), None, name.name, name.asname])
        elif type(node_u) == ast.ImportFrom:
            for name in node_u.names:
                if name.asname is not None:
                    return_name_table.append([name.asname, j * (i<0) + i * (i>=0), type(node_u), node_u.module, name.name, name.asname])
                else:
                    return_name_table.append([name.name, j * (i<0) + i * (i>=0), type(node_u), node_u.module, name.name, name.asname])
        elif type(node_u) == ast.Assign:
            if type(node_u.targets[0]) == ast.Tuple:
                for elt in node_u.targets[0].elts:
                    #return_name_table.append(elt.id)
                    return_name_table.append([elt.id, j * (i<0) + i * (i>=0), type(node_u), None, None, None])
            elif type(node_u.targets[0]) == ast.Name:
                return_name_table.append([node_u.targets[0].id, j * (i<0) + i * (i>=0), type(node_u), None, None, None])
        elif type(node_u) == ast.For:
            if type(node_u.target) == ast.Tuple:
                for elt in node_u.target.elts:
                    #return_name_table.append(elt.id)
                    return_name_table.append([elt.id, j * (i<0) + i * (i>=0), type(node_u), None, None, None])
            elif type(node_u.target) == ast.Name:
                #return_name_table.append(node_u.target.id)
                return_name_table.append([node_u.target.id, j * (i<0) + i * (i>=0), type(node_u), None, None, None])

            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
        
        elif type(node_u) == ast.FunctionDef:
            return_name_table.append([node_u.name, j * (i<0) + i * (i>=0), type(node_u), None, None, None])
        elif type(node_u) == ast.While:
            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
        elif type(node_u) == ast.If:
            return_name_table = return_name_table + body_dig(node_u, j * (i<0) + i * (i>=0))
    return return_name_table
def name_info_df(func_p):
    func_name_table = body_dig(func_p)
    if func_name_table == []:
        return_name_df = pd.DataFrame(
            columns=['name', 'idx', 'type', 'module', 'import', 'as']
        )
    else:
        return_name_df = pd.DataFrame(
            data=np.array(func_name_table),
            columns=['name', 'idx', 'type', 'module', 'import', 'as']
        )
    return return_name_df
def import_str(name_ds):
    if name_ds['module'] is not None:
        return name_ds['module'] + '.' + name_ds['import']
    else:
        return name_ds['import']
def new_import_check(add_name_ds, base_name_df):
    #add_import_info_alist = add_name_df.iloc[4][['module', 'import', 'as']].values
    #base_import_info_array = base_name_df[['module', 'import', 'as']].values
    concat_status = 'new'
    for _, base_name_ds in base_name_df.iterrows():
        if (add_name_ds['name'] == base_name_ds['name'])*(import_str(add_name_ds) == import_str(base_name_ds)):
            concat_status = 'exist'
        elif (add_name_ds['name'] == base_name_ds['name'])*(import_str(add_name_ds) != import_str(base_name_ds)):
            concat_status = 'error'
    return concat_status

def nbtof_update_base(
    base_py_file_name,
    add_py_file_name,
    auto_sort=True,
    ):
    
    if base_py_file_name[-3:] != '.py':
        base_py_file_name = base_py_file_name +'.py'
    
    if not os.path.isfile(base_py_file_name):
        with open(base_py_file_name, 'w') as f:
            pass
    
    with open(base_py_file_name) as f:
        base_p = copy.deepcopy(ast.parse(f.read()))
    with open(add_py_file_name) as f:
        add_p = copy.deepcopy(ast.parse(f.read()))
    
    add_name_df = name_info_df(add_p)
    base_name_df = name_info_df(base_p)
    
    return_p = copy.deepcopy(base_p)
    return_body_list = []
    for idx, node in enumerate(add_p.body):
        instant_name_df = add_name_df[add_name_df['idx'] == idx]
        if (type(node) == ast.Import) + (type(node) == ast.ImportFrom):
            for _, instant_name_ds in instant_name_df.iterrows():
                concat_status = new_import_check(instant_name_ds, base_name_df)
                #print(instant_name_ds['name'], concat_status)
                if (concat_status == 'new')&(instant_name_ds['type'] == ast.Import):
                    instant_module = ast.Import(
                        names=[
                            ast.alias(
                                name = instant_name_ds['import'], 
                                asname=instant_name_ds['as']
                                )
                            ]
                        )
                    return_body_list.append(copy.deepcopy(instant_module))
                elif (concat_status == 'new')&(instant_name_ds['type'] == ast.ImportFrom):
                    instant_module = ast.ImportFrom(
                        module=instant_name_ds['module'],
                        names=[
                            ast.alias(
                                name = instant_name_ds['import'], 
                                asname=instant_name_ds['as']
                                )
                            ],
                        level=0
                        )
                    return_body_list.append(copy.deepcopy(instant_module))
        elif (type(node) == ast.FunctionDef):
            add_func_name = add_name_df[(add_name_df['idx'] == idx)&(add_name_df['type'] == ast.FunctionDef)]['name'].values[0]
            return_body_list.append(copy.deepcopy(node))
            for _, instant_name_ds in base_name_df.iterrows():
                if (instant_name_ds['name'] == add_func_name)&(instant_name_ds['type'] == ast.FunctionDef):
                    return_p.body[instant_name_ds['idx']] = copy.deepcopy(node)
                    return_body_list = return_body_list[:-1]        
                    break
        else:
            return_body_list.append(copy.deepcopy(node))
            
    return_p.body = return_p.body + return_body_list
    
    if auto_sort:
        auto_sort_table = [
            [ast.Import], 
            [ast.ImportFrom],
            [ast.Assign, ast.AnnAssign, ast.For, ast.AsyncFor, ast.While, ast.Raise, ast.If, ast.ClassDef, ast.With, ast.Expr],
            [ast.FunctionDef, ast.AsyncFunctionDef],
            [ast.Delete, ast.Return, ast.Break, ast.Continue, ast.Pass],
            ]
        sort_body_list = []
        for auto_sort_list in auto_sort_table:
            for node in return_p.body:
                if type(node) in auto_sort_list:
                    sort_body_list.append(copy.deepcopy(node))
        return_p.body = sort_body_list
    
    with open(base_py_file_name, mode='w') as f:
        f.write(ast.unparse(return_p))

    return True
