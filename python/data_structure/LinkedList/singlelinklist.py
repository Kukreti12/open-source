from typing import AnyStr


class linkedlist:
    """LIFO stack implementation using a single linked list for storage"""

    # ---------------------------------nested _node class--------------------------------#
    class _node:
        """ "non public class for stroing a single linked class"""

        __slots__ = "_element", "_next"  # streamline memory usage

        def __init__(self, element, next):  # intialize node fields
            self._element = element  # reference to user element
            self._next = next  # reference to next node

    # ---------------------------------stack methods-------------------------------------#

    def __init__(self):
        """create an empty stack"""
        self._head=None  #reference the head node
        self._size=0 #number of stack element

    def __len__(self):
        """return the length of the stack"""
        return self._size

    def is_empty(self):
        """return true if the stack is empty"""
        return self._size==0
   
    def push(self,e):
        """add element e to the top of the stack"""
        self._head=self._node(e,self._head)
        self._size+=1

    def top(self):
        """return the element at the top of the stack. Raise Empty exception if the stack is empty"""
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element

    def pop(self):
        """remove and return the element from the top of the stack
        Raise empty exception if the stack is empty"""
        if self.is_empty():
            raise Empty("stack is empty")
        answer = self._head._element
        self._head=self._head._next
        self._size-=1
        return answer


