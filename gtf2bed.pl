#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
open GTF,"<$ARGV[0]";
open BED,">$ARGV[0].bed";

my $chr;
my $exonstart;
my $exonend;
my $trans_id;
my $score=0;
my $strand;
my $CDSstart;
my $CDSend;
my $color=0;
my $exoncount;
my @exonlen;
my @exonloci;

my %trans;																		#trans_id => chrom => strand => exon => exon array && trans_id => chrom => strand => CDS => CDS array

while(<GTF>){
	next if(/^#/);
	my @data=split/\t/,$_;
	next unless($data[2] eq 'exon'||$data[2] eq 'CDS');
    my $trans=$1 if($data[8]=~/transcript_id "(.+?)";/);
	if(scalar(keys %trans)==0){													#accept the first data and no longer use it
		if($data[2] eq 'exon'){
			push@{$trans{$trans}{$data[0]}{$data[6]}{exon}},[$data[3],$data[4]];
		}
		else {
			push@{$trans{$trans}{$data[0]}{$data[6]}{CDS}},($data[3],$data[4]);
		}
		next;
	}
	if(!exists $trans{$trans}){													#to determine whether the change for trans_id,if changed,print result.if not,push data to %trans
		$trans_id=(keys%trans)[0];
		$chr=(keys%{$trans{$trans_id}})[0];
		$strand=(keys%{$trans{$trans_id}{$chr}})[0];
		my @exon=@{$trans{$trans_id}{$chr}{$strand}{exon}};
		@exon=reverse@exon if($strand eq '-');									#if strand='-',we should reverse the exon array
		foreach(@exon){
			push@exonlen,(${$_}[1]-${$_}[0]+1);
			push@exonloci,(${$_}[0]-${$exon[0]}[0]);
		}
		$exonstart=${$exon[0]}[0]-1;
		$exonend=${$exon[-1]}[1];
		my @CDS;
		if (exists $trans{$trans_id}{$chr}{$strand}{CDS}){						#for ncRNA,usually they don't have CDS.So give the exon array to CDS array 
			@CDS=@{$trans{$trans_id}{$chr}{$strand}{CDS}};
		}
		else{
			push@CDS,(${$_}[0],${$_}[1]) foreach(@exon);
		}
		@CDS=reverse@CDS if($strand eq '-');
		$CDSstart=$CDS[0]-1;
		$CDSend=$CDS[-1];
		$exoncount=scalar(@exon);
		print BED"$chr\t$exonstart\t$exonend\t$trans_id\t$score\t$strand\t$CDSstart\t$CDSend\t$color\t$exoncount\t".(join",",(@exonlen,"\t")).(join",",(@exonloci,"\n"));
		undef(@exonlen);
		undef(@exonloci);
		delete $trans{$trans_id};
		if($data[2] eq 'exon'){
			push@{$trans{$trans}{$data[0]}{$data[6]}{exon}},[$data[3],$data[4]];
		}
		else {
			push@{$trans{$trans}{$data[0]}{$data[6]}{CDS}},($data[3],$data[4]);
		}
	}
	else{
		if($data[2] eq 'exon'){
			push@{$trans{$trans}{$data[0]}{$data[6]}{exon}},[$data[3],$data[4]];
		}
		else {
			push@{$trans{$trans}{$data[0]}{$data[6]}{CDS}},($data[3],$data[4]);
		}
	}
}
$trans_id=(keys%trans)[0];														#count for the last data.
$chr=(keys%{$trans{$trans_id}})[0];
$strand=(keys%{$trans{$trans_id}{$chr}})[0];
my @exon=@{$trans{$trans_id}{$chr}{$strand}{exon}};
@exon=reverse@exon if($strand eq '-');
foreach(@exon){
	push@exonlen,(${$_}[1]-${$_}[0]+1);
	push@exonloci,(${$_}[0]-${$exon[0]}[0]);
}
$exonstart=${$exon[0]}[0]-1;
$exonend=${$exon[-1]}[1];
my @CDS;
if (exists $trans{$trans_id}{$chr}{$strand}{CDS}){
	@CDS=@{$trans{$trans_id}{$chr}{$strand}{CDS}};
}
else{
	push@CDS,(${$_}[0],${$_}[1]) foreach(@exon);
}
@CDS=reverse@CDS if($strand eq '-');
$CDSstart=$CDS[0]-1;
$CDSend=$CDS[-1];
$exoncount=scalar(@exon);
print BED"$chr\t$exonstart\t$exonend\t$trans_id\t$score\t$strand\t$CDSstart\t$CDSend\t$color\t$exoncount\t".(join",",(@exonlen,"\t")).(join",",(@exonloci,"\n"));
close GTF;
close BED;