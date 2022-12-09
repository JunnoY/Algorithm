SIZES="20000 40000 60000 80000 100000"

for SIZE in $SIZES
do

for COUNT in 1 2 3 4 5
do

    # Debugging command to check program call actually works
    python3 ./python/speller_hashset.py -d ./sorted/dict_${SIZE} -m 4 ./sorted/query_${SIZE}

    ALL_TIME=`(time -p python3 ./python/speller_hashset.py -d ./sorted/dict_${SIZE} -m 4 ./sorted/query_${SIZE}) 2>&1 | grep -E "user |sys " | sed s/[a-z]//g`
    
    RUNTIME=0
    for i in $ALL_TIME;
    do RUNTIME=`echo $RUNTIME + $i|bc`;
    done
    
    echo $SIZE $RUNTIME >> data/sorted/data_hashset_python.dat
    echo $SIZE, $RUNTIME >> data/sorted/data_hashset_python.csv
    
    # Debugging command to check program call actually works
    python3 ./python/speller_bstree.py -d ./sorted/dict_${SIZE} -m 0 ./sorted/query_${SIZE}

    ALL_TIME2=`(time -p python3 ./python/speller_bstree.py -d ./sorted/dict_${SIZE} -m 0 ./sorted/query_${SIZE}) 2>&1 | grep -E "user |sys " | sed s/[a-z]//g`


    RUNTIME2=0
    for i in $ALL_TIME2;
    do RUNTIME2=`echo $RUNTIME2 + $i|bc`;
    done

    echo $SIZE $RUNTIME2 >> data/sorted/data_bstree_python_large.dat
    echo $SIZE, $RUNTIME2 >> data/sorted/data_bstree_python_large.csv
    
#done

done

done
