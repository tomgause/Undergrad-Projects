#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "Vars.h"

#include "Opcodes.c"
#include "New.c"

extern void Print_Page_Table(int) ;
struct PCB *New_Program ;
extern void Free_Pages(struct PCB *) ;
extern void printMEM(int) ;
extern struct PCB *Admit_Program() ;
void RestoreState(struct PCB *) ;
int  ExecuteProc(struct PCB *) ;
void DeletePCB(struct PCB *) ;
void MvToTail(struct PCB *, struct PCB **) ;
void SaveState(struct PCB **) ;
void PrintQ(struct PCB*) ;
struct PCB* GetNextProcess(struct PCB **) ;
void Place_On_Queue(struct PCB *) ;

extern int ExecuteProc(struct PCB *) ;

int Max_Line = 0 ;

/*These are variables representing the VM itself*/

int program_line = 0 ; // For loading program into Memory

/*These variables are associated with the implementation of the VM*/
int fp ;
int i ;
int j, k ;
char input_line [7] ;

int main(int argc, char *argv[])
{	RQ = NULL ; RQT = NULL ; /* Changed how PCB allocated and placed on RQ */

	while(1)
	{	New_Program = Admit_Program() ;
		if(New_Program == NULL)
			break ;
		printf("Putting PID %d on the RQ\n", New_Program->PID) ;
		Place_On_Queue(New_Program) ;
		sleep(0) ;
	}

	while(1)
    {
		Current = GetNextProcess(&RQ); //Standard and already coded
	        RestoreState(Current);
		if(Current->PID == 0)
            		Current->IC =  40 ;
		else if(Current->PID == 1)
            		Current->IC =  4 ;
		else if(Current->PID == 2)
            		Current->IC =  30 ;
		else
			Current->IC = 25 ;
		Print_Page_Table(Current->PID) ;
    	//Current->IC = (rand() % 200) + 5;
    	printf("CURRENT PID %d, IC %d\n", Current->PID, Current->IC);
    	int Completed = ExecuteProc(Current);

		if (Completed)
        {
              printf("Process %d has completed its exeuction and will be terminated\n",Current->PID);
              printf("Removing PID %d\n", Current->PID);
            Free_Pages(Current) ;
              DeletePCB(Current); //Calls DeletePCB, expanded upon below
            //printMEM(100) ;
            sleep(0) ;
    		while(1)
            {
                New_Program = Admit_Program() ;
                    	 if(New_Program == NULL)
                            	break ;
                    	 printf("Putting PID %d on the RQ\n", New_Program->PID) ;
    			         printf("PID is %d PC is %d\n", New_Program->PID, New_Program->PC) ;
                    	 Place_On_Queue(New_Program) ;
                sleep(0);
    		}
        } else {
            SaveState(&Current);
            printf("Moving PID %d to TAIL\n", Current->PID);
            MvToTail(Current, &RQT);
            printf("RQT is %d\n", RQT->PID);
            if(RQ == NULL)
                    	RQ = RQT;
        }
        PrintQ(RQ); //Prints the state of the ready queue
        //sleep(1); //Sleep diagnostic
        if (RQ == NULL)
        	break;
    }
    printf("All processes complete. Printing memory...\n");
	printMEM(100);
    printf("Main successfully executed.\n");
}

/*	This function returns the PCB at the head of the RQ and updates
	RQ to point to the next PCB in the list
*/

struct PCB *GetNextProcess(struct PCB **RQ) // Gets the next process in the Ready Queue
{
    struct PCB *removedPointer;
    struct PCB *newHead;
    removedPointer = *RQ;
    newHead = (*RQ)->Next_PCB;
    *RQ = newHead;
    removedPointer->Next_PCB = NULL ;
    return (removedPointer) ;
}

/*	Deletes the PCB (using free) */

void DeletePCB(struct PCB *Current) // Deletes the PCB once it has completed its execution
{
    free(Current);
}

void MvToTail (struct PCB *Current, struct PCB **RQT) // Moves the PCB to tail of the ready queue
{
    (*RQT)->Next_PCB = Current;
    (*RQT)->Next_PCB->Next_PCB = NULL;
    (*RQT) = (*RQT)->Next_PCB;
}


/*	Prints out the elements of a linked list */

void PrintQ(struct PCB *Head) // Prints the contents of the ready queue, all remaining programs
{
    if (Head != NULL)
    {
        printf("%d > ", Head->PID);
        Head = Head->Next_PCB;
        PrintQ(Head);
    } else {
        printf("\n");
    }
}

/*	This function restores the state of the process that is set to begin its
	execution
*/

void RestoreState(struct PCB *NextProc) //
{
    PC = NextProc->PC;
    ACC = NextProc->ACC;

    for (i = 0; i < 2; i++) {
        PSW[i] = NextProc->PSW[i];
    }

    for (i = 0; i < 4; i++) {
        RRegs[i] = NextProc->RRegs[i];
        PRegs[i] = NextProc->PRegs[i];
    }
}

void SaveState(struct PCB **PrevProc) // Saves the current state
{
    (*PrevProc)->ACC = ACC;
    (*PrevProc)->PC = PC;

    for (i = 0; i < 2; i++) {
        (*PrevProc)->PSW[i] = PSW[i];
    }

    for (i = 0; i < 4; i++) {
        (*PrevProc)->RRegs[i] = RRegs[i];
        (*PrevProc)->PRegs[i] = PRegs[i];
    }
}

// takes PCB returned by Admit_Program() and places at tail of RQ
void Place_On_Queue(struct PCB *New)
{
    if (RQ == NULL) {
        RQ = New;
        RQ->Next_PCB = NULL;
        RQT = RQ;
    } else {
        RQT->Next_PCB = New;
        RQT->Next_PCB->Next_PCB = NULL;
        RQT = RQT->Next_PCB;
    }
}
