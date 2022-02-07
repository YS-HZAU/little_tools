aa = "CGAGCTGCTCGCGCGGCGAGAGCGGGCCGCCGCGTGCCGGCCGGGGGACGGACCGGGAACGGCCCCCTCGGGGGCCTTCCCCGGGC"
bb = "GAGCTGCTCGCGCGGCGAGAGCGGGCCGCCGCGTGCCGGCCGGGGGACGGACCGGGAACGGCCCCCTC"

MismatchScore = -1
MatchScore = 1
IndelScore = -2

m = len(aa)
n = len(bb)

scoreMatrix = []
for i in range(m+1):
    scoreMatrix.append([])
    for j in range(n+1):
        scoreMatrix[i].append(0)

for i in range(1,m+1):
    scoreMatrix[i][0] = i*MismatchScore
for i in range(1,n+1):
    scoreMatrix[0][i] = i*MismatchScore
    
for i in range(m):
    for j in range(n):
        if aa[i] == bb[j]:
            scoreMatrix[i+1][j+1] = scoreMatrix[i][j]+MatchScore
        else:
            scoreMatrix[i+1][j+1] = scoreMatrix[i][j]+MismatchScore
        if scoreMatrix[i+1][j+1] < scoreMatrix[i+1][j] + IndelScore:
            scoreMatrix[i+1][j+1] = scoreMatrix[i+1][j]+IndelScore
        if scoreMatrix[i+1][j+1] < scoreMatrix[i][j+1] + IndelScore:
            scoreMatrix[i+1][j+1] = scoreMatrix[i][j+1]+IndelScore

for i in scoreMatrix:
    print(i)
    
i = m-1
j = n-1

str1 = ""
str2 = ""
alignedStatus = ""
while i>=0 or j>=0:
    if i < 0:
        str1 += "-"
        str2 += bb[j]
        alignedStatus += " "
        j -= 1
    elif j < 0:
        str1 += aa[i]
        str2 += "-"
        alignedStatus += " "
        i -= 1
    elif scoreMatrix[i+1][j+1] == scoreMatrix[i][j] + MatchScore and aa[i] == bb[j]:
        str1 += aa[i]
        str2 += bb[j]
        alignedStatus += "|"
        i -= 1
        j -= 1
    elif scoreMatrix[i+1][j+1] == scoreMatrix[i][j] + MismatchScore:
        str1 += aa[i]
        str2 += bb[j]
        alignedStatus += "X"
        i -= 1
        j -= 1
    elif scoreMatrix[i+1][j+1] == scoreMatrix[i][j+1] + IndelScore:
        str1 += aa[i]
        str2 += "-"
        alignedStatus += " "
        i -= 1
    elif scoreMatrix[i+1][j+1] == scoreMatrix[i+1][j] + IndelScore:
        str1 += "-"
        str2 += bb[j]
        alignedStatus += " "
        j -= 1
    else:
        print("error")
print(str1[::-1])
print(alignedStatus[::-1])
print(str2[::-1])
