def pack_list_if_not (*args):
    return_list = []
    for obj in args:
        if not isinstance(obj, list):
            return_list.append([obj])
        else:
            return_list.append(obj)
    if len(return_list) == 1:
        return return_list[0]
    return return_list

