package Util;

/**
 * @version: V1.0.0
 * @author: huang
 * @className: Tools
 * @date: 2022/3/1 0001 21:19
 * @description:
 */

import Data.Frag;
import Data.Linker;

import java.io.*;
import java.util.Arrays;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

public class Tools {
    public static BufferedReader readFile(String fileIN) throws IOException {
        BufferedReader filehandle;
        if (fileIN.endsWith("gz") || fileIN.endsWith("GZ") || fileIN.endsWith("gzip") || fileIN.endsWith("GZIP")) {
            filehandle = new BufferedReader(new InputStreamReader(new GZIPInputStream(new FileInputStream(fileIN))));
        } else {
            filehandle = new BufferedReader(new InputStreamReader(new FileInputStream(fileIN)));
        }
        return filehandle;
    }

    public static BufferedWriter writeFile(String fileOUT) throws IOException {
        BufferedWriter filehandle;
        if (fileOUT.endsWith("gz") || fileOUT.endsWith("GZ") || fileOUT.endsWith("gzip") || fileOUT.endsWith("GZIP")) {
            filehandle = new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(new FileOutputStream(fileOUT))));
        } else {
            filehandle = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileOUT)));
        }
        return filehandle;
    }

    private static char[] complementTable = new char[255];
    static {
        complementTable['A'] = 'T';
        complementTable['C'] = 'G';
        complementTable['G'] = 'C';
        complementTable['T'] = 'A';
        complementTable['a'] = 't';
        complementTable['c'] = 'g';
        complementTable['g'] = 'c';
        complementTable['t'] = 'a';

        complementTable['R'] = 'Y';
        complementTable['Y'] = 'R';
        complementTable['M'] = 'K';
        complementTable['K'] = 'M';
        complementTable['r'] = 'y';
        complementTable['y'] = 'r';
        complementTable['m'] = 'k';
        complementTable['k'] = 'n';

        complementTable['V'] = 'B';
        complementTable['B'] = 'V';
        complementTable['H'] = 'D';
        complementTable['D'] = 'H';
        complementTable['v'] = 'b';
        complementTable['b'] = 'v';
        complementTable['h'] = 'd';
        complementTable['d'] = 'h';

        complementTable['N'] = 'N';
        complementTable['n'] = 'n';

    }

    public static String rc(String seq) {
        StringBuffer result = new StringBuffer(seq);
        result.reverse();
        for (int i = seq.length() - 1; i >= 0; i--) {
            result.setCharAt(i, complementTable[result.charAt(i)]);
        }
        return result.toString();
    }

    public static AlignInfo align(Frag aa, Linker bb) {
        int MatchScore = 1;
        int MismatchScore = -1;
        int IndelScore = -999;
        int maxI = 0; // at row maxI, the score is maximum
        int maxJ = 0; // at column maxJ, the score is maximum
        int minI = 0; // at row minI, the maximum score starts from here
        int minJ = 0; // at column minJ, the maximum score starts from here
        int m = aa.getEnd();
        int n = bb.getSeq().length();
        int maxScore = 0;
        int[][] scoreMatrix = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) {
            Arrays.fill(scoreMatrix[i], 0);
        }

        int index1, index2;
        for (index1 = aa.getStart(); index1 < m; index1++) {
            for (index2 = 0; index2 < n; index2++) {
                if (aa.getSeq().charAt(index1) == bb.getSeq().charAt(index2)) {
                    scoreMatrix[index1 + 1][index2 + 1] = scoreMatrix[index1][index2] + MatchScore;
                } else {
                    scoreMatrix[index1 + 1][index2 + 1] = scoreMatrix[index1][index2] + MismatchScore;
                }
                if (scoreMatrix[index1 + 1][index2 + 1] < scoreMatrix[index1 + 1][index2] + IndelScore) {
                    scoreMatrix[index1 + 1][index2 + 1] = scoreMatrix[index1 + 1][index2] + IndelScore;
                }
                if (scoreMatrix[index1 + 1][index2 + 1] < scoreMatrix[index1][index2 + 1] + IndelScore) {
                    scoreMatrix[index1 + 1][index2 + 1] = scoreMatrix[index1][index2 + 1] + IndelScore;
                }
                if (scoreMatrix[index1 + 1][index2 + 1] < 0) {
                    scoreMatrix[index1 + 1][index2 + 1] = 0;
                }
                if (maxScore < scoreMatrix[index1 + 1][index2 + 1]) {
                    maxScore = scoreMatrix[index1 + 1][index2 + 1];
                    maxI = index1 + 1;
                    maxJ = index2 + 1;
                }
            }
        }

