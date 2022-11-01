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
    for (i = 1; i <= NF; i++) {
        split($i,a,":");
        printf("%s", a[2]);
        if (i != NF) {
            printf(", ");
        } 
        if (header[i] != a[1]) {
            printf("\nphase3 Error from fix.awk: mismatch on line %d: %s != %s\n",i, header[i], a[1]);
            exit 1
        }
    }
    printf("\n")
}
