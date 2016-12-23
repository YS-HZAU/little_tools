#data:2016-12-19
#author:xyhuang
#fuc:filter lncRNA
use strict;
use warnings;
use Cwd qw(abs_path);
use Getopt::Long;
use Data::Dumper;
use POSIX;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname);
#----------------------#
#    start script      #
#----------------------#
my $BEGIN_TIME=time();
my $version="1.0.0";
#----------------------#
#    get options       #
#----------------------#
my($gtf,$csv,$protein,$other,$n,$out,$cov);
GetOptions(
  "gtf=s"  => \$gtf,
  "csv=s"  => \$csv,
  "cov=n" => \$cov,
  "protein=s"     => \$protein,
  "other=s"  => \$other,
  "out=s" =>\$out,
  "n=n" =>\$n,
  "help|?" => \&USAGE,
 ) or &USAGE;
&USAGE unless (defined $gtf && defined $csv && defined $protein && defined $other);
$out||="basic.gtf";
$n||=6;
$cov||=5;
open GTF,"$gtf";
open CSV,"$csv";
open CODE,"$protein";
open OTHER,"$other";
open FL,">$out";
my %lnc;
while(<GTF>){
	next if(/^#/);
	next if(/exon/);
#		gene_id "MSTRG.1"; transcript_id "AT1G01180.1"; ref_gene_id "AT1G01180"; 
	$lnc{$2}{$1}=0 if(/gene_id "(.+?)"; transcript_id "(.+?)";/);
}
while(<CODE>){
	next if(/^#/);
#		1	StringTie	transcript	403190	404456	.	-	.	transcript_id "AT1G02140.1"; gene_id "MSTRG.4"; gene_name "MEE63"; xloc "XLOC_004341"; ref_gene_id "AT1G02140"; class_code "u"; tss_id "TSS4583";
	my @tmp=split/\t/,$_;
	next if($tmp[2] eq 'exon');
	my ($t_id,$g_id,$classcode)=($1,$2,$3) if($tmp[-1]=~/transcript_id "(.+?)"; gene_id "(.+?)".+? class_code "(.)";/);
	unless($classcode eq 'j'||$classcode eq 'i'||$classcode eq 'o'||$classcode eq 'u'||$classcode eq 'x'){
		delete $lnc{$t_id};
	}
}
close CODE;
while(<OTHER>){
	next if(/^#/);
#		1	StringTie	transcript	403190	404456	.	-	.	transcript_id "AT1G02140.1"; gene_id "MSTRG.4"; gene_name "MEE63"; xloc "XLOC_004341"; ref_gene_id "AT1G02140"; class_code "u"; tss_id "TSS4583";
	my @tmp=split/\t/,$_;
	next if($tmp[2] eq 'exon');
	my ($t_id,$g_id,$classcode)=($1,$2,$3) if($tmp[-1]=~/transcript_id "(.+?)"; gene_id "(.+?)".+? class_code "(.)";/);
	if($classcode eq '='||$classcode eq 'c'){
		delete $lnc{$t_id};
	}
}
close OTHER;
<CSV>;
my $num=POSIX::ceil($n/3);
while(<CSV>){
	chomp;
	my @tmp=split/,/,$_;
	next unless(exists $lnc{$tmp[0]});
	my $limitcov=$cov*$n;
	my $cov_sum;
	map{$cov_sum+=$_;}@tmp[1,$#tmp];
	my $flag=0;
	foreach(@tmp[1..$#tmp]){
		$flag+=1 if($_>$cov);
	}
	if($flag < $num){
		delete $lnc{$tmp[0]};
	}
	elsif($cov_sum<$limitcov){
		delete $lnc{$tmp[0]};
	}
}
close CSV;
seek(GTF,0,0);
while(<GTF>){
	my $line=$_;
	my @tmp=split/\t/,$line;
	if($line=~/transcript_id "(.+?)";/){
		my $id=$1;
		if($tmp[2] eq 'transcript'){
			my $len=$tmp[4]-$tmp[3]+1;
			delete $lnc{$id} if($len<200);
		}
		print FL"$line" if(exists $lnc{$id});
	}
}
close FL;
close GTF;

sub log_current_time {
	my ($info) = @_;
	my $curr_time = &date_time_format(localtime(time()));
	return "[$curr_time] $info";
#	print "[$curr_time] $info\n";
}
sub date_time_format {
	my ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst)=localtime(time());
	return sprintf("%4d-%02d-%02d %02d:%02d:%02d", $year+1900, $mon+1, $day, $hour, $min, $sec);
}

sub USAGE{
	my $usage=<<"__USAGE__";
#-----------------------------------------------------------
 Program:$Script
 Version:$version
 Contact:1182768992\@qq.com
    Data:2016-12-19
Function:filter gtf file to lncRNA
   USAGE:
		--gtf			merged.gtf
		--csv			coverage for every sample [eg:transcript_count_matrix.csv]
		--cov			if coverage <cov,filter [default:5]
		--protein			compare protein file and merged.gtf [eg:pretein.annotated.gtf]
		--other			compare other file and merged.gtf [eg:other.annotated.gtf]
		--out			the result file [default:./basic.gtf]
		--n			the number for sample [default:6]
		--help			show the docment and exit
 Example:
    perl $Script --gtf merge.gtf --csv transcript_count_matrix.csv --cov 5 --protein pretein.annotated.gtf --other other.annotated.gtf --out basic.gtf --n 6
#---------------------------------------------------------
__USAGE__
   print $usage;
   exit;
}