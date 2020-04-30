from utils import get_file_list_from_fileform, check_pattern_exist, copy_file, split_list

src_dir = '/data1/sap/interpark_data/train/extra_1210_mod/images/'
cam_num = [0, 1, 2]
#file_name = ['TunaCan_0_*[0-9].jpg', 'TunaCan_1_*[0-9].jpg', 'TunaCan_2_*[0-9].jpg']
file_name = ['Myzzo_0_*[0-9].jpg', 'Myzzo_1_*[0-9].jpg', 'Myzzo_2_*[0-9].jpg']
#list_format = "TunaCan_%d_%d.jpg"
list_format = "Myzzo_%d_%d.jpg"
train_dir = '/data1/sap/mv/train/'
test_dir = '/data1/sap/mv/test/'
train_size = 230

def copy_files(num_list, cam_num, list_format, src_dir, dst_dir):
    for num in num_list :
        for c in cam_num : 
            final_format = list_format % (c, num)
            image_file =  src_dir + final_format
            txt_file = image_file.replace('.jpg', '.txt')
            txt_file = txt_file.replace('images', 'labels')
            print(image_file)
            print(txt_file)
            copy_file(image_file, dst_dir)
            copy_file(txt_file, dst_dir)

if __name__ == '__main__' : 
    num_list = []
    for n in file_name : 
        file_form = src_dir + n
        files = get_file_list_from_fileform(file_form, is_full_path = False)
        nums = []
        for f in files : 
            pure_name = f.split('.')[0]
            num = pure_name.split('_')[-1]
            nums.append(int(num))
        nums.sort()
        num_list.append(nums)
    
    match_num_list = []
    is_empty = 0
    list_size = len(num_list)
    while(1) : 
        for n in num_list : 
            if not n : is_empty = 1 
        if (is_empty) : break

        first_nums = []
        for n in num_list : first_nums.append(n[0])
        ref_num = max(first_nums)
        ref_list_idx = first_nums.index(ref_num)

        is_match = 1
        target_list_idx = [x for x in range(list_size) if x != ref_list_idx]
        for i in target_list_idx:
            cur_list = num_list[i]
            while(cur_list and cur_list[0] < ref_num) :
                cur_list.pop(0)
            if (not cur_list) or ( cur_list[0] != ref_num):
                is_match = 0
                break

        if(is_match) :
            match_num_list.append(ref_num)
            for n in num_list :
                n.pop(0)

    #print(match_num_list) 
    #print('\n')

    '''
    for num in match_num_list :
        for c in cam_num : 
            final_format = list_format % (c, num)
            image_file =  dir_path + final_format
            txt_file = image_file.replace('.jpg', '.txt')
            txt_file = txt_file.replace('images', 'labels')
            print(image_file)
            print(txt_file)
            copy_file(image_file, dst_dir)
            copy_file(txt_file, dst_dir)
    '''
    
    train_num_list, test_num_list = split_list(match_num_list, train_size) 
    copy_files(train_num_list, cam_num, list_format, src_dir, train_dir)
    copy_files(test_num_list, cam_num, list_format, src_dir, test_dir)
