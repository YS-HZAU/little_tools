use strict;
use warnings;

sub overlap{
    my ($s1,$e1,$s2,$e2) = @_;
    ($s1,$e1,$s2,$e2) = ($s2,$e2,$s1,$e1) if ($s1 > $s2);
    if ($s2 >= $e1){ # no overlap
        return 0,$s2-$e1+1;
    }elsif($e2 >= $e1){
        return 1,$e1-$s2;
    }else{
        return 1,$e2-$s2;
    }
}

while(<>){
    chomp;
    my $line = $_;
    my @tmp = split /\t/,$line;
    my ($over,$dis) = (-1,-1);
    if($tmp[0] eq $tmp[3]){
        ($over,$dis) = overlap($tmp[1],$tmp[2],$tmp[4],$tmp[5]);
    }
    print "$line\t$over\t$dis\n";
}