#/bin/bash

monitor() {
    id=$!
    rm -f $out
    while kill -0 $id 2>/dev/null; do
        pgrep -P $id |
            xargs ps -o %mem,%cpu -p 2>/dev/null |
            awk '{memory+=$1;cpu+=$2} END {print memory,cpu}' |
            echo $(date '+%s%N') $(cat -) >>$out
    done
}
