list1= ['a','b','c','d']
list2 =['e','f','g','h','i']


def check(list):
    for i in list:
        ## Here the complexity of the problem is big O(N). 
        # If we increase the number of elements then the number of operation is also increasing linearly.
        if i == 'A':
            print("Available")
            
            
check(list1)            

