/*
 * directmapped.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "makenum.c"

void directmapped();

int main(int argc, char *argv[])
{
    directmapped();
}

void directmapped()
{
    // declaring variables
    int64_t tags[512];
    char buffer[16];
    int64_t line, map, tag, mask;
    int hits, total, i;

    // assigning variables
    hits = 0;
    total = 0;
    mask = 0x37;
    i = 0;

    // sets all tags to 0
    for (i; i < 512; i++) tags[i] = 0;

    while(fgets(buffer, 16, stdin)) {

        line = makenum(buffer);
        tag = line >> 15;
        map = (line >> 6) & mask;

        if (tags[map] == tag) hits ++; // hit case
        else tags[map] = tag; // miss case

        total++;
    }

    // prints results
    double hitratio = 100 * (double)hits/(double)total;
    printf("Direct Mapped Simulation\n");
    printf("    hits = %d\n", hits);
    printf("    misses = %d\n",total-hits);
    printf("    hit rate = %f%\n", hitratio);
}
