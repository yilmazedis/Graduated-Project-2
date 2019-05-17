#include <stdio.h> 
#include "myStack.h"

int main() 
{ 
    struct StackNode* root = NULL; 
  
    push(&root, 10); 
    push(&root, 20); 
    push(&root, 30); 
  
    printf("%d popped from stack\n", pop(&root)); 
  
    printf("Top element is %d\n", peek(root)); 
  
    return 0; 
} 