
int getAddress(const char *node, const char *service, const struct addrinfo *hints, struct addrinfo **res);

int getSocket(struct addrinfo *res);

int getBind(int sockfd, struct addrinfo *res);
int getListen(int sockfd, int backlog);

int getAccept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

int sendAll(int sockfd, const void *msg, int *len, int flag);

int receive(int sockfd, void *buf, int len, int flags);

void add_to_pfds(struct pollfd *pfds[], int newfd, int *fd_count, int *fd_size);

void del_from_pfds(struct pollfd pfds[], int i, int *fd_count);

void *get_in_addr(struct sockaddr *sa);

int get_listener_socket(void);

void writeFile(char* string, int filelength);

