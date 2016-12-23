open CPC,"<cpcput/cpc.result";
open CNCI,"<CNCI/cnci/CNCI.index";
open PLEK,"<PLEK/predicted";
open OUT,">veen.list";
open LNC,">lnc.list";
my (%cpc,%cnci,%plek,@trans_id);
while(<CPC>){
	my @tmp=split/\t/,$_;
	$tmp[0]=$1 if($tmp[0]=~/^(.+?\d)_/);
	$cpc{$tmp[0]}='noncoding' if($tmp[2] eq 'noncoding');
}
close CPC;
<CNCI>;
while(<CNCI>){
	my @tmp=split/\t/,$_;
	$tmp[0]=$1 if($tmp[0]=~/^(.+?\d)_/);
	$cnci{$tmp[0]}='noncoding' if($tmp[1] eq 'noncoding');
}
close CNCI;
while(<PLEK>){
	my @tmp=split/\t/,$_;
	$tmp[2]=$1 if($tmp[2]=~/^>(.+?\d)_/);
	push@trans_id,$tmp[2];
	$plek{$tmp[2]}='noncoding' if($tmp[0] eq 'Non-coding');
}
close PLEK;
print OUT"id\tcpc\tcnci\tplek\n";
foreach my $i(@trans_id){
	if(exists $cpc{$i} || exists $cnci{$i} || exists $plek{$i}){
		my $tmp_cpc=$cpc{$i}||"NA";
		my $tmp_cnci=$cnci{$i}||"NA";
		my $tmp_plek=$plek{$i}||"NA";
		print OUT"$i\t$tmp_cpc\t$tmp_cnci\t$tmp_plek\n";
		if(exists $cpc{$i} && exists $cnci{$i} && exists $plek{$i}){
			print LNC"$i\n";
		}
	}
}
close OUT;
close LNC;

open LIST,"<lnc.list";
my %tmp;
while(<LIST>){
	$_=~s/[\r\n]+//;
	$tmp{$_}=1;
}
close LIST;
open GTF,"<merge.gtf";
open OUT,">lncRNA.gtf";
while(<GTF>){
	$_=~s/[\r\n]+//;
	my $seq=$_;
	my $id=$1 if($seq=~/transcript_id "(.*?)"/);
	print OUT"$seq\n" if(exists $hash{$id});
}
close GTF;
close OUT;
