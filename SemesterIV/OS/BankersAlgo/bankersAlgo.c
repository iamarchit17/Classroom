/*
Archit Agrawal
202051213
*/

#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

#define MAXN 10  
#define MAXM 10 
#define n 3 
#define m 1

//int n = 3, m = 3;
int ProcCurr[n][m];     /* n threads(processes), m resources    */
int Available[m];        // resources that are not allocated to any process
int Max[n][m] = { {10,10,10},{10,10,10},{10,10,10} };  //maximum demand of processes n for resource m 
int Allocation[n][m] = { {1,2,3},{3,2,1},{1,1,1} }; //Allocation[n][m] = # resources m allocated to processes n
int Need[n][m];    //resources m needed by processes n apart from already allocated resoures
//Need[i][j] = Max[i][j] - Allocated[i][j]          

int counti = 0;     
int countj = 0;
int threadsi = n;
int threadsj = n;

void *inc_count(void *r);
void *watch_count(void *r);

pthread_mutex_t mutex; 
pthread_cond_t count_threshold_cv;

int main(){
	
	/*
	for(int p = 0; p < n; p++){
		for(int q = 0; q < m; q++){
			printf("%d ", Allocation[p][q]);
		}
		printf("\n");
	}
	*/

	//int n; //number of processes
	//int m; //number of resources
	//printf("Enter n, the number of processes and m, the number of resources : ");
	//scanf("%d%d, &n, &m);


	pthread_t ProcCurr[n][m]; /*id of thread*/
	pthread_attr_t attr;
	
	int  i, j;
	long r[n];
	for(int x = 0; x < n; x++) r[x] = x + 1;
	//long r1 = 1,r2 = 2,r3 = 3;

	if(pthread_mutex_init(&mutex, NULL) < 0){
		perror("Pthread_mutex_init error.");
		exit(1);    
	} else pthread_cond_init(&count_threshold_cv, NULL); //pthread_mutex_init(&mutex, NULL);

	pthread_attr_init(&attr); /*get default attributes*/
	
	for(int x = 0; x < n; x++){
		pthread_create(&ProcCurr[x][0], &attr, watch_count, (void *)r[x]);
	}
	
	//pthread_create(&ProcCurr[0][0], &attr, watch_count, (void *)r1);
	//pthread_create(&ProcCurr[1][0], &attr, inc_count, (void *)r2);
	//pthread_create(&ProcCurr[2][0], &attr, inc_count, (void *)r3);


    for(i = 0; i <= threadsi; i++){ 
        for(j = 0; j <= threadsj; j++){ 
            //pthread_join(ProcCurr[i][j],NULL); /*wait for thread to exit*/
            for(int k = 0; k < n; k++){
            	pthread_join(ProcCurr[k][0],NULL); 
            }
            //pthread_join(ProcCurr[0][0],NULL); 
            //pthread_join(ProcCurr[1][0],NULL);             
            //pthread_join(ProcCurr[2][0],NULL); 
        }
    }
    printf("Main: waited on %d, %d threads. Done.\n", threadsi, threadsj);

    pthread_attr_destroy(&attr);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&count_threshold_cv);
    pthread_exit(NULL);
    
}

void *inc_count(void *r){  
    /*processes are running, thread of process is initalize to something <= n,
     each threads request up to m resources,
      when all resources are commited then next thread will have to wait (mutex goes
      to resource from a thread letting other threads know not to this resource)
    */
    
    int i, j;
    //int n, m;
    
    long my_id = (long)r;

    for(i = 0; i < n; i++){
        for(j = 0; j < m; j++){
            Need[i][j] = Max[i][j] - Allocation[i][j];
            printf("Allocation = %d, Need = %d\n", Allocation[i][j], Need[i][j]);
        }
    
    	pthread_mutex_lock(&mutex);
    	if(counti == MAXN && countj == MAXM){
        	pthread_cond_signal(&count_threshold_cv);
        	printf("inc_count: thread %ld, Need = %d. Threshold reached.\n",my_id, Need[i][j]);
    	}
    
    	printf("inc_count: thread %ld, Need = %d. Unlocking mutex.\n", my_id, Need[i][j]);
    	pthread_mutex_unlock(&mutex);
    	sleep(1);
    	watch_count(r);
    }
  	
  	pthread_exit(NULL);
  	watch_count(r);
}


void *watch_count(void *r){
    
    long my_id = (long)r;
    //int n, m;

    printf("Start watch_count: thread %ld\n", my_id);

    while(counti < MAXN && countj <MAXM){
    	pthread_mutex_lock(&mutex);
   		Available[countj] = Max[counti][countj] - Allocation[counti][countj];
   		counti++; countj++;
   		printf("Available = %d\n", Available[countj]);
   		pthread_cond_wait(&count_threshold_cv, &mutex);
   		printf("watch_count: thread %ld, available = %d. Conditional Signal Received.\n", my_id, Available[countj]);
   		countj++;
   		printf("watch_count: thread %ld, Need now = %d.\n", my_id, Need[counti][countj]);
  	}
  	pthread_mutex_unlock(&mutex);
  	pthread_exit(NULL);
}



