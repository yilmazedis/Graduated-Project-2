all: exe1 exe2

exe1:
	gcc -o server server.c myStack.c -lpthread -g -lm

exe2:
	gcc -o client client.c -lpthread -g -lm

clean:
	rm server
	rm client
	rm -rf *~
