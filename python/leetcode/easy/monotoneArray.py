class Solution(object):
    def isMonotonic(self, A):
        return (all(A[i] <= A[i+1] for i in range(len(A) - 1)) or  # all will check all the elements in tuple or list as true
                all(A[i] >= A[i+1] for i in range(len(A) - 1)))

