#!/bin/bash

for file in $(find /raw -name '*.md')
do 
    for line in $(cat $file)
    do
        if [[ $line == *"](http"* ]]
        then
            url=`echo $line | egrep -o '\]\(h.*)' | sed 's|[]()]||g'`

            # bail out on private repos
            if [[ ("$url" == *"docker-training/exercises"*) || ("$url" == *"docker-training/presentations"*) || ("$url" == *"docker-training/communication-templates"*) || ("$url" == *"docker/testkit"*) ]]
            then
                continue
            fi

            status_code=$(curl -o -I -L -s -w "%{http_code}\n" $url)

            if [[ $status_code -ge "200" ]] && [[ $status_code -lt "300" ]]
            then
                :
            else
                echo $file
                echo "broken url:" $url
                echo "---"
            fi
        fi
    done
done 


