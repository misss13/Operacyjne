#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h> /* socket() */
#include <netinet/in.h> /* struct sockaddr_in */
#include <arpa/inet.h>  /* inet_ntop() */
#include <unistd.h>     /* close() */
#include <string.h>
#include <time.h>
#include <errno.h>
#include <pthread.h>
#include <sys/types.h>
#include <signal.h>

/*
TODO:
 - uwierzytelnienie (+sukces -zle haslo)
 - kolejka graczy
 - co 5 min jesli 2<=graczy<10, graczy=10 od razu gra
 - wybor wybierajacego slowo losowanie lub z kolejki<- (odsylam @)
 - czekam na klienta 2s jak nie ma słowa to rezygnuje
 - sprawdzam slowo w slowniku DONE
*/

#define MIN_CLIENTS 2
#define MAX_CLIENTS 10
#define BUFFER_SZ 2048

static _Atomic unsigned int cli_count = 0;
static int uid = 10;

typedef struct {
  struct sockaddr_in addr; /* klient adres do usuniecia */
  int connfd;              /* deskryptor dla gniazda klienta */
  int uid;                 /* unikalny nr klienta */
  char name[32];           /* nick klienta */
} client_t;

client_t *clients[MAX_CLIENTS];

pthread_mutex_t clients_mutex = PTHREAD_MUTEX_INITIALIZER;

void print_client_addr(struct sockaddr_in addr){
  printf("%d.%d.%d.%d",
         addr.sin_addr.s_addr & 0xff,
         (addr.sin_addr.s_addr & 0xff00) >> 8,
         (addr.sin_addr.s_addr & 0xff0000) >> 16,
         (addr.sin_addr.s_addr & 0xff000000) >> 24);
}

/* znak kszksz usuwam */
void strip_newline(char *s){
  while (*s != '\0') {
    if (*s == '\r' || *s == '\n') {
      *s = '\0';
    }
    s++;
  }
}

void queue_add(client_t *cl){
  pthread_mutex_lock(&clients_mutex);
  for (int i = 0; i < MAX_CLIENTS; ++i) {
    if (!clients[i]) {
      clients[i] = cl;
      break;
    }
  }
  pthread_mutex_unlock(&clients_mutex);
}

/* usuwanie klienta z kolejki */
void queue_delete(int uid){
  pthread_mutex_lock(&clients_mutex);
  for (int i = 0; i < MAX_CLIENTS; ++i) {
    if (clients[i]) {
      if (clients[i]->uid == uid) {
        clients[i] = NULL;
        break;
      }
    }
  }
  pthread_mutex_unlock(&clients_mutex);
}

void send_message_all(char *s){
  pthread_mutex_lock(&clients_mutex);
  for (int i = 0; i <MAX_CLIENTS; ++i){
    if (clients[i]) {
      if (write(clients[i]->connfd, s, strlen(s)) < 0) {
        perror("blad zapisu do deskryptora");
        break;
      }
    }
  }
  pthread_mutex_unlock(&clients_mutex);
}
/*do jednego*/
void send_message(char *s, int uid){
  pthread_mutex_lock(&clients_mutex);
  for (int i = 0; i < MAX_CLIENTS; ++i) {
    if (clients[i]) {
      if (clients[i]->uid != uid) {
        if (write(clients[i]->connfd, s, strlen(s)) < 0) {
          perror("blad zapisu do deskryptora");
          break;
        }
      }
    }
  }
  pthread_mutex_unlock(&clients_mutex);
}

