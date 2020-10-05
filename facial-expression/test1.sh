#!/bin/bash

##############################################################
# メイン処理

##############################################################


VAR=`git diff --name-status`
M="M"
D="D"
while read line
do
    if [ "${line:0:1}" = "$M" ]
    then
        echo $line+" /Mです"
    elif [ "${line:0:1}" = "$D" ]
    then
        echo $line+" /Dです"
    fi
done <<END
$VAR
END

# echo $VAR



# 正常終了
# exit 0