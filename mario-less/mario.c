#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //asking for the height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n > 8 || n < 1);

    //making the pyramid
    //i for rows and j for columns
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i + j < n - 1)

           printf(" ");

           else

           printf("#");
    }

    printf("\n");
    }

}
