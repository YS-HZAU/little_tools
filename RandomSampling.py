import numpy as np

# choice(a, size=None, replace=True, p=None)
# 表示从a中随机选取size个数
# replacement 代表的意思是抽样之后还放不放回去，如果是False的话，那么通一次挑选出来的数都不一样，如果是True的话， 有可能会出现重复的，因为前面的抽的放回去了。
# p表示每个元素被抽取的概率，如果没有指定，a中所有元素被选取的概率是相等的。

# 有放回抽样
np.random.choice(5, 3) # 和np.random.randint(0,5,3)意思相同，表示从[0,5)之间随机以等概率选取3个数
np.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0]) # 表示分别以p=[0.1, 0, 0.3, 0.6, 0]的概率从[0,1,2,3,4]这四个数中选取3个数

# 无放回抽样
np.random.choice(a=5, size=3, replace=False, p=None)
np.random.choice(a=5, size=3, replace=False, p=[0.2, 0.1, 0.3, 0.4, 0.0])

aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])