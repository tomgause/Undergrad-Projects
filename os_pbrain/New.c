#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "Vars.h"

void Scrub_Memory(int) ;
void Print_Page_Table(int) ;
void Print_Frames() ;
int Find_Frame() ;
struct PCB *Admit_Program() ;
struct Program *New_Allocation ;
void Allocate_Pages(struct Program *) ;
int NAF = 10 ;
int Free_Frames[10]= {1,1,1,1,1,1,1,1,1,1} ;
int fp ;

int On_Disk[10] = {3,3,3,5,5,3,3,3,5,5} ;
int disk_index = 0 ;
char temp_memory[21] [6] ;
char input[7] ;
int num_requested ;
//struct PPT SPT[10] ;

int i, j, k ;

struct PCB *Admit_Program()
{
    static int First = 1 ;
    static int PID = 0 ;
    int Num_Lines ;
    if(First)
    {First = 0 ;
     for(i = 0 ; i < 10 ; i++)
    	for(j = 0 ; j < 5 ; j++)
    		Page_Table[i][j] = -1 ;
    }
    if(disk_index >= 10)
    {
     return(NULL) ;
    }

    num_requested = On_Disk[disk_index] ;
    printf("Number of Pages Requested is %d\n", num_requested) ;
    printf("There are %d pages left\n", NAF) ;
    if (num_requested > NAF)
    {printf("NOT ENOUGH PAGES\n") ;
    return(NULL) ;
    }
    New_Allocation = (struct Program *) malloc(sizeof(struct Program)) ;
    New_Allocation->New_PCB = (struct PCB *) malloc(sizeof(struct PCB)) ;
    New_Allocation->New_PCB->PID = PID++ ;
    New_Allocation->New_PCB->PC = 0 ;
    New_Allocation->New_PCB->ACC = 0 ;
    New_Allocation->New_PCB->PRegs[0] = 0 ;
    New_Allocation->New_PCB->PRegs[1] = 0 ;
    New_Allocation->New_PCB->PRegs[2] = 0 ;
    New_Allocation->New_PCB->PRegs[3] = 0 ;
    New_Allocation->New_PCB->RRegs[0] = 0 ;
    New_Allocation->New_PCB->RRegs[1] = 0 ;
    New_Allocation->New_PCB->RRegs[2] = 0 ;
    New_Allocation->New_PCB->RRegs[3] = 0 ;
    New_Allocation->New_PCB->Next_PCB = NULL ;

    New_Allocation->Num_Lines = 21 ;

    if (num_requested == 5)
    {
    fp = open("Fib.PB", O_RDONLY) ;
    New_Allocation->Data_Pages = 2 ;
    New_Allocation->Total_Pages = 5 ;
    New_Allocation->New_PCB->Total_Pages = 5 ;

    }

    else
    {
     fp = open("LittleFib.PB", O_RDONLY) ;
     printf("Opened Little FIB with %d\n", fp) ;
     New_Allocation->Data_Pages = 0 ;
     New_Allocation->Total_Pages = 3 ;
     New_Allocation->New_PCB->Total_Pages = 3 ;
    }

    Num_Lines = 21 ;
    for (i= 0; i < Num_Lines ; i++)
    {
       	 k = read(fp, input, 7) ;
     for(j = 0 ; j < 6 ; j++)
      {
       New_Allocation->temp_mem[i][j] = input[j] ;
      }

    }
    disk_index++ ;
    Allocate_Pages(New_Allocation) ;
    return(New_Allocation->New_PCB) ;
}


void Allocate_Pages(struct Program *NP)
{//see how many pages needed

   int i, j, k, m ;
   int PID ;
   int Frame ;
   double code_pages_double;
   int code_pages;
   int num_data, num_needed ;
   PID = NP->New_PCB->PID ;
   num_needed = NP->Total_Pages ;
   code_pages_double = ceil((double)(NP->Num_Lines / 10.0)) ;
   code_pages = code_pages_double;

   for (i = 0 ; i < code_pages ; i++)
	{Frame = Find_Frame() ;
	 printf("Allocating Frame %d\n", Frame) ;
	 NAF-- ;
	 Page_Table[PID][i] = Frame ;
	 m=0;
	 for(j = i * 10 ; j < i*10 + 10 ; j++)
		{
		for(k = 0; k < 6 ; k++)
			{
			 memory[Frame * 10 + m] [k] = NP->temp_mem[j][k] ;
			}
		m++ ;
		}
	}
   num_data = num_needed - code_pages ;
   for(i = 0; i < num_data ; i++)
	{
	 Frame = Find_Frame() ;
	 printf("Allocating Frame %d\n", Frame) ;
	 Page_Table[PID][code_pages + i] = Frame;
	 NAF-- ;
	}

}

void Print_Page_Table(int PID)
	{ int i ;
	  for(i = 0 ; i < 5 ; i++)
		printf("Page table %d %d is %d\n", PID, i, Page_Table[PID][i]) ;
 	}

void Free_Pages(struct PCB *Current)
	{ int i, j ;
	  for(i = 0 ; i < Current->Total_Pages ; i++)
		{Free_Frames[Page_Table[Current->PID][i]] = 1 ;
		 //Scrub_Memory(Page_Table[Current->PID][i]) ;
		 Page_Table[Current->PID][i] = -1 ;
		 NAF++ ;
		}
	}

void Print_Frames()
{ int i ;
  for(i = 0; i < 10 ; i++)
	printf("Frame %d is %d\n", i, Free_Frames[i]) ;
}


 int Find_Frame()
 { int i ;
   for(i = 0; i < 10 ; i++)
	{if(Free_Frames[i] == 1)
		{Free_Frames[i] = 0 ;
		 return(i) ;
		}
 	}
   return(-1) ;
 }

 void Scrub_Memory(int Physical_Page)
  {}
