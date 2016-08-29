#include <stdio.h>
#include <unistd.h> 
#include <stdlib.h>
#include <errno.h>
#include <string.h>

int main (int argc, char *argv[]) {
    const char* PATH = "/srv/ctf_go/challs/";
    char final_path[512];
    snprintf(final_path, sizeof final_path, "%s%s", PATH, "CHALLENGE");
    // have to do this to keep the suid
    setregid(getegid(), getegid());
    setreuid(geteuid(), geteuid());
    int arrayLength = (4 + argc - 1);
    printf("%d\n", arrayLength);
    char** arguments = (char**)malloc( sizeof(char*) * arrayLength);
    char* user = "--user=THE_USER";
    char* null = (char*)0;
    int i;
    arguments[0] = "sudo";
    arguments[1] = user;
    arguments[2] = final_path;
    for(i=3 ; i<arrayLength-1 ; ++i){ // 1 to n-1
        printf("%d\n", i);
        arguments[i] = argv[i-2];
    }
    arguments[arrayLength-1] = null;
    for(i=0 ; i<arrayLength-1 ; ++i){
        printf("%d\n", i);
        printf("%s\n", arguments[i]);
    }
    printf("Done\n");
    int ret = execv("/usr/bin/sudo", arguments);
    printf("%s\n", strerror(errno));
    free(arguments);
    return ret;
}
