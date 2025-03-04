#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    // open memory card
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 2;
    }
    // repeat until the end of the card
    typedef uint8_t BYTE;
    BYTE buffer[512];
    int i = 0;
    char *filename = malloc(8);
    FILE *img = NULL;
    while (fread(buffer, 1, 512, file) == 512)
    {
        // is this the start of a jpeg?
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (i == 0)
            {
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
            }
            else if (i > 0)
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
            }
            i++;
        }
        // keep writing to the jpeg
        else if (img != NULL)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    // dont leak any memory
    free(filename);
    // dont keep any file opened
    fclose(file);
    fclose(img);
}