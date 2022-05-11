#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void writeFile(char* string, int filelength){
	FILE * fp;
	int fnlen = strcspn(string, "\n");
	printf("%i\n", fnlen);

	char* filename = malloc(fnlen+2);
	filename[fnlen] = '\0';

	strncpy(filename, string, fnlen);
       	string += fnlen+1;
	printf("%s\n", filename);	

//	printf("%s\n", string);	
	fp = fopen(filename, "w");

	if(fp != NULL){
		fputs(string, fp);
		fclose(fp);
	}
	
}
