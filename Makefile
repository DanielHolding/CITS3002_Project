
# A Makefile to build our 'calcmarks' project

PROJECT =  rakeserver
HEADERS =  $(PROJECT).h
OBJ     =  rakeserver.o  writeFile.o network.o


C11     =  cc -std=c11
CFLAGS  =  -Wall -Werror 


$(PROJECT) : $(OBJ)
	$(C11) $(CFLAGS) -o $(PROJECT) $(OBJ) -lm


%.o : %.c $(HEADERS)
	$(C11) $(CFLAGS) -c $<

clean:
	rm -f $(PROJECT) $(OBJ)
