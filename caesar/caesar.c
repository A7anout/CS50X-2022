#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
// my custom functions
bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Make sure every character in argv[1] is a digit (main)
    bool check = only_digits(argv[1]);
    if (check == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Convert argv[1] from a `string` to an `int`
    int n = atoi(argv[1]);
    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    // For each character in the plaintext rotate the character if it's a letter
    char ciphertext;
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        ciphertext = rotate(plaintext[i], n);
        printf("%c", ciphertext);
    }
    printf("\n");
}

// Make sure every character in argv[1] is a digit (function)
bool only_digits(string s)
{
    bool check = true;
    for (int i = 0; i < strlen(s); i++)
    {
        if (! isdigit(s[i]))
        {
            check = false;
        }
    }
    return check;
}

char rotate(char c, int n)
{
    if (isupper(c))
    {
        c = (c - 65 + n) % 26 + 65;
    }
    else if (islower(c))
    {
        c = (c - 97 + n) % 26 + 97;
    }
    return c;
}