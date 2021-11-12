class Solution:
    m = []
    def letterCasePermutation(self, s):
        print("在迭代中>>>>>>>>>>>>>>>>>>>")           		
        l = list(s)
        self.m.append(list())
        for i in l:
            if ord(i) in range(48,58):
                self.m[-1].append(i)
            else:
                #添加列表m中最后一个元素中的最后一个元素的小写字母
                self.m[-1].append(chr(ord(i) if ord(i)<=90 else ord(i)-32))
                self.stop = l.index(i)
					#迭代添加元素
                self.m[-1].append(self.letterCasePermutation(l[self.stop+1:]))



                #再次型m列表中 添加一个元素，这个元素是m列表中的最后一个元素，只不过将最后一个元素中的最后一个元素大写了
                again = self.m[-1][:]
                again[-1] = chr(ord(again[-1])+32)
                self.m.append(again)

					#迭代添加元素
                self.m[-1].append(self.letterCasePermutation(l[self.stop+1:]))


                break
        if self.stop+1 > len(l):
            return l

        #在这里将m列表中的每个元素都补齐

s = Solution()
s.letterCasePermutation("123a45b67c89")
print(s.m)