void *handle_client(void *arg){
    char buff_out[BUFFER_SZ];
    char buff_in[BUFFER_SZ / 2];
    int rlen;

    cli_count++;
    client_t *cli = (client_t *)arg;

    printf("<< zaakceptowano ");
    print_client_addr(cli->addr);
    printf(" przyznanie uid %d\n", cli->uid);

    sprintf(buff_out, "<< %s dolaczyl \r\n", cli->name);
    send_message_all(buff_out);


    /* Receive input from client */
    while ((rlen = read(cli->connfd, buff_in, sizeof(buff_in) - 1)) > 0) {
        buff_in[rlen] = '\0';
        buff_out[0] = '\0';
        strip_newline(buff_in);

        /* pozbywam sie pustego wejscia */
        if (!strlen(buff_in)) {
            continue;
        }

        /* opcja quit */
        if (buff_in[0] == '/') {
            char *command, *param;
            command = strtok(buff_in," ");
            if (!strcmp(command, "/quit")) {
                break;
            }
        } else {
            /* wyslij wiadomosc */
            snprintf(buff_out, sizeof(buff_out), "[%s] %s\r\n", cli->name, buff_in);
            send_message(buff_out, cli->uid);
        }
    }

    /* zamknij polaczenie */
    sprintf(buff_out, "<< %s odszedl\r\n", cli->name);
    send_message_all(buff_out);
    close(cli->connfd);

    /* usuniecie klienta z kolejki i jego watku */
    queue_delete(cli->uid);
    printf("<< odszedl ");
    print_client_addr(cli->addr);
    printf(" o uid %d\n", cli->uid);
    free(cli);
    cli_count--;
    pthread_detach(pthread_self());

    return NULL;
}

int main(int argc, char** argv) {
  pthread_t tid;
  /* Deskryptory dla gniazda nasluchujacego i polaczonego: */
  int listenfd, connfd;
  int retval; /* Wartosc zwracana przez funkcje. */

  /* Gniazdowe struktury adresowe (dla klienta i serwera): */
  struct sockaddr_in client_addr, server_addr;

  /* Rozmiar struktur w bajtach: */
  socklen_t client_addr_len, server_addr_len;

  /* Bufor wykorzystywany przez write() i read(): */
  char buff[256];

  /* Bufor dla adresu IP klienta w postaci kropkowo-dziesietnej: */
  char addr_buff[256];

  time_t rawtime;
  struct tm* timeinfo;

  /* Utworzenie gniazda dla protokolu TCP: */
  listenfd = socket(PF_INET, SOCK_STREAM, 0);
  if (listenfd == -1) {
    perror("socket()");
    exit(EXIT_FAILURE);
  }

  /* Wyzerowanie struktury adresowej serwera: */
  memset(&server_addr, 0, sizeof(server_addr));
  /* Domena komunikacyjna (rodzina protokolow): */
  server_addr.sin_family = AF_INET;
  /* Adres nieokreslony (ang. wildcard address): */
  server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  /* Na porcie */
  server_addr.sin_port = htons(8181);
  /* Rozmiar struktury adresowej serwera w bajtach: */
  server_addr_len = sizeof(server_addr);

  /* Powiazanie "nazwy" (adresu IP i numeru portu) z gniazdem: */
  if (bind(listenfd, (struct sockaddr*) &server_addr, server_addr_len) == -1) {
    perror("bind()");
    exit(EXIT_FAILURE);
  }

    /* Przeksztalcenie gniazda w gniazdo nasluchujace: */
    if (listen(listenfd, 2) == -1) {
        perror("listen()");
        exit(EXIT_FAILURE);
    }

    fprintf(stdout, "Server nasluchuje na polaczenie...\n");

    while(1){
      socklen_t clilen = sizeof(client_addr);
      connfd = accept(listenfd, (struct sockaddr*) &client_addr, &clilen);

      //max osiagniety
      if((cli_count + 1) == MAX_CLIENTS){
        printf("Max ilosc klientow\n polaczenie odrzucone: ");
        printf("\n");
        close(connfd);
        continue;
      }

      client_t *cli = (client_t *) malloc(sizeof(client_t));
      cli->addr = client_addr;
      cli->connfd = connfd;
      cli->uid = uid++;
      sprintf(cli->name, "%d", cli->uid);

      queue_add(cli);
      pthread_create(&tid, NULL, &handle_client, (void*)cli);
      sleep(1);
    }
    exit(EXIT_SUCCESS);
}
