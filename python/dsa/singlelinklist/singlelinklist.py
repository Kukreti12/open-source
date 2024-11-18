class Node:
    def __init__(self,value):
        self.value=value
        self.next=None
        
class singlelinklist:
    def __init__(self):
        self.head=None
        self.tail=None
        self._length=0
        
    def append(self,value):
        # first create the new value and keep it in a container
        new_node=Node(value)
        # check if the link list is empty
        if not self._length:
            self.head=self.tail=new_node
        else:
            self.tail.next=new_node
            # Update the tail of the node
            self.tail=new_node
        self._length+=1
        return self
    def preappend(self,value):
        new_node=Node(value)
        if not self._length:
            self.head=self.tail=new_node
        else:
            new_node.next=self.head
            self.head=new_node
        self._length+=1
        return self
    
    
my_list=singlelinklist()
my_list.append(3)

print(my_list._length)
print(my_list.head.value)
print(my_list.tail.value)

my_list.append(4)
print(my_list.head.value)
print(my_list.tail.value)