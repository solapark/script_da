set -x

gpu_num=$1
ARGS=("$@")
class_num=$#

for (( c =1; c< $class_num; c++))
do
	class=${ARGS[$c]}
	#echo "c=$c class=$class class_num=$class_num gpu_num=$gpu_num"
	./darknet detector train VOC/VOC_$class.data VOC/VOC_one_class.cfg /data1/sap/backup/darknet53.conv.74 -dont_show -gpus $gpu_num > VOC/loss/loss_VOC_$class.log	
done
