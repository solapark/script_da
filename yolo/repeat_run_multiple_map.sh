set -x

for class in "$@"
do
	./../script_da/yolo/run_multiple_map.sh VOC/test_clipart_$class.data VOC/VOC_one_class.cfg /data1/sap/backup/clipart2VOC/VOC_$class/ VOC/map/map_clipart_"$class"_with_VOC_$class.log
	./../script_da/yolo/run_multiple_map.sh VOC/VOC_$class.data VOC/VOC_one_class.cfg /data1/sap/backup/clipart2VOC/VOC_$class/ VOC/map/map_VOC_"$class"_with_VOC_$class.log
done
