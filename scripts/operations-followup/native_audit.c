/* Isolated test instrumentation, not a product dependency. No input values. */
#define _GNU_SOURCE
#include <link.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>

static void record(const char *kind, const char *name) {
    const char *path=getenv("O6_NATIVE_LOG");
    if (!path) return;
    char safe[2048]; size_t j=0;
    for(size_t i=0;name && name[i] && j<sizeof(safe)-2;i++) {
        unsigned char c=name[i];
        if(c=='"'||c=='\\')safe[j++]='\\';
        if(c>=32)safe[j++]=c;
    }
    safe[j]=0;
    char line[2304];int n=snprintf(line,sizeof(line),"{\"kind\":\"%s\",\"pid\":%ld,\"euid\":%ld,\"name\":\"%s\"}\n",kind,(long)syscall(SYS_getpid),(long)syscall(SYS_geteuid),safe);
    /* Windows bind mounts do not provide reliable cross-process append. */
    char target[4096];
    snprintf(target,sizeof(target),"%s.%ld.%ld",path,(long)syscall(SYS_getpid),(long)syscall(SYS_gettid));
    int fd=syscall(SYS_openat,AT_FDCWD,target,O_WRONLY|O_APPEND|O_CREAT|O_CLOEXEC,0600);
    if(fd>=0){syscall(SYS_write,fd,line,n);syscall(SYS_close,fd);}
}
unsigned int la_version(unsigned int version) {record("audit_ready","");return LAV_CURRENT;}
unsigned int la_objopen(struct link_map *map,Lmid_t lmid,uintptr_t *cookie) {
    *cookie=(uintptr_t)map;record("object",map->l_name);
    return LA_FLG_BINDTO|LA_FLG_BINDFROM;
}
uintptr_t la_symbind64(Elf64_Sym *sym,unsigned int ndx,uintptr_t *refcook,uintptr_t *defcook,unsigned int *flags,const char *name) {
    if(strncmp(name,"acl_",4)==0 || strncmp(name,"sqlite3_",8)==0)record("binding",name);
    return sym->st_value;
}
