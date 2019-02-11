#!/bin/bash

for file in $(find /raw -name '*.md')
do 
    #echo $file
    for line in $(cat $file)
    do
       if [[ $line == [http* ]]
       then
           #echo $line
           url=`echo $line | cut -d "(" -f2 | cut -d ")" -f1`
           #echo $url

           status_code=$(curl -o -I -L -s -w "%{http_code}\n" $url)
           #echo $status_code

          if [ $status_code -ge "200" ] && [ $status_code -lt "300" ]
          then
               #echo "status check succeeded"
               :
           else
               echo $file
               echo "broken url:" $url
               echo "---"
           fi
       fi

    done
done 


