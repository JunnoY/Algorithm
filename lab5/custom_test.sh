function timeout() { perl -e 'alarm shift; exec @ARGV' "$@"; }

function for_c {
  echo "c/$1"
}
function for_java {
  echo "java -cp java comp26120.$1_kp"
}
function for_python {
  echo "python3 python/$1_kp.py"
}
function get {
  if [[ $1 == "c" ]]; then for_c $2; fi
  if [[ $1 == "java" ]]; then for_java $2; fi
  if [[ $1 == "python" ]]; then for_python $2; fi
}


lang="c"
if [ $# -eq 1 ]
then
  lang=$1
fi
if [[ "$lang" != "c"  &&  "$lang" != "java"  &&  "$lang" != "python" ]]
then
  echo "Supply either c, java, or python as the language"
  exit
fi

algs=(dp)
inputs=( 'test1.txt' 'test2.txt' 'test3.txt' 'test4.txt' 'test5.txt' 'test6.txt' 'test7.txt' 'test8.txt' 'test9.txt' 'test10.txt')
declare -A times=(
  ['test1.txt']=20
  ['test2.txt']=20
  ['test3.txt']=20
  ['test4.txt']=20
  ['test5.txt']=20
  ['test6.txt']=20
  ['test7.txt']=20
  ['test8.txt']=20
  ['test9.txt']=20
  ['test10.txt']=20
)
Sizes=( 200 400 600 800 1000 1200 1400 1600 1800 2000 )
  for SIZE in ${Sizes[@]}
  do
    for FILE in ${inputs[@]}
      do
      LIMIT="${times[$FILE]}"
      echo "Running on $FILE for $LIMIT seconds"
      echo
      echo "\begin{tabular}{|l|l|l|l|} \hline"
      echo "Algorithm & Optimal Value & Time Taken & Result \\\\ \hline"
        for alg in ${algs[@]}
        do
        RUN=$(get $lang $alg)
        TIME=$({ time timeout ${LIMIT}s ${RUN} data/${SIZE}_capacity_input_tests/$FILE > ${alg}_${FILE}_out ; } 2>&1 | grep real | grep -o '[0-9].*')
        LAST=$(grep -o '\(Current best solution\|value\)=[0-9]*' ${alg}_${FILE}_out | tail -1)
        VALUE=$(echo $LAST | sed -n -e 's/.*=//g' -e 'p')
  #
        minutes=${TIME%m*}   # remove everything after "m" (including "m")
        seconds=${TIME#*m}
        seconds=${seconds%*s}  # remove everything after "s" (including "s")
        minutes=$(($minutes*60))
        total_seconds=$(echo "$minutes + $seconds" | bc)

        printf -v alg %-10.10s $alg
        printf -v VALUE %-25.25s "$VALUE"
        echo "$alg & $VALUE & ${TIME} & $CORRECT  \\\\"
        echo $SIZE, $total_seconds>> data/data_python.csv
  done
  done
  done
  echo "\hline \end{tabular}"
  echo
  echo