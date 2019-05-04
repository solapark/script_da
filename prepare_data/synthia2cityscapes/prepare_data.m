
%% An example of preparing data for da-faster-rcnn, the exmample is based on adaptation from Cityscapes to Foggy Cityscapes, other datasets can be prepared similarly.
%  
% yuhua chen <yuhua.chen@vision.ee.ethz.ch> 
% created on 2018.07.17

%% specify path
source_data_dir = '/data1/sap/SYNTHIA';
target_data_dir = '/data1/sap/CITYSCAPES';

%% initialization
img_dir = '/home/sap/VOCdevkit2007/VOC2007/JPEGImages';
sets_dir = '/home/sap/VOCdevkit2007/VOC2007/ImageSets/Main';
annotation_dir = '/home/sap/VOCdevkit2007/VOC2007/Annotations';

addpath /home/sap/VOCdevkit2007/VOCcode
mkdir(img_dir); mkdir(sets_dir); mkdir(annotation_dir);

%% organize images & prepare split list.
%{
% process SYNTHIA train images
[~,cmd_output] = system(sprintf('find %s -name "*.png"', ...
    fullfile(source_data_dir,'leftImg8bit','train')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

source_train_list = cell(numel(file_names),1);
for i = 1:numel(file_names)
    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'.png','');
    im_name = ['source_' im_name];
    
    img = imread(file_names{i});
    imwrite(img,fullfile(img_dir,'SYNTHIA', 'train', [im_name '.jpg']));
    
    source_train_list{i} = im_name;
end

% process SYNTHIA test images
[~,cmd_output] = system(sprintf('find %s -name "*.png"', ...
    fullfile(source_data_dir,'leftImg8bit','test')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

source_train_list = cell(numel(file_names),1);
for i = 1:numel(file_names)
    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'.png','');
    im_name = ['source_' im_name];
    
    img = imread(file_names{i});
    imwrite(img,fullfile(img_dir,'SYNTHIA', 'test', [im_name '.jpg']));
    
    source_train_list{i} = im_name;
end
%}

% process CITYSACPES train images.
[~,cmd_output] = system(sprintf('find %s -name "*.png"', ...
    fullfile(target_data_dir,'leftImg8bit','train')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

target_train_list = cell(numel(file_names),1);
for i = 1:numel(file_names)
    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'.png','');
    im_name = ['target_' im_name];
    
    img = imread(file_names{i});
    imwrite(img,fullfile(img_dir, 'CITYSCAPES', 'train', [im_name '.jpg']));
    
    target_train_list{i} = im_name;
end

% process CITYSCAPES test images
[~,cmd_output] = system(sprintf('find %s -name "*.png"', ...
    fullfile(target_data_dir,'leftImg8bit','val')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

target_test_list = cell(numel(file_names),1);
for i = 1:numel(file_names)
    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'.png','');
    im_name = ['target_' im_name];
    
    img = imread(file_names{i});
    imwrite(img,fullfile(img_dir, 'CITYSCAPES', 'test', [im_name '.jpg']));
    
    target_test_list{i} = im_name;
end

%% prepare the annotation needed for training/testing.
% process SYNTHIA train labels.
load cityscapes_synthia_semantics.mat
[~,lb_filter] = ismember(synthia_semantics,instance_semantics);

[~,cmd_output] = system(sprintf('find %s -name "*.png"', ...
    fullfile(source_data_dir,'gtFine', 'train')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

for i = 1:numel(file_names)
    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'.png','');
    im_name = ['source_' im_name];

    im_label = imread(file_names{i});
    im_lb = im_label(:,:,1) + 1;
    im_inst = im_label(:,:,2);
    all_inst_id = setdiff(unique(im_inst),0);
    
    clear gt
    gt.boxes = zeros(numel(all_inst_id),4);
    gt.category = zeros(numel(all_inst_id),1);
    for i_inst = 1:numel(all_inst_id)
        inst_mask = (im_inst==all_inst_id(i_inst));
        gt.boxes(i_inst,:) = mask2box(inst_mask);
        inst_lb = unique(im_lb(inst_mask));
        gt.category(i_inst) = lb_filter(inst_lb);
    end
    gt.boxes = gt.boxes(gt.category~=0,:);
    gt.category = gt.category(gt.category~=0);
    
    clear save_var
    save_var.annotation.folder = 'VOC2007';
    save_var.annotation.filename = [im_name,'.jpg'];
    save_var.annotation.segmented = '0';
    save_var.annotation.size.width = num2str(size(im_inst,2));
    save_var.annotation.size.height = num2str(size(im_inst,1));
    save_var.annotation.size.depth = '3';
    
    for i_obj = 1:numel(gt.category)
        bbox = gt.boxes(i_obj,:);
        save_var.annotation.object(i_obj).bndbox.xmin = num2str(bbox(1));
        save_var.annotation.object(i_obj).bndbox.ymin = num2str(bbox(2));
        save_var.annotation.object(i_obj).bndbox.xmax = num2str(bbox(3));
        save_var.annotation.object(i_obj).bndbox.ymax = num2str(bbox(4));
        save_var.annotation.object(i_obj).name = ...
            (instance_semantics(gt.category(i_obj)));
        save_var.annotation.object(i_obj).difficult = '0';
        save_var.annotation.object(i_obj).truncated = '0';   
    end
    
    VOCwritexml(save_var,fullfile(annotation_dir, 'SYNTHIA', 'train', [im_name,'.xml']));
end

% process SYNTHIA test labels.
load cityscapes_synthia_semantics.mat
[~,lb_filter] = ismember(synthia_semantics,instance_semantics);

[~,cmd_output] = system(sprintf('find %s -name "*.png"', ...
    fullfile(source_data_dir,'gtFine', 'test')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

for i = 1:numel(file_names)
    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'.png','');
    im_name = ['source_' im_name];

    im_label = imread(file_names{i});
    im_lb = im_label(:,:,1) + 1;
    im_inst = im_label(:,:,2);
    all_inst_id = setdiff(unique(im_inst),0);
    
    clear gt
    gt.boxes = zeros(numel(all_inst_id),4);
    gt.category = zeros(numel(all_inst_id),1);
    for i_inst = 1:numel(all_inst_id)
        inst_mask = (im_inst==all_inst_id(i_inst));
        gt.boxes(i_inst,:) = mask2box(inst_mask);
        inst_lb = unique(im_lb(inst_mask));
        gt.category(i_inst) = lb_filter(inst_lb);
    end
    gt.boxes = gt.boxes(gt.category~=0,:);
    gt.category = gt.category(gt.category~=0);
    
    clear save_var
    save_var.annotation.folder = 'VOC2007';
    save_var.annotation.filename = [im_name,'.jpg'];
    save_var.annotation.segmented = '0';
    save_var.annotation.size.width = num2str(size(im_inst,2));
    save_var.annotation.size.height = num2str(size(im_inst,1));
    save_var.annotation.size.depth = '3';
    
    for i_obj = 1:numel(gt.category)
        bbox = gt.boxes(i_obj,:);
        save_var.annotation.object(i_obj).bndbox.xmin = num2str(bbox(1));
        save_var.annotation.object(i_obj).bndbox.ymin = num2str(bbox(2));
        save_var.annotation.object(i_obj).bndbox.xmax = num2str(bbox(3));
        save_var.annotation.object(i_obj).bndbox.ymax = num2str(bbox(4));
        save_var.annotation.object(i_obj).name = ...
            (instance_semantics(gt.category(i_obj)));
        save_var.annotation.object(i_obj).difficult = '0';
        save_var.annotation.object(i_obj).truncated = '0';   
    end
    
    VOCwritexml(save_var,fullfile(annotation_dir, 'SYNTHIA', 'test', [im_name,'.xml']));

	if mod(i, 100)==0
		cur_pos = ['synthia_test ', num2str(i), ' / ', num2str(numel(file_names))];
		disp(cur_pos)
	end
end


% process CITYSACPES train labels.
load cityscapes_synthia_semantics.mat
[~,lb_filter] = ismember(cityscapes_semantics,instance_semantics);

[~,cmd_output] = system(sprintf('find %s -name "*instanceIds.png"', ...
    fullfile(target_data_dir,'gtFine', 'train')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

for i = 1:numel(file_names)

    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'_gtFine_instanceIds.png','_leftImg8bit');
    im_name = ['source_' im_name];

    im_inst = imread(file_names{i});
    im_lb = imread(strrep(file_names{i},'_gtFine_instanceIds.png','_gtFine_labelIds.png'));
    all_inst_id = setdiff(unique(im_inst),0);
    
    clear gt
    gt.boxes = zeros(numel(all_inst_id),4);
    gt.category = zeros(numel(all_inst_id),1);
    for i_inst = 1:numel(all_inst_id)
        inst_mask = (im_inst==all_inst_id(i_inst));
        gt.boxes(i_inst,:) = mask2box(inst_mask);
        inst_lb = unique(im_lb(inst_mask));
        gt.category(i_inst) = lb_filter(inst_lb);
    end
    gt.boxes = gt.boxes(gt.category~=0,:);
    gt.category = gt.category(gt.category~=0);
    
    clear save_var
    save_var.annotation.folder = 'VOC2007';
    save_var.annotation.filename = [im_name,'.jpg'];
    save_var.annotation.segmented = '0';
    save_var.annotation.size.width = num2str(size(im_inst,2));
    save_var.annotation.size.height = num2str(size(im_inst,1));
    save_var.annotation.size.depth = '3';
    
    for i_obj = 1:numel(gt.category)
        bbox = gt.boxes(i_obj,:);
        save_var.annotation.object(i_obj).bndbox.xmin = num2str(bbox(1));
        save_var.annotation.object(i_obj).bndbox.ymin = num2str(bbox(2));
        save_var.annotation.object(i_obj).bndbox.xmax = num2str(bbox(3));
        save_var.annotation.object(i_obj).bndbox.ymax = num2str(bbox(4));
        save_var.annotation.object(i_obj).name = ...
            (instance_semantics(gt.category(i_obj)));
        save_var.annotation.object(i_obj).difficult = '0';
        save_var.annotation.object(i_obj).truncated = '0';   
    end
    
    VOCwritexml(save_var,fullfile(annotation_dir,'CITYSCAPES', 'train', [im_name,'.xml']));

	if mod(i, 100) == 0 
		cur_pos = ['cityscapes_train ', num2str(i), ' / ', num2str(numel(file_names))];
		disp(cur_pos)
	end

end

% process CITYSACPES test labels.
load cityscapes_synthia_semantics.mat
[~,lb_filter] = ismember(cityscapes_semantics,instance_semantics);

[~,cmd_output] = system(sprintf('find %s -name "*instanceIds.png"', ...
    fullfile(target_data_dir,'gtFine', 'val')));
file_names = strsplit(cmd_output); file_names = file_names(1:end-1);

for i = 1:numel(file_names)

    im_name = strsplit(file_names{i},'/'); 
    im_name = strrep(im_name{end},'_gtFine_instanceIds.png','_leftImg8bit');
    im_name = ['source_' im_name];

    im_inst = imread(file_names{i});
    im_lb = imread(strrep(file_names{i},'_gtFine_instanceIds.png','_gtFine_labelIds.png'));
    all_inst_id = setdiff(unique(im_inst),0);
    
    clear gt
    gt.boxes = zeros(numel(all_inst_id),4);
    gt.category = zeros(numel(all_inst_id),1);
    for i_inst = 1:numel(all_inst_id)
        inst_mask = (im_inst==all_inst_id(i_inst));
        gt.boxes(i_inst,:) = mask2box(inst_mask);
        inst_lb = unique(im_lb(inst_mask));
        gt.category(i_inst) = lb_filter(inst_lb);
    end
    gt.boxes = gt.boxes(gt.category~=0,:);
    gt.category = gt.category(gt.category~=0);
    
    clear save_var
    save_var.annotation.folder = 'VOC2007';
    save_var.annotation.filename = [im_name,'.jpg'];
    save_var.annotation.segmented = '0';
    save_var.annotation.size.width = num2str(size(im_inst,2));
    save_var.annotation.size.height = num2str(size(im_inst,1));
    save_var.annotation.size.depth = '3';
    
    for i_obj = 1:numel(gt.category)
        bbox = gt.boxes(i_obj,:);
        save_var.annotation.object(i_obj).bndbox.xmin = num2str(bbox(1));
        save_var.annotation.object(i_obj).bndbox.ymin = num2str(bbox(2));
        save_var.annotation.object(i_obj).bndbox.xmax = num2str(bbox(3));
        save_var.annotation.object(i_obj).bndbox.ymax = num2str(bbox(4));
        save_var.annotation.object(i_obj).name = ...
            (instance_semantics(gt.category(i_obj)));
        save_var.annotation.object(i_obj).difficult = '0';
        save_var.annotation.object(i_obj).truncated = '0';   
    end
    
    VOCwritexml(save_var,fullfile(annotation_dir,'CITYSCAPES', 'test', [im_name,'.xml']));

	if mod(i, 100) == 0 
		cur_pos = ['cityscapes_test ', num2str(i), ' / ', num2str(numel(file_names))];
		disp(cur_pos)
	end

end

%{
load cityscapes_semantics
[~,lb_filter] = ismember(cityscapes_semantics,instance_semantics);

im_color = imread('/data1/sap/SYNTHIA/RAND_CITYSCAPES/RGB/0000000.png');
im_label = imread('/data1/sap/SYNTHIA/RAND_CITYSCAPES/GT/LABELS/0000000.png');

im_lb = im_label(:,:,1) + 1;
all_lb_id = unique(im_lb);
im_inst = im_label(:,:,2);
all_inst_id = setdiff(unique(im_inst),0);
    
boxes = zeros(numel(all_inst_id),4);
category = zeros(numel(all_inst_id),1);
for i_inst = 1:numel(all_inst_id)
    inst_mask = (im_inst==all_inst_id(i_inst));
    boxes(i_inst,:) = mask2box(inst_mask);
    inst_lb = unique(im_lb(inst_mask));
    category(i_inst) = lb_filter(inst_lb);
end


for i_inst = 1:numel(all_inst_id)
    boxes(i_inst,3) = boxes(i_inst,3) - boxes(i_inst,1);
    boxes(i_inst,4) = boxes(i_inst,4) - boxes(i_inst,2);
end

for i = 1:8
    [ target_idx_row,~ , ~] = find(category == i);
    target_box = boxes(target_idx_row, :);
    box_image = insertShape(im_color, 'Rectangle', target_box);
    figure_name = string(instance_semantics(i))
    figure('Name', figure_name);
    imshow(box_image);
    

end

%}


