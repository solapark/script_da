set -x

data=$1
cfg=$2
weights=$3
thresh_interval=$4
map_log=$5

> $map_log

thresh=0
while [ 1 -eq "$(echo "${thresh} < 1" | bc)" ]
do
	echo "" >> $map_log 
	echo "thesh ${thresh}" >> $map_log 

	./darknet detector map $data $cfg $weights -thresh $thresh >> $map_log
	thresh=`echo $thresh + $thresh_interval | bc`
done
