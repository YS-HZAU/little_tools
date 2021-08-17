i=A549CTCF
in1=${i}.1.fq.gz
in2=${i}.2.fq.gz
########################################
##               QC                   ##
########################################
fastqc -t 4 ${i}.1.fq.gz ${i}.2.fq.gz
java -jar ~/Tools/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 -threads 20 ${i}.1.fq.gz ${i}.2.fq.gz ${i}_R1.clean.fq.gz ${i}_R1.unclean.fq.gz ${i}_R2.clean.fq.gz ${i}_R2.unclean.fq.gz ILLUMINACLIP:/public/home/xyhuang/Tools/Trimmomatic-0.36/adapters/NexteraPE-PE.fa:2:30:7:8:true LEADING:10 TRAILING:10 SLIDINGWINDOW:4:15 MINLEN:50
fastqc -t 4 ${i}_R1.clean.fq.gz ${i}_R1.unclean.fq.gz ${i}_R2.clean.fq.gz ${i}_R2.unclean.fq.gz
python /public/home/xyhuang/longread_pipeline/longread_pipeline/program/remove_duplicated_reads.py ${i}_R1.clean.fq.gz ${i}_R2.clean.fq.gz ${i}_R1.clean.uniq.fq.gz ${i}_R2.clean.uniq.fq.gz
python /public/home/xyhuang/longread_pipeline/longread_pipeline/program/remove_duplicated_reads_SE.py ${i}_R1.unclean.fq.gz ${i}_R1.unclean.uniq.fq.gz
python /public/home/xyhuang/longread_pipeline/longread_pipeline/program/remove_duplicated_reads_SE.py ${i}_R2.unclean.fq.gz ${i}_R2.unclean.uniq.fq.gz
