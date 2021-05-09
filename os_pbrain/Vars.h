#ifndef VARS_H_
#define VARS_H_
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

struct PCB
{
    struct PCB *Next_PCB ;
 	int PID ;
    short int PC, PRegs[4];
    int RRegs[4];
 	int IC ; //number of instructions before preemption (i.e., time slice)
 	char PSW[2] ; // Process status word
 	int ACC ; // accumulator
 	int BaseReg, LimitReg ; // minimum and maximum memory location
    int Total_Pages ;
 	/* Note: You cannot store the process' memory in PCB */
};

struct PCB *RQ, *tmp, *RQT, *Current ;

/*These are variables representing the VM itself*/

char IR[6] ;
short int PC ;

short int PRegs[4] ;
short int RRegs[4] ;

int BaseRegister, LimitRegister ;

int ACC ;
char PSW[2] ;
char memory [100][6]  ; 	//this is the program memory for all programs
short int opcode ;

struct Program
{ int Last ;
  int Num_Lines ;
  int  Data_Pages ;
  int  Total_Pages;
  char temp_mem[100][6] ;
  struct PCB *New_PCB ;
} ;

int Page_Table[10][5] ;
struct PPT
 { int LP ;
   int PP[10] ;
   char valid[10] ;
 } ;
#endif
