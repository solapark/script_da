set -x

for class in "$@"
do
	./darknet detector test clipart/pseudo_clipart_$class.data clipart/one_class.cfg  /data1/sap/backup/clipart2VOC/VOC_$class/VOC_one_class_10000.weights -dont_show -save_labels -thresh .01 < /home/sap/dataset/clipart/train.txt
done
