dir_path=$1

set -x
for dir_name in $dir_path*; 
do
	file_name=$dir_name".txt" 
	dir_full_path=$dir_name
	ls $dir_full_path/* > $file_name
done
