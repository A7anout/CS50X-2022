#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// defining my functions
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // asking the user for the text
    string text = get_string("Text: ");
    // getting letters , words and sentecnes
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    // setting the variables
    float L = letters / (float) words * 100;
    float S = sentences / (float) words * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int X = round(index);
    // printing the results
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", X);
    }

}

//counting the letters
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            letters++;
        }
        else if (text[i] >= 'a' && text[i] <= 'z')
        {
            letters++;
        }
    }
    return letters;
}

// counting the words (words = spaces +1)
int count_words(string text)
{
    int spaces = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            spaces++;
        }
    }
    int words = spaces + 1;
    return words;
}

// counting the sentences that end with '.' or '?' or '!'
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }
    return sentences;
}