class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        else:
            reverse_integer = int(str(x)[::-1])
            if x == reverse_integer:
                return True
            else:
                return False


d = Solution()
check = d.isPalindrome(121)
print(check)
