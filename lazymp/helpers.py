def join_dict(from_dict, to_dict):
    for k, v in from_dict.items():
        to_dict[k] = v

def join_add_dict(from_dict, to_dict):
    for k, v in from_dict.items():
        if k in to_dict:
            to_dict[k] += v
        else:
            to_dict[k] = v


def join_shared(shared_variables_list, variables):
    for shared_variables in shared_variables_list:
        for name, value in shared_variables.items():
            if type(value) == dict:
                join_dict(value, variables[name])

def join_add_shared(shared_variables_list, variables):
    for shared_variables in shared_variables_list:
        for name, value in shared_variables.items():
            if type(value) == dict:
                join_add_dict(value, variables[name])

def copy_dict(from_dict, to_dict):
    join_dict(from_dict, to_dict)

def copy_new_list(from_list, to_list):
    for e in from_list:
        to_list.append(e)

def copy_list(from_list, to_list):
    for i, e in enumerate(from_list):
        to_list[i] = e



