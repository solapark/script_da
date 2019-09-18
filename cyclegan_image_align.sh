_DEBUG="on"
function DEBUG()
{
 [ "$_DEBUG" == "on" ] &&  $@
}

DEBUG set -x 

target_dir=$1	# /data1/sap/cyclegan/results/synthia2cityscapes_8class/test_30
target_file=$2 # *A.png
align_list=$3 # /home/sap/pytorch-CycleGAN-and-pix2pix/datasets/synthia2cityscapes_8class/testB.txt
dataset_name=$4 # fake_synthia
target_or_source=$5 # target
label_path=$6 # /home/sap/dataset/images/cityscapes_8class/train

list_name=''
list_path=''

re='$+/(+)[/]+'
if [[ $target_dir =~ $re]] 
then 
	$list_name={BASH_REMATCH[1]}
	$list_path="$target_dir$list_name'.txt'"

cd $cyclegan_target_dir/images/
rm *real* *rec*
cd /
ls $cyclegan_target_dir/images/$target_file > $list_path 
python ~/script_da/rename_based_on_list.py $list_path $align_list 

mkdir ~/dataset/images/$dataset_name/$list_name
mv $cyclegan_target_dir/images/$target_or_source* ~/dataset/images/$dataset_name/$list_name
cp $label_path/*txt ~/dataset/images/$dataset_name/$list_name
cd /
ls ~/dataset/images/$dataset_name/$list_name/*.jpg > ~/dataset/images/$dataset_name/$list_name.txt
