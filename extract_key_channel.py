import commands
from utils import get_list_from_file 

path_list_path ="/home/sap/darknet_interpark/activation_map/tmp/data/path_list.txt"
row_list_path = "/home/sap/darknet_interpark/activation_map/tmp/data/row_list.txt"
col_list_path = "/home/sap/darknet_interpark/activation_map/tmp/data/col_list.txt"
output_path = "/home/sap/darknet_interpark/activation_map/tmp/data/output.txt"
log_path = "/home/sap/darknet_interpark/activation_map/tmp/data/log.txt"
run_darknet = "/home/sap/darknet_interpark/darknet detector test /home/sap/darknet_interpark/Corntea_Kantata_600_org/obj.data /home/sap/darknet_interpark/Corntea_Kantata_600_org/yolov3.cfg /data1/sap/backup/interpark/Corntea_Kantata_600_org/yolov3_4000.weights "
print_channel = "python /home/sap/script_da/print_channel.py "

#failure, output = commands.getstatusoutput(run_darknet)
#print(output)

if __name__ == "__main__" :
    path_list = get_list_from_file(path_list_path)   
    row_list = get_list_from_file(row_list_path)
    col_list = get_list_from_file(col_list_path)
    output_file = open(output_path, 'w')
    log_file = open(log_path, 'w')

    size = len(path_list)
    for i, (path, row, col) in enumerate(zip(path_list, row_list, col_list)) :
        run_darknet_cmd = run_darknet + path    
        _, output = commands.getstatusoutput(run_darknet_cmd)
        log_file.write(output + '\n')

        print_channel_cmd = print_channel + row + " " + col
        failure, channel = commands.getstatusoutput(print_channel_cmd)
        output_file.write(path + " " + channel + "\n")
        print(path, row, col)
        print(i+1, '/', size, 'done')
        #if(i == 2) : break

    output_file.close()
    log_file.close()
