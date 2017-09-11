echo "running getpid"
for i in $(pgrep dedup);do ps -mo pid,tid,fname,user,psr -p $i;done

