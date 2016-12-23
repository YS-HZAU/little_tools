use strict;
use warnings;
use FileHandle;
my $in=$ARGV[0];
my %data;
open IN,"<$in";
while(<IN>){
	my $line=$_;
	push@{$data{$1}},$line if($line=~/gene_biotype "(.+?)";/);
}
my %fh;
my @type=keys %data;
foreach(@type){
	open $fh{$_},">$_.gtf" or die;
}
foreach my $i (@type){
	foreach my $j (@{$data{$i}}){
		$fh{$i}->print("$j");
	}
 }
