#include <stdio.h>
#include <unistd.h> 
#include <stdlib.h>
#include <errno.h>
#include <string.h>

int main (int argc, char *argv[]) {
    const char* COMMAND_PATH = "/srv/ctf_go/check_challenge_corrected.py";
    char* COMMAND_NAME = "check_challenge_corrected.py";
    // have to do this to keep the suid
    setregid(getegid(), getegid());
    setreuid(geteuid(), geteuid());
    int arrayLength = argc+1;
    char** arguments = (char**)malloc( sizeof(char*) * (arrayLength));
    char* null = (char*)0;
    int i;
    arguments[0] = COMMAND_NAME;
    for(i=1 ; i<arrayLength-1 ; ++i){
        arguments[i] = argv[i];
    }
    arguments[arrayLength-1] = null;
    int ret = execv(COMMAND_PATH, arguments);
    free(arguments);
    if(ret != 0){
        fprintf(stderr, "%s\n", strerror(errno));
    }
    return ret;
}
