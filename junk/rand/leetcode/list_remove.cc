#include <stdlib.h>
#include <iostream>

// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

ListNode* 
removeElements(ListNode* head, int val) 
{
    ListNode* prev = NULL;
    ListNode* next = NULL;
    ListNode* curr = head;
    
    // compute new head
    ListNode* newHead = head;
    while (newHead != NULL && newHead->val == val) {
        newHead = newHead->next;
    }
    
    // delete target nodes
    while (curr != NULL) {
        next = curr->next;
        
        if (curr->val == val) {
            
            if (prev != NULL) {
                prev->next = next;
            }
            
            // cleanup
            curr->next = NULL;
            delete curr;
            curr = NULL;
        } else {
            prev = curr;
        }
        
        curr = next;
     }
     
     return newHead;
}

void
printList(ListNode* root)
{
    ListNode* curr = root;
    while (curr != NULL) {
        std::cout << curr->val << " ";
        curr = curr->next;
    }
    std::cout << std::endl;
}

void
testCase1()
{
    ListNode* one = new ListNode(1);
    ListNode* two = new ListNode(2);
    ListNode* three = new ListNode(3);

    one->next = two;
    two->next = three;

    ListNode* newHead = removeElements(one, 2);
    printList(newHead);
}

void
testCase2()
{
    ListNode* one = new ListNode(1);
    ListNode* two = new ListNode(2);
    ListNode* three = new ListNode(2);
    ListNode* four = new ListNode(1);

    one->next = two;
    two->next = three;
    three->next = four;

    ListNode* newHead = removeElements(one, 2);
    printList(newHead);
}

int
main()
{
    testCase1();
    testCase2();
    return 0;
}
