// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
// my own headers
#include<stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h> // for strcasecmp

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int num;
int counter; // so i can use it in the size function
// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    num = hash(word);
    node *cursor = table[num];
    // we need to go through each node in that linked list to check if that is the word
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function (left for later)
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);
        num = hash(word); // hash function will deal with sorting the words
        n->next = table[num];
        table[num] = n;
        counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{

    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i]; // for each array
        while (cursor != NULL)
        {
            node *tmp = cursor; // a tmp to free
            cursor = cursor->next;
            free(tmp);
        }
        // the program stops when there are no more arrays either cursors
        if (i == N - 1 && cursor == NULL)
        {
            return true;
        }
    }
    return false;
}
