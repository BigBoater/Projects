# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

l1 = [2,4,3]
l2 = [0]

def reverse(string):
    return string[::-1]

def solution(l1, l2):

    r_l1 = ""
    r_l2 = ""
    for i in l1:
        r_l1 = r_l1+str(i)
    for i in l2:
        r_l2 = r_l2+str(i)
    r_l1 = reverse(r_l1)
    r_l2 = reverse(r_l2)

    output = int(r_l1) + int(r_l2)

    print(output)
