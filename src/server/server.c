#include <signal.h>
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <openssl/md5.h>
#define ITEMPATH "./"


typedef enum {
    Rain_Login=0x00,
    Rain_xmlReq=0x01,
    Rain_HasReq=0x02,
    Rain_AllMof=0x03,
    Rain_xmlUpl=0x04,
    Rain_xmlSnd=0x81,
    Rain_HasSnd=0x82,
    Rain_ModRep=0x83,
    Rain_UnLcok=0x84
} RainMod; 

typedef struct {
    unsigned char mod;
    unsigned char IDLength;
    unsigned short Dataoffset;
    unsigned short DataLength;
    char * userID;
    char * data;
} dataST;


int doit(int refd);
void receiveData(int refd,dataST* myblock);
void login(int refd,dataST* myblock);
void xmlReq(int refd,dataST* myblock);
void HasReq(int refd,dataST* myblock);
void AllMof(int refd,dataST* myblock);
void xmlUpl(int refd,dataST* myblock);
void createDefaultXML(dataST* myblock); // unmaked

unsigned int calculateXMLHash(char* userID); //calcualte and save it
void xmlSnd(int refd,dataST* myblock);
void DataPacker(int refd,dataST* myblock,int mod,int dataSize,void * data);
void sendHeader(int refd,dataST* myblock,int mod,int dataSize);

