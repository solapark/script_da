from utils import *

src_file_path = '/data1/sap/interpark_data/test/class/part_label/Kantata_pure_part.txt'

class2class = {\
"0" : "5",\
"1" : "6",\
"2" : "7",\
"3" : "8",\
"4" : "9"\
}

src_files = get_list_from_file(src_file_path)

for src_file in src_files : 
    print('src_file', src_file)
    src_lines = get_list_from_file(src_file)
    new_file = open(src_file, "w")
    for line in src_lines :
        line_split =line.split() 
        old_class = line_split[0]
        contents = line_split[1:]
        new_class = class2class[old_class]
        new_line = new_class + " " + " ".join(contents) + "\n" 
        new_file.write(new_line)
    new_file.close()
