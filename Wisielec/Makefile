all:
	$(CC) -Wall serwer.c -O2 -std=c11 -lpthread -o serwer
	$(CC) -Wall client.c -O2 -std=c11 -lpthread -o client

clean:
	$(RM) -rf serwer
	$(RM) -rf client