//        for (index1 = 0; index1 <= m; index1++) {
//            for (index2 = 0; index2 <= n; index2++) {
//                System.out.print("\t" + scoreMatrix[index1][index2]);
//            }
//            System.out.println();
//        }

        index1 = maxI - 1;
        index2 = maxJ - 1;
        int nMatches = 0;
        int nMismatches = 0;
        int nIndels = 0;
        StringBuffer alignedStr1 = new StringBuffer();
        StringBuffer alignedStr2 = new StringBuffer();
        StringBuffer alignedStatus = new StringBuffer();
        int scoreGreaterThan0 = 1;

        while (m-1 > index1) {
            alignedStr1.append(aa.getSeq().charAt(m - 1));
            alignedStr2.append('-');
            alignedStatus.append(' ');
            m--;
        }
        while (n-1 > index2) {
            alignedStr1.append('-');
            alignedStr2.append(bb.getSeq().charAt(n-1));
            alignedStatus.append(' ');
            n--;
        }
        while ((index1 >= 0) || (index2 >= 0)) {
            if (index1 < 0) { // deletion at the beginning of str1, insertion in str2
                alignedStr1.append('-');
                alignedStr2.append(bb.getSeq().charAt(index2));
                alignedStatus.append(' ');
                index2--;
                if (scoreGreaterThan0 == 1) {
                    nIndels++;
                }
            } else if (index2 < 0) { // insertion in str1, deletion at the beginning of str2
                alignedStr1.append(aa.getSeq().charAt(index1));
                alignedStr2.append('-');
                alignedStatus.append(' ');
                index1--;
                if (scoreGreaterThan0 == 1) {
                    nIndels++;
                }
            } else if ((scoreMatrix[index1 + 1][index2 + 1] == scoreMatrix[index1][index2] + MatchScore) && (aa.getSeq().charAt(index1) == bb.getSeq().charAt(index2))) {
                // match from both strs
                alignedStr1.append(aa.getSeq().charAt(index1));
                alignedStr2.append(bb.getSeq().charAt(index2));
                alignedStatus.append('|');
                index1--;
                index2--;
                if (scoreGreaterThan0 == 1) {
                    nMatches++;
                }
            } else if (scoreMatrix[index1 + 1][index2 + 1] == scoreMatrix[index1][index2] + MismatchScore) {
                // mismatch from both strs
                alignedStr1.append(aa.getSeq().charAt(index1));
                alignedStr2.append(bb.getSeq().charAt(index2));
                alignedStatus.append('X');
                index1--;
                index2--;
                if (scoreGreaterThan0 == 1) {
                    nMismatches++;
                }
            } else if (scoreMatrix[index1 + 1][index2 + 1] == scoreMatrix[index1 + 1][index2] + IndelScore) {
                // deletion in str1, insertion in str2
                alignedStr1.append('-');
                alignedStr2.append(bb.getSeq().charAt(index2));
                alignedStatus.append(' ');
                index2--;
                if (scoreGreaterThan0 == 1) {
                    nIndels++;
                }
            } else {
                // insertion in str1, deletion in str2
                //if (scoreMatrix[index1 + 1][index2 + 1] == scoreMatrix[index1][index2 + 1] + IndelScore)
                alignedStr1.append(aa.getSeq().charAt(index1));
                alignedStr2.append('-');
                alignedStatus.append(' ');
                index1--;
                if (scoreGreaterThan0 == 1) {
                    nIndels++;
                }
            }
            if (scoreGreaterThan0 == 1) {
                if (scoreMatrix[index1 + 1][index2 + 1] <= 0) {
                    minI = index1 + 1;
                    minJ = index2 + 1;
                    scoreGreaterThan0 = 0;
                }
            }
        }
//        alignedStr1.reverse();
//        alignedStr2.reverse();
//        alignedStatus.reverse();
//        System.err.println("str1: " + aa);
//        System.err.println("str2: " + bb);
//        System.err.println("aligned score: " + maxScore);
//        System.err.println("aligned str1      : " + alignedStr1);
//        System.err.println("aligned strStatus : " + alignedStatus);
//        System.err.println("aligned str2      : " + alignedStr2);
//        System.err.println("aligned minI      : " + minI);
//        System.err.println("aligned maxI      : " + maxI);
//        System.err.println("aligned minJ      : " + minJ);
//        System.err.println("aligned maxJ      : " + maxJ);
//        System.err.println("aligned nMatches  : " + nMatches);
//        System.err.println("aligned nMismatches: " + nMismatches);
//        System.err.println("aligned nIndels   : " + nIndels);
        return new AlignInfo(maxScore,minI,maxI,nMismatches,nIndels,bb);
    }
}
