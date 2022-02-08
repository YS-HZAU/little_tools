import sys

aa = "GTGAGCTGCCTTGGAAAAGGTTTGACATCATGGTCTCACCCTCCAGGCATTCGCAATGCTGTTGAAGCACTCTGGGCAATTCGGCTGGATTGCAACAGCCTCCTCGTTCTTCGCGATGCACATGTCAAACTCTCGTAGCTAAACCAAATC"
bb = "GCCTTGGAAAAGGTTTGACATCATGGTCTCACCCTCCAGGCATTCGCAATGCTGTTGAAGCACTCTGGGCAATTCGGCTGGATTGCAACAGCCTCCTCGTTCTTCGCGATGCACATGTCAACCTCTCGTAGCTAAACCAAAT"

MismatchScore = -1
MatchScore = 1
IndelScore = -2 # 设置的更大，就可以避免通过indel

maxI = 0
maxJ = 0
minI = 0
minJ = 0

start = 0

m = len(aa)
n = len(bb)

scoreMatrix = []
maxScore = 0
for i in range(m+1):
    scoreMatrix.append([])
    for j in range(n+1):
        scoreMatrix[i].append(0)
    
for i in range(m):
    for j in range(start,n):
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
            
for i in scoreMatrix:
    print(i)
print(maxScore)
    
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
print(str1[::-1])
print(alignedStatus[::-1])
print(str2[::-1])
print(minI)
print(maxI)
print(minJ)
print(maxJ)
print(nMatches)
print(nMismatches)
print(nIndels)
