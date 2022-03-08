/**
 * @version: V1.0.0
 * @author: huang
 * @className: LocalAlign
 * @date: 2022/3/1 0001 21:42
 * @description:
 */

import Data.Frag;
import Data.Linker;
import Util.AlignInfo;
import Util.Tools;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.util.*;

public class LocalAlign {
    public static void main(String[] args) throws IOException {
        if (args.length != 4){
            System.out.println("Usage: java -jar ChIAPETLinkerFilter <input fastq R1> <input fastq R2> <linker1,linker2,linker3,linker4,....> <outputfile>");
            System.exit(1);
        }

        Set<String> linkerSet = new HashSet<>();
        List<Linker> ListLinker = new ArrayList<>();
        for (String x: args[2].split(",")){
            if (linkerSet.contains(x)){
                continue;
            } else {
                ListLinker.add(new Linker(x));
                linkerSet.add(x);
            }
        }
        linkerSet = null;

        BufferedReader fin1 =  Tools.readFile(args[0]);
        BufferedReader fin2 =  Tools.readFile(args[1]);
        BufferedWriter flong = Tools.writeFile(String.format("%s.long.fq.gz",args[3]));
        BufferedWriter fshort = Tools.writeFile(String.format("%s.short.fq.gz",args[3]));
        String line1,line2;
        String rid1,rid2,rseq1,rseq2,rsyb1,rsyb2,rqual1,rqual2;
        Stack<Frag> stacks = new Stack<>();
        List<AlignInfo> splitFrag = new ArrayList<>(ListLinker.size());
        List<AlignInfo> filterFrag = new ArrayList<>(ListLinker.size());
        List<Frag> resultFrag = new ArrayList<>();
        Frag tmpseq;
        while((line1=fin1.readLine())!=null){
            rid1 = line1;
            rseq1 = fin1.readLine();
            rsyb1 = fin1.readLine();
            rqual1 = fin1.readLine();
            rid2 = fin2.readLine();
            rseq2 = fin2.readLine();
            rsyb2 = fin2.readLine();
            rqual2 = fin2.readLine();
            rid1 = rid1.split("\\s+")[0];
            rid1 = rid1.substring(1,rid1.length());
            rid2 = rid2.split("\\s+")[0];
            rid2 = rid2.substring(1,rid2.length());
            if (!rid1.equals(rid2)){
                System.err.println(String.format("the reads is not match \n%s \n%s \n",rid1,rid2));
                System.err.flush();
                System.exit(1);
            }

            stacks.clear();
            stacks.push(new Frag(rseq1,0,rseq1.length()));
            resultFrag.clear();
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
                    if (filterFrag.get(0).maxI != tmpseq.getEnd()){ // 右端不重合
                        stacks.push(new Frag(tmpseq.getSeq(),filterFrag.get(0).maxI,tmpseq.getEnd()));
                    }
                    if (filterFrag.get(0).minI != tmpseq.getStart()) { // 左端不重合
                        stacks.push(new Frag(tmpseq.getSeq(),tmpseq.getStart(),filterFrag.get(0).minI));
                    }
                }
            }
            for (int i=0; i < resultFrag.size(); i++){
                if (resultFrag.get(i).getEnd() - resultFrag.get(i).getStart() >= 55){
                    flong.write(String.format("@%s_R1_%d_%d\n",rid1,resultFrag.size(),i));
                    flong.write(String.format("%s\n",rseq1.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                    flong.write("+\n");
                    flong.write(String.format("%s\n",rqual1.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                } else if (resultFrag.get(i).getEnd() - resultFrag.get(i).getStart() >= 18) {
                    fshort.write(String.format("@%s_R1_%d_%d\n",rid1,resultFrag.size(),i));
                    fshort.write(String.format("%s\n",rseq1.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                    fshort.write("+\n");
                    fshort.write(String.format("%s\n",rqual1.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                }
            }

            stacks.clear();
            stacks.push(new Frag(rseq2,0,rseq2.length()));
            resultFrag.clear();
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
                    if (filterFrag.get(0).maxI != tmpseq.getEnd()){ // 右端不重合
                        stacks.push(new Frag(tmpseq.getSeq(),filterFrag.get(0).maxI,tmpseq.getEnd()));
                    }
                    if (filterFrag.get(0).minI != tmpseq.getStart()) { // 左端不重合
                        stacks.push(new Frag(tmpseq.getSeq(),tmpseq.getStart(),filterFrag.get(0).minI));
                    }
                }
            }
            for (int i=0; i < resultFrag.size(); i++){
                System.out.println(resultFrag.get(i).getStart());
                System.out.println(resultFrag.get(i).getEnd());
                if (resultFrag.get(i).getEnd() - resultFrag.get(i).getStart() >= 55){
                    flong.write(String.format("@%s_R2_%d_%d\n",rid2,resultFrag.size(),i));
                    flong.write(String.format("%s\n",rseq2.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                    flong.write("+\n");
                    flong.write(String.format("%s\n",rqual2.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                } else if (resultFrag.get(i).getEnd() - resultFrag.get(i).getStart() >= 18) {
                    fshort.write(String.format("@%s_R2_%d_%d\n",rid2,resultFrag.size(),i));
                    fshort.write(String.format("%s\n",rseq2.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                    fshort.write("+\n");
                    fshort.write(String.format("%s\n",rqual2.substring(resultFrag.get(i).getStart(),resultFrag.get(i).getEnd())));
                }
            }
        }
        fin1.close();
        fin2.close();
        flong.close();
        fshort.close();
    }
}
