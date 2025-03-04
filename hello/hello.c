#include <stdio.h>
#include <cs50.h>
//asking for username
int main(void)
{
    string name = get_string("What's your name?");
    printf("hello, %s\n", name);
}