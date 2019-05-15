def get_list_from_file(file_path):
    list_file = open(file_path, 'r')
    target_list = list_file.read().strip().splitlines()
    return target_list

def get_name_from_path(path):
    name = path.split('/')[-1]
    return name
