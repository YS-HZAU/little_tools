use strict;
use warnings;
open IN,"<exons.fa";
open OUT,">possible.fa";
$/=">";
<IN>;
my @array;
while(<IN>){
	my @tmp=split/\n/,$_,2;
	$tmp[0]=~s/ /_/g;
	$tmp[1]=~s/\n|>//g;
	push@array,[@tmp];
}
$/="\n";
print OUT">${$_}[0]\n${$_}[1]\n" foreach(@array);
close IN;
close OUT;
