set -x

data=$1
cfg=$2
weights_dir=$3
map_log=$4

target_weight='.weights$'
#target_weight='_[0-9]+000.weights$'
#target_weight='_(18|19|2|3)[0-9]+.weights$'

>$map_log

for weight in $weights_dir*.weights; 
do
	if [[ $weight =~ $target_weight ]]
	then 
		echo "correct"
		./../script_da/yolo/run_map.sh $data $cfg "$weight" $map_log 
	fi
	echo "done"
done
