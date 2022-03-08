/**
 * @version: V1.0.0
 * @author: huang
 * @className: Test1
 * @date: 2022/3/2 0002 22:06
 * @description:
 */

import Data.Frag;
import Data.Linker;
import Util.AlignInfo;
import Util.Tools;

import java.util.*;

public class Test1 {
    public static void main(String[] args){
        String tmp = "ACGCGATATCTTATCTGACT,AGTCAGATAAGATATCGCGT";
        Set<String> linkerSet = new HashSet<>();
        List<Linker> ListLinker = new ArrayList<>();
        for (String x: tmp.split(",")){
            if (linkerSet.contains(x)){
                continue;
            } else {
                ListLinker.add(new Linker(x));
                linkerSet.add(x);
            }
        }
        linkerSet = null;

        Stack<Frag> stacks = new Stack<>();
        List<AlignInfo> splitFrag = new ArrayList<>(ListLinker.size());
        List<AlignInfo> filterFrag = new ArrayList<>(ListLinker.size());
        List<Frag> resultFrag = new ArrayList<>();
        Frag tmpseq;

        String rseq1 = "TTTTACGCGATATCTTATCTGACTTTTTTTAGTCAGATAAGATATCTTTTTTTTACGCGATATCTTATCTGA";
        stacks.clear();
        stacks.push(new Frag(rseq1,0,rseq1.length()));
        System.out.println(stacks);
        resultFrag.clear();
        filterFrag.clear();
        while(stacks.size() > 0){
            tmpseq = stacks.pop();
            splitFrag.clear();
            filterFrag.clear();
            for (Linker x: ListLinker){
                splitFrag.add(Tools.align(tmpseq,x));
            }
            for (AlignInfo x: splitFrag){
                if (x.nIndels+x.nMismatches <= x.linker.getMaxErr() && x.maxScore >= x.linker.getCutoff()) {
                    filterFrag.add(x);
                }
            }
            if (filterFrag.size() == 0){
                resultFrag.add(tmpseq);
            } else {
                Collections.sort(filterFrag);
//                System.out.println(filterFrag.get(0).maxScore);
//                System.out.println(filterFrag.get(1).maxScore);
//                System.out.println("---------------------------------------");
                if (filterFrag.get(0).maxI != tmpseq.getEnd()){ // 右端不重合
                    stacks.push(new Frag(tmpseq.getSeq(),filterFrag.get(0).maxI,tmpseq.getEnd()));
                }
                if (filterFrag.get(0).minI != tmpseq.getStart()) { // 左端不重合
                    stacks.push(new Frag(tmpseq.getSeq(),tmpseq.getStart(),filterFrag.get(0).minI));
                }
            }
        }
        System.out.println(resultFrag.size());
        System.out.println(resultFrag.get(0).getStart());
        System.out.println(resultFrag.get(0).getEnd());
    }
}
