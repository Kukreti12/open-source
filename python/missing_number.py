def missing_number(arr, n):
    for i in n:
        if i not in arr:
            return i
        