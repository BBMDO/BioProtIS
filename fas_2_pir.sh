#####
#!/bin/bash
name=$(basename $1 .fas)
cp $name.fas $name.sequence # copy your fasta to a new file
sed -i '1d' $name.sequence # remove the top line and rewrite
grep pattern $name.sequence | tr '\n' ' ' # consolidates multiple lines into one
touch temp_pir.ali # make a temp file
cat << EOF >> temp_pir.ali # this copys the following to tempfile
>P1;$name
sequence:$name:::::::0.00: 0.00
EOF
cat $name.sequence >> temp_pir.ali # append the protein sequence to this file
mv temp_pir.ali $name.ali # rename the temp file to match your fasta input file
rm $name.sequence # deletes the temp file containing the seq
#######
