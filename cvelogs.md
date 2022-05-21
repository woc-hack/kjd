
To get all commits that mention cve in their commit message we can use clickhouse database:
```
echo "select lower(hex(sha1)),author, project, comment from commit_all where match(comment, 'CVE') FORMAT CSV" |clickhouse-client --host=da3 --format_csv_delimiter=";" | gzip > CVELog
```
Now we can inspect it: 
```
zcat CVELog|head -3
```

an alternative way is to grep dtails from commit data files:
```
for i in {0..127}
do zcat /da?_data/basemaps/gz/c2chFullU0.s|grep -i 'cve-[0-9][0-9]' | join -t\; <(zcat /da?_data/basemaps/gz/c2PFullU$i.s) - | gzip > c2Pch$i
done  
```

Now we also have projects as in the clickhouse extract above.

To link commits to the files and blobs:
```
for i in {0..127}
do zcat c2Pch$i |join -t\; <(zcat /da?_data/basemaps/gz/c2fbbFullU$i.s) - |gzip > c2fbbPch$i
done
```
Now c2fbbPch$i has everything you might need, including the CVE number in the commit message (last field), 
commit,filename, fixed blob, unfixed blob,project, ...

you can see example for i=0
in /home/audris/swsc/kjd/c2fbbPch0


