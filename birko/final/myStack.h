//https://www.geeksforgeeks.org/stack-data-structure-introduction-program/


// A structure to represent a stack 
struct StackNode 
{ 
    int data; 
    struct StackNode* next; 
};

struct StackNode* newNode(int data);
int isEmpty(struct StackNode *root);
void push(struct StackNode** root, int data);
int pop(struct StackNode** root);
int peek(struct StackNode* root);