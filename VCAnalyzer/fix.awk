#
# Convert cvs file with name value pairs to just values.
# usage: cat report.csv | awk -F "," -f ~/kjd/VCAnalyzer/fix.awk > report.values.csv
#
{
    # print the column headings first
    if (NR == 1) {
        for (i = 1; i <= NF; i++) {
            split($i,a,":");
            printf("%s", a[1]);
            if (i != NF) {
                printf(",");
            }
            header[i]=a[1];
        }
        printf("\n");
    }
    # first, check to see if the record is valid
    for (i = 1; i <= NF; i++) {
        split($i,a,":");
        if (header[i] != a[1]) {
            printf("phase3 Error from fix.awk: mismatch on line %d: %s != %s, NF=%d\n",NR, header[i], a[1], NF) >> "/dev/stderr";
            next;
        }
    }
    # then, print the fields
    for (i = 1; i <= NF; i++) {
        split($i,a,":");
        printf("%s", a[2]);
        if (i != NF) {
            printf(", ");
        } 
    }
    printf("\n")
}
