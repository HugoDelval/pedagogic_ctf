#include <stdio.h>
#include <unistd.h> 

int main (int argc, char *argv[]) {
    char* path = "/srv/ctf_interne/challs/";
    char final_cmd[512];
    snprintf(final_cmd, sizeof final_cmd, "%s%s", path, "CHALLENGE");
    setreuid(geteuid(), geteuid());
    if(argc == 1)
	    return execl(final_cmd, final_cmd, (char*)0);
	else if(argc == 2)
		return execl(final_cmd, final_cmd, argv[1], (char*)0);
	else if(argc == 3)
		return execl(final_cmd, final_cmd, argv[1], argv[2], (char*)0);
	else if(argc == 4)
		return execl(final_cmd, final_cmd, argv[1], argv[2], argv[3], (char*)0);
	else if(argc == 5)
		return execl(final_cmd, final_cmd, argv[1], argv[2], argv[3], argv[4], (char*)0);
	else if(argc == 6)
		return execl(final_cmd, final_cmd, argv[1], argv[2], argv[3], argv[4], argv[5], (char*)0);
	else if(argc == 7)
		return execl(final_cmd, final_cmd, argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], (char*)0);
	else if(argc == 8)
		return execl(final_cmd, final_cmd, argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], (char*)0);
	else if(argc == 9)
		return execl(final_cmd, final_cmd, argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], (char*)0);
	else
		printf("Not supported\n");
	return 1;
}
