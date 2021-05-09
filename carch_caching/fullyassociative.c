/*
 * fullyassociative.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "makenum.c"

void fullyassociative();

int main(int argc, char *argv[])
{
    fullyassociative();
}

void fullyassociative()
{
    //declaring variables
    int64_t tags[512];
    char buffer[16];
    int64_t line, tag;
    int i, j, hits, total;

    // assigning variables
    hits = 0;
    total = 0;
    i = 0;
    j = 0;

    // sets all tags to 0
    for (i; i < 512; i++) tags[i] = 0;

    while(fgets(buffer, 16, stdin)) {

        line = makenum(buffer);
        tag = line >> 6;

        for (i = 0; i < 512; i++) {
            if (tags[i] == tag) { // hit case
                hits++;
                if (i > 0) for (j = i; j > 0; j--) tags[j] = tags[j-1];
                tags[0] = tag;
                break;
            } if (i == 511) { // miss case
                for (j = 511; j > 0; j--) tags[j] = tags[j-1];
                tags[0] = tag;
                break;
            }
        }

        total++;
    }

    // prints results
    double hitratio = 100 * (double)hits/(double)total;
    printf("Fully Associative Simulation\n");
    printf("    hits = %d\n", hits);
    printf("    misses = %d\n",total-hits);
    printf("    hit rate = %f%\n", hitratio);
}
