/*
 * makenum.c
 */

#include <stdint.h>

// converts a buffer[16] in hex into an int64_t
int64_t makenum(char buffer[]) {
    int64_t x = 0;
    int i = 0;
    while (i < 16) {
        if (buffer[i] == '0') {
            x += 0;
        } else if (buffer[i] == '1') {
            x += 1;
        } else if (buffer[i] == '2') {
            x += 2;
        } else if (buffer[i] == '3') {
            x += 3;
        } else if (buffer[i] == '4') {
            x += 4;
        } else if (buffer[i] == '5') {
            x += 5;
        } else if (buffer[i] == '6') {
            x += 6;
        } else if (buffer[i] == '7') {
            x += 7;
        } else if (buffer[i] == '8') {
            x += 8;
        } else if (buffer[i] == '9') {
            x += 9;
        } else if (buffer[i] == 'a') {
            x += 10;
        } else if (buffer[i] == 'b') {
            x += 11;
        } else if (buffer[i] == 'c') {
            x += 12;
        } else if (buffer[i] == 'd') {
            x += 13;
        } else if (buffer[i] == 'e') {
            x += 14;
        } else if (buffer[i] == 'f') {
            x += 15;
        } else break;
        x = x << 4;
        i++;
    }
    x = x >> 4;
    return x;
}