int main(int argc,char **argv)
{

    struct sockaddr_in myaddr ,clientaddr;
    int sockid,newsockid;

    struct stat st;

    if(stat("lock",&st)!=0) system("mkdir lock");
    if(stat("xml",&st)!=0) system("mkdir xml");
    if(stat("hash",&st)!=0) system("mkdir hash");

    if(stat("./lock/d.lock",&st)!=0) printf("1");
    if(stat("./lock/e.lock",&st)!=0) printf("2");





    sockid=socket(AF_INET,SOCK_STREAM,0);
    memset(&myaddr,'0',sizeof(myaddr));
    myaddr.sin_family=AF_INET;
    if(argc==1){
        myaddr.sin_port=htons(1287);
        printf("sock 8888\n");
    }
    else{ 
        myaddr.sin_port=htons(atoi(argv[1]));
        printf("sock %d\n",atoi(argv[1]));
    }


    myaddr.sin_addr.s_addr=inet_addr("127.0.0.1");
    if(sockid==-1)
    {
        perror("socket");
        exit(1);
    }
    else printf("socket succes\n");



    int len=sizeof(myaddr);
    int yes=1;
    if ( setsockopt(sockid, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1 )
    {
        perror("setsockopt");
    }

    if(bind(sockid,( struct sockaddr*)&myaddr,len)==-1)
    {
        perror("bind");
        exit(2);
    }
    else printf("bind succ\n");

    if(listen(sockid,10)==-1)
    {
        perror("listen");
        exit(3);
    }else printf("listen succ\n");

    int pid,new;
    static int counter=0;
    for(;;)
    {       
        new =accept(sockid,(struct sockaddr *)&clientaddr,&len);
        printf("accept succ\n");
        if((pid=fork())==-1)
        {
            close(new);
            continue;
        }   
        else if(pid>0)
        {
            close(new);
            continue;
        }   
        else if(pid==0)
        {
            printf("accept succ\n");
            doit(new); 
            close(new);
            break;
        }

    }
    close(sockid);
    return 0;
}

int doit(int refd){
    RainMod rainmod;
    dataST receivedata;
    receiveData(refd,&receivedata);
    printf("receviedData\n");

    write(1,receivedata,6);
    write(1,receivedata.userID,receivedata.IDLength);
    write(1,receivedata.data,receivedata.DataLength);

    rainmod=(RainMod)(int)receivedata.mod;
    switch(rainmod){
        case Rain_Login :
            login(refd,&receivedata);
            printf("Login\n");
            break;
        case Rain_xmlReq :
            xmlReq(refd,&receivedata);
            printf("Req\n");
            break;
        case Rain_HasReq :
            HasReq(refd,&receivedata);
            printf("Hreq\n");
            break;
        case Rain_AllMof :
            AllMof(refd,&receivedata);
            printf("MofAllow\n");
            break;
        case Rain_xmlUpl :
            xmlUpl(refd,&receivedata);
            printf("xmlupl\n");
            break;
    }

    if(receivedata.userID!=NULL) free(receivedata.userID);
    if(receivedata.data!=NULL) free(receivedata.data);
}

void receiveData(int refd,dataST* myblock){
    int MSGSize,readpoint;

    MSGSize=6;
    readpoint=0;

    while(readpoint<MSGSize)
        readpoint+=read(refd,(void *)myblock+readpoint,MSGSize-readpoint);

    if(myblock->Dataoffset!=6){
        myblock->userID=malloc(sizeof(char)*(myblock->Dataoffset-5));

        MSGSize=myblock->Dataoffset-6;
        readpoint=0;
        while(readpoint<MSGSize)
            readpoint+=read(refd,myblock->userID+readpoint,MSGSize-readpoint);
        myblock->userID[myblock->IDLength]='\0';
    }
    else myblock->userID=NULL;
    if(myblock->DataLength!=0){
        myblock->data=malloc(sizeof(char)*(myblock->DataLength+1)); 

        MSGSize=myblock->DataLength;
        readpoint=0;
        while(readpoint<MSGSize)
            readpoint+=read(refd,myblock->data+readpoint,MSGSize-readpoint);
        myblock->data[myblock->DataLength]='\0';
    }
    else myblock->data=NULL;
}


void login(int refd,dataST* myblock){
    const int padsize=15;
    char *filename= malloc(myblock->IDLength+padsize);
    struct stat st;
    snprintf(filename,myblock->IDLength+padsize,"%sxml/%s.xml",ITEMPATH,myblock->userID);
    if(stat(filename,&st)!=0){
        createDefaultXML(myblock);
        calculateXMLHash((char *)myblock->userID);	
    }

    xmlSnd(refd,myblock);
    free(filename);
}

unsigned int calculateXMLHash(char* userID){
    const int padsize=15;
    unsigned char c[MD5_DIGEST_LENGTH];
    char *filename= malloc(strlen(userID)+padsize);
    snprintf(filename,strlen(userID)+padsize,"%sxml/%s.xml",ITEMPATH,userID);
    FILE *inFile = fopen (filename, "rb");
    MD5_CTX mdContext;
    unsigned char data[1024];
    int i,bytes;

    if (inFile == NULL) {
        printf ("%s can't be opened.\n", filename);
        return 0;
    }

    MD5_Init (&mdContext);
    while ((bytes = fread (data, 1, 1024, inFile)) != 0)
        MD5_Update (&mdContext, data, bytes);
    MD5_Final (c,&mdContext); 
    fclose (inFile);

    snprintf(filename,strlen(userID)+padsize,"%shash/%s.hash",ITEMPATH,userID);

    inFile = fopen (filename, "wb");
    for(i = 0; i < MD5_DIGEST_LENGTH; i++) fprintf(inFile,"%02x", c[i]);
    fclose (inFile);
    return 0;
}


void xmlSnd(int refd,dataST* myblock){
    char *file_data;
    size_t nbytes = 0;
    size_t bytes;
    unsigned char mod = 0x81; 
    const int padsize=15;
    int pos,end;
    char *filename= malloc(myblock->IDLength+padsize);
    snprintf(filename,myblock->IDLength+padsize,"%sxml/%s.xml",ITEMPATH,myblock->userID);
    FILE *inFile = fopen (filename, "rb");
    pos = ftell (inFile);
    fseek (inFile, 0, SEEK_END);
    end = ftell (inFile);
    fseek (inFile, pos, SEEK_SET);

    file_data=malloc(end);


    nbytes=0;
    while ( nbytes<end){
        bytes=fread(file_data+nbytes,sizeof(char), end-nbytes ,inFile);
        if(bytes<=0) break;
        else nbytes+=bytes;
    }
    printf("%s",file_data);
    DataPacker(refd,myblock,mod,end,file_data);

    free(file_data);
    fclose(inFile);
    free(filename);
}


void xmlReq(int refd,dataST* myblock){
    xmlSnd(refd,myblock);
}


void HasReq(int refd,dataST* myblock){
    const int CHUNK_SIZE=128;
    char file_data[CHUNK_SIZE];
    size_t nbytes = 0;
    unsigned char mod = 0x82; 
    const int padsize=15;
    int pos,end;
    char *filename= malloc(myblock->IDLength+padsize);
    snprintf(filename,myblock->IDLength+padsize,"%shash/%s.hash",ITEMPATH,myblock->userID);
    FILE *inFile = fopen (filename, "rb");
    pos = ftell (inFile);
    fseek (inFile, 0, SEEK_END);
    end = ftell (inFile);
    fseek (inFile, pos, SEEK_SET);
    
    nbytes=0;
    while ( (nbytes += fread(file_data+nbytes,sizeof(char),  CHUNK_SIZE,inFile)!=end) );
    printf("%s",file_data);
    DataPacker(refd,myblock,mod,end,file_data);

    fclose(inFile);
    free(filename);

}


void AllMof(int refd,dataST* myblock){
    const int padsize=15;
    char *filename= malloc(myblock->IDLength+padsize);
    struct stat st;
    snprintf(filename,myblock->IDLength+padsize+padsize,"%slock/%s.lock",ITEMPATH,myblock->userID);
    printf("%s\n",filename);
    if(stat(filename,&st)!=0){
        FILE * infile=fopen(filename,"wb");
        fclose(infile);
        DataPacker(refd,myblock,0x83,3,"YES");
        printf("Yes\n");
    }
    else {
        printf("stat: %d",stat(filename,&st));
      
        DataPacker(refd,myblock,0x83,2,"NO");
        printf("no\n");
    }
    free(filename);
}

void xmlUpl(int refd,dataST* myblock){
    const int padsize=15;
    char *filename= malloc(myblock->IDLength+padsize);

    snprintf(filename,myblock->IDLength+padsize,"%sxml/%s.xml",ITEMPATH,myblock->userID);
    FILE *inFile = fopen (filename, "wb");

    fwrite(myblock->data,1,myblock->DataLength,inFile);
    fclose(inFile);


    calculateXMLHash(myblock->userID);

    snprintf(filename,myblock->IDLength+padsize,"%slock/%s.lock",ITEMPATH,myblock->userID);
    unlink (filename);
    free(filename);

    
    DataPacker(refd,myblock,0x84,0,"");
}





void createDefaultXML(dataST* myblock){
    const int padsize=15;
    char *filename= malloc(myblock->IDLength+padsize);

    snprintf(filename,myblock->IDLength+padsize,"%sxml/%s.xml",ITEMPATH,myblock->userID);
    FILE *inFile = fopen (filename, "wb");

    fprintf(inFile,"<Rain><username>%s</username></Rain>",myblock->userID);
    fclose(inFile);

}

void DataPacker(int refd,dataST* myblock,int mod,int dataSize,void * data){
    int sendpa=0;
    int tosend=myblock->Dataoffset+dataSize;
    char * Mydata= (char *)malloc(tosend) ;   
    myblock->mod=mod;
    myblock->DataLength=dataSize;
    memcpy(Mydata,myblock,6);
    memcpy(Mydata+6,myblock->userID,myblock->Dataoffset-6);
    memcpy(Mydata+myblock->Dataoffset,data,myblock->DataLength);
    while(sendpa<tosend)
        sendpa+=send(refd,Mydata+sendpa,tosend-sendpa,0);
    free(Mydata);
}

void sendHeader(int refd,dataST* myblock,int mod,int dataSize){
    int sendpa=0;
    int tosend=myblock->Dataoffset;
    char * Mydata= (char *)malloc(tosend) ;   
    myblock->mod=mod;
    myblock->DataLength=dataSize;
    memcpy(Mydata,myblock,6);
    memcpy(Mydata+6,myblock->userID,myblock->Dataoffset-6);
    
    while(sendpa<tosend)
        sendpa+=send(refd,Mydata+sendpa,tosend-sendpa,0);
    free(Mydata);
}


