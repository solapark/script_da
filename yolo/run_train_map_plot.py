import commands
import argparse
from utils import get_list_from_file, makefile, get_file_list_from_dir, check_pattern_exist, makedir

run_darknet = "/home/sap/da_yolo/darknet"
base = "/home/sap/da_yolo/da_yolo"
train_base = "sim10k"
val_base = "cityscapes1_val"
plot_base = "plot"
pretrain_path = "/data1/sap/backup/darknet53.conv.74"
gpus = "0"
data_name = "obj.data"
cfg_name = "obj.cfg"
loss_name = "loss.log"

parser = argparse.ArgumentParser()
parser.add_argument("--base", default=base)
parser.add_argument("--train_base", default=train_base)
parser.add_argument("--val_base", default=val_base)
parser.add_argument("--plot_base", default=plot_base)
parser.add_argument("--pretrain_path", default=pretrain_path)
parser.add_argument("--gpus", default=gpus)
parser.add_argument("--data_name", default=data_name)
parser.add_argument("--cfg_name", default=cfg_name)
parser.add_argument("--loss_name", default=loss_name)
args = parser.parse_args()

base = args.base
train_base = args.train_base
val_base = args.val_base
plot_base = args.plot_base
pretrain_path = args.pretrain_path
gpus = args.gpus
data_name = args.data_name
cfg_name = args.cfg_name
loss_name = args.loss_name

def get_backup_path_from_train_data(train_data_pah):
    content_list = get_list_from_file(train_data_pah) 
    for content in content_list :
        a, b = content.split("=")
        if a.strip() == "backup":
            return b.strip() + '/'

def darknet_map(darknet, data, cfg, wgt, log):
    makefile(log)
    cmd_write_name = "echo \"#\" " + wgt + " >> " + log
    _, _ = commands.getstatusoutput(cmd_write_name)
    cmd_map = darknet + " detector map " + data + " " + cfg + " " + wgt + " >> " +  log
    print(cmd_map)
    _, output = commands.getstatusoutput(cmd_map)

def darknet_multiple_map(darknet, data, cfg, wgt_dir, log, is_dont_100 = True, is_dont_final = True):
    wgt_list = get_file_list_from_dir(wgt_dir)
    if(is_dont_100) :  
        pattern = '.*_100.weights'
        wgt_list = [wgt for wgt in wgt_list if not check_pattern_exist(wgt, pattern)]
    if(is_dont_final) :  
        pattern = '.*_final.weights'
        wgt_list = [wgt for wgt in wgt_list if not check_pattern_exist(wgt, pattern)]
    size = len(wgt_list)
    for i, wgt in enumerate(wgt_list) :
        print(i, '/', size)
        darknet_map(darknet, data, cfg, wgt, log)    

if __name__ == "__main__" :
    train_data_path = base + "/" + train_base + "/" + data_name 
    train_cfg_path = base + "/" + train_base + "/" + cfg_name
    train_loss_path = base + "/" + train_base + "/" + loss_name
    train_backup_path = get_backup_path_from_train_data(train_data_path)
    makedir(train_backup_path)
        
    val_data_path = base + "/" + val_base + "/" + data_name 
    val_backup_path = train_backup_path
    val_map_path = base + "/" + val_base + "/map_" + val_base + "_with_" + train_base + ".log"

    plot_save_path = base + "/" + plot_base + "/map_" + val_base + "_with_" + train_base + ".png"

    train_yolo = run_darknet + " detector train " + train_data_path + " " + train_cfg_path + " " + pretrain_path + " -dont_show -gpus " + gpus + " > " + train_loss_path
    plot_yolo = "python /home/sap/script_da/yolo/plot_yolo_log.py " + train_loss_path + " " + val_map_path + " " + plot_save_path

    #print(train_yolo)
    #_, output = commands.getstatusoutput(train_yolo)
    #print(output)
    #darknet_multiple_map(run_darknet, val_data_path, train_cfg_path, val_backup_path, val_map_path)
    print(plot_yolo)
    #_, output = commands.getstatusoutput(plot_yolo)
    #print(output)
