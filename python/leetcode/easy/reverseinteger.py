class Solution:
    """
    we can slice the string 
    string[start,stop, step] 
    """
    def reverse(self, x: int) -> int:
        if x > 0:  # handle positive numbers
            a = int(str(x)[::-1])
        if x <= 0:  # handle negative numbers
            a = -1 * int(str(x * -1)[::-1])
        # handle 32 bit overflow
        mina = -(2 ** 31)
        maxa = 2 ** 31 - 1
        if a not in range(mina, maxa):
            return 0
        else:
            return a


x = Solution()
d = x.reverse(897)
print(d)
