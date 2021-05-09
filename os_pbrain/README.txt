I've included the New.c and Opcodes.c files in main1.c (this time
using #include rather than copy paste).

Compile:		gcc main1.c -o main
Run:		./main

Although you included a Scrub_Memory function, I chose not to 
implement it as you did not specify whether or not to in the 
project description. Obviously this leads to memory leaks.