#include <unistd.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <poll.h>
#include <errno.h>
#include <fcntl.h>

#define MYPORT "9000"

int getAddress(const char *node, const char *service, const struct addrinfo *hints, struct addrinfo **res){
	int ret;
	
	if((ret = getaddrinfo(node, service, hints, res))!=0){
		fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(ret));
		exit(EXIT_FAILURE);
	}
	return ret;

}

int getSocket(struct addrinfo *res){
	int ret;
	
	if((ret = socket(res->ai_family, res->ai_socktype, res->ai_protocol))<0){
		fprintf(stderr, "socket error: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
	return ret;
}

int getBind(int sockfd, struct addrinfo *res){
	int ret;

	if((ret = bind(sockfd, res->ai_addr, res->ai_addrlen))<0){
		fprintf(stderr, "bind error: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
	return ret;
}

int getListen(int sockfd, int backlog){
	int ret;

	if((ret = listen(sockfd, backlog))<0){
		fprintf(stderr, "listen error: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
	return ret;
}

int getAccept(int sockfd, struct sockaddr *addr, socklen_t *addrlen){
	int ret;

	if((ret = accept(sockfd, addr, addrlen))<0){
		fprintf(stderr, "accept error: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
	return ret;
}


int sendAll(int sockfd, const void *msg, int *len, int flag){
	int ret;
	int sent = 0;
	int left = *len;

	while(sent < *len) {
		ret = send(sockfd, msg+sent, left, 0);
		if(ret<0){
			fprintf(stderr, "send error: %s\n", strerror(errno));
			exit(EXIT_FAILURE);
		}
		sent += ret;
		left -= ret;
	}

	*len = sent;

	return ret;
}
int receive(int sockfd, void *buf, int len, int flags){
	int ret;

	if((ret = recv(sockfd, buf, len, flags))<0){
		fprintf(stderr, "receive error: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
	return ret;
}

void add_to_pfds(struct pollfd *pfds[], int newfd, int *fd_count, int *fd_size)
{
    // If we don't have room, add more space in the pfds array
    if (*fd_count == *fd_size) {
        *fd_size *= 2; // Double it

        *pfds = realloc(*pfds, sizeof(**pfds) * (*fd_size));
    }

    (*pfds)[*fd_count].fd = newfd;
    (*pfds)[*fd_count].events = POLLIN; // Check ready-to-read

    (*fd_count)++;
}

void del_from_pfds(struct pollfd pfds[], int i, int *fd_count)
{
    // Copy the one from the end over this one
    pfds[i] = pfds[*fd_count-1];

    (*fd_count)--;
}


void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int get_listener_socket(void)
{
    int listener;     // Listening socket descriptor
    int yes=1;        // For setsockopt() SO_REUSEADDR, below
    int rv;

    struct addrinfo hints, *ai, *p;

    // Get us a socket and bind it
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;
    if ((rv = getaddrinfo(NULL, MYPORT, &hints, &ai)) != 0) {
        fprintf(stderr, "selectserver: %s\n", gai_strerror(rv));
        exit(1);
    }
    
    for(p = ai; p != NULL; p = p->ai_next) {
        listener = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (listener < 0) { 
            continue;
        }
        
        // Lose the pesky "address already in use" error message
        setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));

        if (bind(listener, p->ai_addr, p->ai_addrlen) < 0) {
            close(listener);
            continue;
        }

        break;
    }

    freeaddrinfo(ai); // All done with this

    // If we got here, it means we didn't get bound
    if (p == NULL) {
        return -1;
    }
    // Listen
    if (listen(listener, 10) == -1) {
        return -1;
    }

    return listener;
}
