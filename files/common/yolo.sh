#!/system/bin/sh

show_counter() {
   for i in `seq $1 $2`;
   do
      printf "\r%d" $i
      sleep 1
   done
   print ""
}

printf "hi  " && show_counter 1 11