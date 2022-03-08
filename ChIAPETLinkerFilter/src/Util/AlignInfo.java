package Util;

import Data.Linker;

/**
 * @version: V1.0.0
 * @author: huang
 * @className: AlignInfo
 * @date: 2022/3/2 0002 21:14
 * @description:
 */
public class AlignInfo implements Comparable<AlignInfo>{
    public int maxScore;
    public int minI;
    public int maxI;
    public int nMismatches;
    public int nIndels;
    public Linker linker;
    public AlignInfo(int a, int b, int c, int d, int e, Linker f) {
        maxScore = a;
        minI = b;
        maxI = c;
        nMismatches = d;
        nIndels = e;
        linker = f;
    }
    @Override
    public int compareTo(AlignInfo o) {
        if (this == o) {
            return 0;
        }
        return o.maxScore - maxScore;
    }
    @Override
    public String toString(){
        return String.format("%d\t%d\t%d\t%d\t%d",maxScore,minI,maxI,nMismatches,nIndels);
    }
}
