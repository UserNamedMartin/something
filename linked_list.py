# linked list 

class Node :
    '''
    Node is an element of a linked list.
    Contains:
    - self.data : data of the element of linked list
    - self.next : link to the next node of linked list
    '''
    def __init__(self, data) :
        self.data = data
        self.next = None

class LinkedList :
    def __init__(self) -> None:
        self.head = None
    def append(self, data) -> None: # Adds element to the end of the list
        new_node = Node(data)
        if not self.head : 
            self.head = new_node
        else :
            prev_node = None
            cur_node = self.head
            while cur_node :
                prev_node = cur_node
                cur_node = cur_node.next
            prev_node.next = new_node
    def print_list(self) -> None: # Prints elements of the list 
        cur_node = self.head
        if not cur_node :
            print('List is empty')
        else:
            while cur_node :
                print(cur_node.data, end=' ')
                cur_node = cur_node.next
        print()
    def prepend(self, data) -> None: # Adds element in the beginning of the list
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    def insert_after(self, after_data, insert_data) -> None: # Inserts element after element with 'after_data'
        new_node = Node(insert_data)
        cur_node = self.head
        while cur_node and cur_node.data != after_data :
            cur_node = cur_node.next
        if not cur_node :
            raise ValueError ('Incorrenct input "after_data" : ' + str(after_data))
        new_node.next = cur_node.next
        cur_node.next = new_node
    def delete_data(self, data) -> None: # Deletes element with 'data'
        prev_node = None
        cur_node = self.head
        while cur_node and cur_node.data != data :
            prev_node = cur_node
            cur_node = cur_node.next
        if not cur_node : # If not found
            raise ValueError ('Incorrenct input "data" : ' + str(data))
        if not prev_node : # If first element
            self.head = cur_node.next
            cur_node = None
        else :
            prev_node.next = cur_node.next
            cur_node = None
    def delete_ind(self, ind:int) -> None: # Deletes element with particular index
        cur_node = self.head
        if not cur_node :
            raise ValueError ('The list is empty!')
        count = 0 
        prev_node = None
        while cur_node and count != ind :
            prev_node = cur_node
            cur_node = cur_node.next
            count += 1
        if cur_node is None: # If ind in out of range
            raise ValueError ('Index ' + str(ind) + ' is out of range')
        if not prev_node : # If ind == 0
            self.head = cur_node.next
            cur_node = None
        else :
            prev_node.next = cur_node.next
            cur_node = None
    def length(self) -> int: # Returns length of the list
        count = 0
        cur_node = self.head
        while cur_node :
            cur_node = cur_node.next
            count += 1 
        return count
    def swap_nodes(self, data_1, data_2) -> None: # Swaps places of elements with values "data_1" and "data_2"
        if data_1 == data_2 :
            raise ValueError ('Incorrect input : "data_1" and "data_2" are the same: ' + str(data_1))
        
        prev_node_1 = None
        cur_node_1 = self.head
        prev_node_2 = None
        cur_node_2 = self.head
        while cur_node_1 and cur_node_2 and (cur_node_1.data != data_1 or cur_node_2.data != data_2) :
            if cur_node_1.data != data_1 :
                prev_node_1 = cur_node_1
                cur_node_1 = cur_node_1.next
            if cur_node_2.data != data_2 :
                prev_node_2 = cur_node_2
                cur_node_2 = cur_node_2.next

        if not cur_node_1 :
            raise ValueError ('Incorrect input "data_1" : ' + str(data_1))
        if not cur_node_2 :
            raise ValueError ('incorrenct input "data_2" : ' + str(data_2))
        
        if not prev_node_1 :
            self.head = cur_node_2
        else :
            prev_node_1.next = cur_node_2
        if not prev_node_2 :
            self.head = cur_node_1
        else :
            prev_node_2.next = cur_node_1

        cur_node_1.next, cur_node_2.next = cur_node_2.next, cur_node_1.next
    def reverse(self) -> None: # Reverses the list
        cur_node = self.head
        prev_node = None
        if not cur_node :
            raise ValueError ('The list is emply!')
        while cur_node :
            next_node = cur_node.next
            cur_node.next = prev_node
            prev_node = cur_node
            cur_node = next_node
        self.head = prev_node
    def merge_sorted(self, llist) -> None: # Merges two sorted llists in one sorted llist 
        small_node = None
        cur_node_1 = self.head
        cur_node_2 = llist.head
        if not cur_node_1 :
            raise ValueError ('Initial list is empty')
        if not cur_node_2 :
            raise ValueError ('Given list is empty')
        
        if cur_node_1.data > cur_node_2.data :
            small_node = cur_node_2
            cur_node_2 = cur_node_2.next
        else :
            small_node = cur_node_1
            cur_node_1 = cur_node_1.next
        new_head = small_node

        while cur_node_1 and cur_node_2 :
            if cur_node_1.data <= cur_node_2.data :
                small_node.next = cur_node_1
                small_node = small_node.next
                cur_node_1 = cur_node_1.next
            if cur_node_1.data > cur_node_2.data :
                small_node.next = cur_node_2
                small_node = small_node.next
                cur_node_2 = cur_node_2.next

        if not cur_node_1 :
            small_node.next = cur_node_2
        if not cur_node_2 :
            small_node.next = cur_node_1
        
        self.head = new_head
    def remove_duplicates(self) -> None: # Removes all duplicates from the llist
        data_values = dict()
        prev_node = None
        cur_node = self.head
        while cur_node :
            if not cur_node.data in data_values :
                data_values[cur_node.data] = 1
                prev_node = cur_node
                cur_node = cur_node.next
            else :
                prev_node.next = cur_node.next
                cur_node = cur_node.next
    def get_element(self, index:int) : # Returns element with particular index. Index can be negative
        if index >= 0 :
            cur_node = self.head
            count = 0
            while cur_node and count !=index :
                count += 1 
                cur_node = cur_node.next
            if not cur_node :
                raise ValueError ('Index is out of range: ' + str(index))
            return cur_node.data
        else :
            cur_node = self.head
            ind_nodes_before = self.head
            count = 0
            while cur_node :
                if count != index :
                    count -= 1
                    cur_node = cur_node.next
                else :
                    ind_nodes_before = ind_nodes_before.next
                    cur_node = cur_node.next
            if count != index :
                raise ValueError ('Index is out of range: ' + str(index))
            return ind_nodes_before.data
    def count_occurences(self, data) -> int : # Returns number of occurences of a particulal value in the llist
        count = 0
        cur_node = self.head
        while cur_node :
            if cur_node.data == data :
                count += 1 
            cur_node = cur_node.next
        return count
    '''
    def count_recursive(self, data) -> int : # Does the same as previous, but recursive way
        def count(node, data) :
            if not node :
                return 0
            if node.data == data :
                return 1 + count(node.next, data)
            return count(node.next, data)
        return count(self.head, data)
    '''
    def rotate(self, index) -> None: # Moves all the elements after index element to the end of the list
        target_node = self.head
        count = 0
        while target_node and count != index :
            count += 1
            target_node = target_node.next
        if not target_node :
            raise ValueError ('Index is out of range: ' + str(index))
        if not target_node.next :
            raise ValueError ('Index points to the last element in the llist, nothing to rotate!' + str(index))
        
        cur_node = target_node
        while cur_node.next : # Searching for the last element in the list
            cur_node = cur_node.next
        cur_node.next = self.head
        self.head = target_node.next
        target_node.next = None
    def move_tail_to_head(self) -> None:
        prev_node = None
        cur_node = self.head
        while cur_node.next :
            prev_node = cur_node
            cur_node = cur_node.next
        cur_node.next = self.head
        self.head = cur_node
        prev_node.next = None
    def sum_two_lists(self, llist):
        def get_int(llist) :
            num = 0
            tens = 1
            cur_node = llist.head
            while cur_node :
                num += cur_node.data * tens
                cur_node = cur_node.next
                tens *= 10
            return num
        return get_int(self) + get_int(llist)



# 3 6 5 
#   4 2 
# ------
#  
llist1 = LinkedList()
llist1.append(5)
llist1.append(6)
llist1.append(3)

llist2 = LinkedList()
llist2.append(8)
llist2.append(4)
llist2.append(2)

print(365 + 248)
print(llist1.sum_two_lists(llist2))


