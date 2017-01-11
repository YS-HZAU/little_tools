#!/usr/bin/perl
use strict;
use warnings;

my $out = shift;
my (%rd1,%rd2);

while (<>) {
     my ($id,$flag,$chr,$pos,$mapQ,$cigar,$pe,$pairpos,$foo,$seq,$qv)=split;
     if ($pe eq '=') {
        my $binflag = reverse(sprintf("%b",$flag));
        if (substr($binflag,6,1) eq '1') {
            $rd1{$id} = "$seq\n+\n$qv\n";
        }
        elsif (substr($binflag,7,1) eq '1') {
            $seq =~ tr/ACGT/TGCA/;
            $seq = reverse($seq);
            $qv = reverse($qv);
            $rd2{$id} = "$seq\n+\n$qv\n";
        }
     }
}

my $ofile1 = $out . "_1.fq";
my $ofile2 = $out . "_2.fq";
open (FD1,">$ofile1") or die "ERROR: cannot open '$ofile1' for writing.$!\n";
open (FD2,">$ofile2") or die "ERROR: cannot open '$ofile2' for writing.$!\n";

while (my ($id,$val) = each(%rd1)) {
     if (exists($rd2{$id})) {
        print FD1 "\@$id/1\n$val";
        print FD2 "\@$id/2\n$rd2{$id}";
     }
}
close(FD1);
close(FD2);
