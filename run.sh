
for i in {1..10}
do
    python ./kagome/main.py -L ${i} -W ${i} --inputFile ./results/kagome/HYBRID/kagome_L_${i}_${i}_HYBRID_sam1_.txt >> kagome_analysis.txt
done