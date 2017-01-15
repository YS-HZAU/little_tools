#!/usr/bin/perl
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
my($in,$g,$t,$l,$sep,$pattern);
GetOptions(
  "in=s"  => \$in,
  "g=s"  => \$g,
  "t=s"     => \$t,
  "l=n"  => \$l,
  "sep=s" =>\$sep,
  "p=s" =>\$pattern,
  "help|?" => \&USAGE,
 ) or &USAGE;
&USAGE unless (defined $in);
$g||="gene_count_matrix.csv";
$t||="transcript_count_matrix.csv";
$l||=75;
$sep||="\t";
$pattern||=".";
my @sample=`ls $in`;
my (%data,$head,%sample);
foreach my $id(@sample){
	chomp($id);
	if($id=~/$pattern+/){
		$sample{$id}=1 if(-d "$in/$id");
	}
}
@sample=sort(keys %sample);
print "sample ID @sample\n";
foreach my $i (@sample) {
	$head.="$sep$i";
	print "load $in/$i/t_data.ctab....\n";
	open IN,"$in/$i/t_data.ctab" ||die "can't find t_data.ctab";
	<IN>;
	while(<IN>){
		chomp;
		my @tmp=split/\t/,$_;
		push @{$data{$tmp[8]}{$tmp[5]}},[$tmp[7],$tmp[10],$i];
	}
	close IN;
}
open TRANS,">$t";
print TRANS"$head\n";
open GENE,">$g";
print GENE"$head\n";
foreach my $gene (keys %data) {
	my (@g_cov,@tmp);
	$g_cov[0]=$gene;
	foreach my $trans (keys %{$data{$gene}}) {
		my @t_cov;
		$t_cov[0]=$trans;
		foreach my $sample (@{$data{$gene}{$trans}}) {
			push @t_cov,POSIX::ceil(${$sample}[1]*${$sample}[0]/$l);
		}
		print TRANS (join $sep,@t_cov)."\n";
		push @tmp,[@t_cov];
	}
	foreach my $lie(1..$#{$tmp[0]}){
		foreach my $hang (0..$#tmp) {
			$g_cov[$lie]+=$tmp[$hang][$lie];
		}
	}
	print GENE (join $sep,@g_cov)."\n";
}
close TRANS;
close GENE;

print "the $Script run ".(time()-$BEGIN_TIME)."s \n";

sub USAGE{
	my $usage=<<"__USAGE__";
#-----------------------------------------------------------
 Program:$Script
 Version:$version
 Contact:1182768992\@qq.com
    Data:2016-12-19
Function:get coverge for deseq
   USAGE:
		--in			data dictionary
		--g			out file for gene ID [default:./gene_count_matrix.csv]
		--t			out file for transript IN [default:./transcript_count_matrix.csv]
		--l			the reads length [default:75]
		--sep			out file's Separator [default:\\t]
		--p			file pattern [default:.]
		--help			show the docment and exit
 Example:
    perl $Script --in count --g gene_count_matrix.csv --t transcript_count_matrix.csv -l 75 --sep , --p sample
#---------------------------------------------------------
__USAGE__
   print $usage;
   exit;
}
