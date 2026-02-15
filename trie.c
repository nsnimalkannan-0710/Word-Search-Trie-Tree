#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct PositionNode
{
    int pos;
    struct PositionNode* next;
} PositionNode;

typedef struct node
{
    struct node* child[26];
    PositionNode* positions;
} sn;

sn* create()
{
    sn* nn = (sn*)malloc(sizeof(sn));
    nn->positions = NULL;
    for (int i = 0; i < 26; i++)
    {
        nn->child[i] = NULL;
    }
    return nn;
}

void insert(sn* root, const char word[], int pos)
{
    sn* curr = root;
    int i = 0;

    while (word[i])
    {
        if (!isalpha(word[i]))
        {
            i++;
            continue;
        }
        int index = tolower(word[i]) - 'a';
        if (!curr->child[index])
        {
            curr->child[index] = create();
        }
        curr = curr->child[index];

        PositionNode* new_node = (PositionNode*)malloc(sizeof(PositionNode));
        new_node->pos = pos;
        new_node->next = curr->positions;
        curr->positions = new_node;

        i++;
    }
}
int results[1000];
int* search(sn* root, char word[])
{
    sn* curr = root;
    int i = 0;
    int idx = 0;

    while (word[i])
    {
        if (!isalpha(word[i]))
        {
            i++;
            continue;
        }
        int index = tolower(word[i]) - 'a';
        
        if (!curr->child[index])
            return NULL;
        
        curr = curr->child[index];
        i++;
    }

    PositionNode* pos = curr->positions;
    while (pos)
    {
        results[idx++] = pos->pos;
        pos = pos->next;
    }
    results[idx] = -1;
    return results;
}
