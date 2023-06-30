from typing import List


class Solution:
    # return the list of added numbers
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # iterate the range of the list: range gives the sequence of the numbers, range(start,stop, increment)
        for i in range(len(nums)):
            # again iterate the same list range
            for y in range(len(nums)):
                # adding each element  of the list 1 and list 2
                if (y != i) and (nums[i] + nums[y] == target):
                    return [i, y]


class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        h = {}
        for i, num in enumerate(nums):
            n = target - num
            if n not in h:
                h[num] = i
            else:
                return [h[n], i]
