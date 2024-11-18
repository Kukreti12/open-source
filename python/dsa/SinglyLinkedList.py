# Python built in list
# list
# If we have the million object in list and if we add or delete any object then it will effect all the index of the list. thats the reason we have the linked list concept
# Singly linked list
# create node
# create linked list
# add nodes to the end of the linked list
# print linked list

class Node:
    def __init__(self,data) -> None:
        self.data=data
        self.next=None

class LinkedList:
    def __init__(self) -> None:
        self.head = None
    
    def insert(self,newNode):
        if self.head == None:
            self.head = newNode
        else:
            lastNode = self.head
            while True:
                if lastNode.next is None:
                    break
                lastNode =lastNode.next
            lastNode.next = newNode
    def listLen(self):
        currentNode = self.head
        length = 0
        while currentNode is not None:
            length+=1            
            currentNode =currentNode.next
        return length
    
    def printList(self):
        if self.head is None:
            print("your linkedList is empty")
            return None
        currentNode = self.head
        while True:
            if currentNode is None:
                break
            print(currentNode.data)
            currentNode = currentNode.next
            
    def insertHead(self,newNode):
        """
        Below module is to add the node in the starting of the list
        """
        if self.head is None:
            self.head=newNode
        else:
            tmpNode = self.head
            # Sets the head of the node to the new node
            self.head = newNode
            self.head.next = tmpNode
            del tmpNode
            
    def insertBtwNode(self, newNode, position):
        if position == 0:  # Insert at the head
            self.insertHead(newNode)
            return
        elif position < 0 or position > self.listLen():
            print("Invalid position")
            return
        
        currentPosition = 0
        currentNode = self.head
        previousNode = None
        
        while currentPosition < position:
            previousNode = currentNode
            currentNode = currentNode.next
            currentPosition += 1

        # Insert the new node between previousNode and currentNode
        previousNode.next = newNode
        newNode.next = currentNode
    def dellastnode(self):
        """
        delete the last node
        """
        if self.islistempty is False:
            if self.head.next is None:
                self.delhead()
                return
        previous=None
        current=self.head
        nextitem=current.next
        while current.next is not None:
            previous=current
            current=current.next
        previous.next=None
    def islistempty(self):
          if self.head is None:
              return True
        
    def delhead(self):
        if self.islistempty is False:    
            data =self.head
            nextitem=data.next
            self.head=nextitem
            data.next  = None
        else:
            print("Linked list is empty")
    def deletebetween(self, position):
        currentPosition=0
        currentNode = self.head
        while True:
            if currentPosition == position:
                prevnode.next=currentNode.next
                currentNode.next=None
                break
            prevnode =currentNode
            currentNode=currentNode.next
            currentPosition+=1
        
firstNode = Node("John")
linkedlist = LinkedList()
linkedlist.insert(firstNode)
secondNode= Node("saurabh")
linkedlist.insert(secondNode)
thirdNode = Node("Gaurav")
linkedlist.insert(thirdNode)
preadd =Node("test")
linkedlist.insertHead(preadd)
inbetween =Node("inbetween")
linkedlist.insertBtwNode(inbetween,3)
linkedlist.printList()
linkedlist.dellastnode()
print("--------------deletelastnode------------------------")
linkedlist.printList()
print("--------------delete head------------------------")
linkedlist.delhead()
linkedlist.printList()
linkedlist.deletebetween(1)
print("--------------delete between nodes------------------------")
linkedlist.printList()