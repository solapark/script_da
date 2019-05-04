data=$1
cfg=$2
weights=$3
map_log=$4

echo "" >>$map_log 
echo "#" $weights >> $map_log

set -x
./darknet detector map $data $cfg $weights >> $map_log 
