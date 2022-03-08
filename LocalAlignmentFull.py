import sys
import math

def Alignmen(aa,bb,start,end):
    MismatchScore = -1
    MatchScore = 1
    IndelScore = -999 # 设置的更大，就可以避免通过indel
    maxI = 0
    maxJ = 0
    minI = 0
    minJ = 0
    # m = len(aa)
    m = end
    n = len(bb)
    scoreMatrix = []
    maxScore = 0
    for i in range(m+1):
        scoreMatrix.append([])
        for j in range(n+1):
            scoreMatrix[i].append(0)
        
    for i in range(start,m):
        for j in range(n):
            if aa[i] == bb[j]:
                scoreMatrix[i+1][j+1] = scoreMatrix[i][j]+MatchScore
            else:
                scoreMatrix[i+1][j+1] = scoreMatrix[i][j]+MismatchScore
            if scoreMatrix[i+1][j+1] < scoreMatrix[i+1][j] + IndelScore:
                scoreMatrix[i+1][j+1] = scoreMatrix[i+1][j]+IndelScore
            if scoreMatrix[i+1][j+1] < scoreMatrix[i][j+1] + IndelScore:
                scoreMatrix[i+1][j+1] = scoreMatrix[i][j+1]+IndelScore
            if scoreMatrix[i+1][j+1] < 0:
                scoreMatrix[i+1][j+1] = 0
            if maxScore < scoreMatrix[i+1][j+1]:
                maxScore = scoreMatrix[i+1][j+1]
                maxI = i+1
                maxJ = j+1
                
#    for i in scoreMatrix:
#        print(i)
    i = maxI-1
    j = maxJ-1
    nMatches = 0
    nMismatches = 0
    nIndels = 0
    
    alignedStatus = ""
    str1 = ""
    str2 = ""
    scoreGreaterThan0 = 1
    
    while m-1 > i:
        str1 += aa[m-1]
        str2 += "-"
        alignedStatus += " "
        m -= 1
    
    while n-1 > j:
        str1 += "-"
        str2 += bb[n-1]
        alignedStatus += " "
        n -= 1
    
    while i>=0 or j>=0:
        if i < 0:
            str1 += "-"
            str2 += bb[j]
            alignedStatus += " "
            j -= 1
            if scoreGreaterThan0 == 1:
                nIndels += 1
        elif j < 0:
            str1 += aa[i]
            str2 += "-"
            alignedStatus += " "
            i -= 1
            if scoreGreaterThan0 == 1:
                nIndels += 1
        elif scoreMatrix[i+1][j+1] == scoreMatrix[i][j] + MatchScore and aa[i] == bb[j]:
            str1 += aa[i]
            str2 += bb[j]
            alignedStatus += "|"
            i -= 1
            j -= 1
            if scoreGreaterThan0 == 1:
                nMatches += 1
        elif scoreMatrix[i+1][j+1] == scoreMatrix[i][j] + MismatchScore:
            str1 += aa[i]
            str2 += bb[j]
            alignedStatus += "X"
            i -= 1
            j -= 1
            if scoreGreaterThan0 == 1:
                nMismatches += 1
        elif scoreMatrix[i+1][j+1] == scoreMatrix[i+1][j] + IndelScore:
            str1 += "-"
            str2 += bb[j]
            alignedStatus += " "
            j -= 1
            if scoreGreaterThan0 == 1:
                nIndels += 1
        else:
            str1 += aa[i]
            str2 += "-"
            alignedStatus += " "
            i -= 1
            if scoreGreaterThan0 == 1:
                nIndels += 1
        if scoreGreaterThan0 == 1:
            if scoreMatrix[i+1][j+1] <= 0:
                minI = i+1
                minJ = j+1
                scoreGreaterThan0 = 0
    return maxScore,minI,maxI,nMismatches,nIndels

def loadpos(alignarr,stack,tmpseq,pos):
    if alignarr[pos][2] == tmpseq[2]: # 右端重合
        pass
    else:
        stack.append([tmpseq[0],alignarr[pos][2],tmpseq[2]])
    if alignarr[pos][1] == tmpseq[1]: # 左端重合
        pass
    else:
        stack.append([tmpseq[0],tmpseq[1],alignarr[pos][1]])
    
# aa = "TTTTACGCGATATCTTATCTGACTAGTCAGATAAGATATCGCGTACGCGATATCTTATCTGACTTTTTTTTTTTTAGTCAGATAAGATATCGCGTACGCGATATCTTATCTGACTAGTCAGATAAGATATCGCGTTTTTT"
aa = "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTACGCGATATCTTATCTGACTTTTTTTAGTCAGATAAGATATCTTTTTTTTACGCGATATCTTATCTGAT"
bb = "ACGCGATATCTTATCTGACT"
cc = "AGTCAGATAAGATATCGCGT"
maxErr = math.ceil(len(bb)*0.1)
cutoff = math.ceil(len(bb)*0.7)


stack = [[aa,0,len(aa)]]
resultfrag = []
while len(stack) > 0:
    tmpseq = stack.pop()
    alignarr = [Alignmen(tmpseq[0],bb,tmpseq[1],tmpseq[2]),Alignmen(tmpseq[0],cc,tmpseq[1],tmpseq[2])]
    flag1 = False
    if alignarr[0][3] + alignarr[0][4] <= maxErr and alignarr[0][0] > cutoff:
        flag1 = True
    flag2 = False
    if alignarr[1][3] + alignarr[1][4] <= maxErr and alignarr[1][0] > cutoff:
        flag2 = True
    if flag1 and flag2:
        if alignarr[0][0] >= alignarr[1][0]:
            loadpos(alignarr,stack,tmpseq,0)
        elif alignarr[0][0] < alignarr[1][0]:
            loadpos(alignarr,stack,tmpseq,1)
    elif flag1:
        loadpos(alignarr,stack,tmpseq,0)
    elif flag2:
        loadpos(alignarr,stack,tmpseq,1)
    else:
        resultfrag.append([tmpseq[1],tmpseq[2]])
print(resultfrag)        