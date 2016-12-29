use strict;
use warnings;
use Data::Dumper;
use Getopt::Long;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname);
my ($help,$gtf,$fa,$out,$type);
GetOptions(
			"h|help"=>\$help,
			"gtf:s"=>\$gtf,
			"fa:s"=>\$fa,
			"type:s"=>\$type,
			"out:s"=>\$out,
);
&USAGE unless ( $gtf and $fa and $out);
#--------------------------------------------------------------------------------
my $BEGIN_TIME=time();
&log_current_time("$Script start¡­¡­");
&log_current_time("load gtf file start¡­¡­");
$type||="transcript";
my %hash;
open GTF,"<$gtf";
while(<GTF>){
	chomp;
	my @tmp=split"\t",$_;
	my $id=$1 if($tmp[8]=~/$type\_id "(.*?)";/);
	$hash{$id}{$tmp[0]}{$tmp[6]}{$tmp[3]}=$tmp[4];
}
close GTF;
#--------------------------------------------------------------------------------
&log_current_time("load gtf file end");
&log_current_time("load fa file start¡­¡­");
my %hash_chr;
open FA,"<$fa";
$/=">";
<FA>;
while(<FA>){
	my @tmp=split"\n",$_,2;
	my $chr=(split/\s+/,$tmp[0])[0];
	$hash_chr{$chr}=$tmp[1];
}
$/="\n";
foreach(keys %hash_chr){
	$hash_chr{$_}=~s/\s+//g;
}
#--------------------------------------------------------------------------------
&log_current_time("load fa file end");
&log_current_time("print result start¡­¡­");
open OUT,">$out";
my @id=map $_->[0],sort{$a->[1]<=>$b->[1]}map{[$_,/(\d+)/]}keys %hash;
foreach my $id(@id){
	foreach my $chr(keys %{$hash{$id}}){
		foreach my $chain(keys %{$hash{$id}{$chr}}){
			my (@str,@loci,$str);
			foreach my $start(sort{$a<=>$b} keys %{$hash{$id}{$chr}{$chain}}){
				my $length=$hash{$id}{$chr}{$chain}{$start}-$start+1;
				push @str,substr($hash_chr{$chr},$start-1,$length);
				push@loci,$hash{$id}{$chr}{$chain}{$start};
				push@loci,$start;
			}
			my ($begin,$last)=(sort{$a<=>$b}@loci)[0,$#loci];
			if($chain eq '-'){
				$str=join"",@str;
				$str=reverse($str);
				$str=~tr/ATCGatcg/TAGCTAGC/;
				print OUT">$id\_$chr\_$begin-$last\_$chain\n";
				print OUT"$str\n";
			}
			elsif($chain eq '+'){
				$str=join"",@str;
				print OUT">$id\_$chr\_$begin-$last\_$chain\n";
				print OUT"$str\n";
			}
			else{
				$str=join"",@str;
				print OUT">$id\_$chr\_$begin-$last\_$chain\+\n";
				print OUT"$str\n";
				$str=join"",@str;
				$str=reverse($str);
				$str=~tr/ATCGatcg/TAGCTAGC/;
				print OUT">$id\_$chr\_$begin-$last\_$chain\-\n";
				print OUT"$str\n";
			}
		}
	}
}
#--------------------------------------------------------------------------------
&log_current_time("print result end");
&log_current_time("$Script end");
my $run_time=time()-$BEGIN_TIME;
print "$Script run time :$run_time\.s\n";
#--------------------------------------------------------------------------------
# Function
#--------------------------------------------------------------------------------
sub log_current_time {
	my ($info) = @_;
	my $curr_time = &date_time_format(localtime(time()));
	print "[$curr_time] $info\n";
}

sub date_time_format {
	my ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst)=localtime(time());
	return sprintf("%4d-%02d-%02d %02d:%02d:%02d", $year+1900, $mon+1, $day, $hour, $min, $sec);
}

sub USAGE {
	my $usage=<<"USAGE";
Program: $Script
Data:2016.05.06
Function:get lnc or gene sequence by gtf file and fa file
Usage:
  Options:
	gtf		gtf file		must
	fa		fa file			must
	out		out file		must
	type		gene or transcript	optional
	h		Help			optional
	example:perl $Script --gtf merged.gtf --fa fa.fastq --out lnc.fa
USAGE
	print $usage;
	exit;
}