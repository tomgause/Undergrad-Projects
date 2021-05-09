/*
 * setassociative.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "makenum.c"

void setassociative();

int main(int argc, char *argv[])
{
    setassociative();
}

void setassociative()
{
    // declare variables
    int64_t sets[64][8];
    char buffer[16];
    int64_t line, map, tag, mask;
    int i, j, hits, total;

    // assign variables
    mask = 0x3a;
    hits = 0;
    total = 0;
    i = 0;
    j = 0;

    // sets all tags to 0
    for (i; i < 64; i++) {
        for (j; j < 8; j++) sets[i][j] = 0;
    }

    while(fgets(buffer, 16, stdin)) {

        line = makenum(buffer);
        map = (line >> 6) & mask;
        tag = line >> 12;

        for (i = 0; i < 8; i++) {
            if (sets[map][i] == tag) { // hit case
                hits++;
                if (i > 0) for (j = i; j > 0; j--) sets[map][j] = sets[map][j-1];
                sets[map][0] = tag;
                break;
            }
            if (i == 7) { // miss case
                for (j = 7; j > 0; j--) sets[map][j] = sets[map][j-1];
                sets[map][0] = tag;
                break;
            }
        }

        total++;
    }

    // prints results
    double hitratio = 100 * (double)hits/(double)total;
    printf("Set Mapped Simulation\n");
    printf("    hits = %d\n", hits);
    printf("    misses = %d\n",total-hits);
    printf("    hit rate = %f%\n", hitratio);
}
