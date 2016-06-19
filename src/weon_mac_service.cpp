/**
 *************************************************************
 *iptables for mac address
 *
 *
 *************************************************************/

#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <stdio.h>
#include <netinet/in.h>
#include <resolv.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
#include <string>
#include <fstream>
/** Puerto  */
#define PORT       7000

/** Número máximo de hijos */
#define MAX_CHILDS 7

/** Longitud del buffer  */
#define BUFFERSIZE 600



int AtiendeCliente(int socket, struct sockaddr_in addr);
int DemasiadosClientes(int socket, struct sockaddr_in addr);
void error(int code, char *err);
void reloj(int loop);

//estas 2 funciones se agregaron por que IOS no permite obtener la MAC
std::string getCmdOutput(const std::string& mStr)
{
    std::string result,file;
    FILE * pipe {popen(mStr.c_str(),"r")};
    char buffer[256];

    while(fgets(buffer,sizeof(buffer),pipe)!=NULL)
    {
        file=buffer;
        result+=file.substr(0,file.size()-1);
    }

    pclose(pipe);
    return result;
}

std::string GetMac(std::string oneIP)
{
    std::string txt="arp -a "+oneIP;//+" |awk '{print $4}'";
    printf("GetMac: ");
    printf(txt.c_str());
    std::string resultado;

    //getCmdOutput("( ping "+oneIP+" -c 1 )");
    resultado=getCmdOutput("( "+txt+" )");

    for(int i =0;i<3;i++)
    {
        resultado=resultado.substr(resultado.find(" ")+1);
    }
    printf("FOR: ");
    printf(resultado.c_str());
    printf("\n");

    resultado=resultado.substr(0,resultado.find(" "));
    return resultado;
}

//funciones para la mac
int main(int argv, char** argc){

     int socket_host;
     struct sockaddr_in client_addr;
     struct sockaddr_in my_addr;
     struct timeval tv;      /* Para el timeout del accept */
     socklen_t size_addr = 0;
     int socket_client;
     fd_set rfds;        /* Conjunto de descriptores a vigilar */
     int childcount=0;
     int exitcode;

     int childpid;
     int pidstatus;

     int activated=1;
     int loop=0;

     socket_host = socket(AF_INET, SOCK_STREAM, 0);
     if(socket_host == -1)
       error(1, "No puedo inicializar el socket");

     my_addr.sin_family = AF_INET ;
     my_addr.sin_port = htons(PORT);
     my_addr.sin_addr.s_addr = INADDR_ANY ;


     if( bind( socket_host, (struct sockaddr*)&my_addr, sizeof(my_addr)) == -1 )
       error(2, "El puerto está en uso"); /* Error al hacer el bind() */

     if(listen( socket_host, 10) == -1 )
       error(3, "No puedo escuchar en el puerto especificado");

     size_addr = sizeof(struct sockaddr_in);


     while(activated)
       {
     reloj(loop);
     /* select() se carga el valor de rfds */
     FD_ZERO(&rfds);
     FD_SET(socket_host, &rfds);

     /* select() se carga el valor de tv */
     tv.tv_sec = 0;
     tv.tv_usec = 500000;    /* Tiempo de espera */

     if (select(socket_host+1, &rfds, NULL, NULL, &tv))
       {
         if((socket_client = accept( socket_host, (struct sockaddr*)&client_addr, &size_addr))!= -1)
           {
         loop=-1;        /* Para reiniciar el mensaje de Esperando conexión... */
         printf("\nSe ha conectado %s por su puerto %d\n", inet_ntoa(client_addr.sin_addr), client_addr.sin_port);
         switch ( childpid=fork() )
           {
           case -1:  /* Error */
             error(4, "No se puede crear el proceso hijo");
             break;
           case 0:   /* Somos proceso hijo */
             if (childcount<MAX_CHILDS)
               exitcode=AtiendeCliente(socket_client, client_addr);
             else
               exitcode=DemasiadosClientes(socket_client, client_addr);

             exit(exitcode); /* Código de salida */
           default:  /* Somos proceso padre */
             childcount++; /* Acabamos de tener un hijo */
             close(socket_client); /* Nuestro hijo se las apaña con el cliente que
                          entró, para nosotros ya no existe. */
             break;
           }
           }
         else
           fprintf(stderr, "ERROR AL ACEPTAR LA CONEXIÓN\n");
       }

     /* Miramos si se ha cerrado algún hijo últimamente */
     childpid=waitpid(0, &pidstatus, WNOHANG);
     if (childpid>0)
       {
         childcount--;   /* Se acaba de morir un hijo */

         /* Muchas veces nos dará 0 si no se ha muerto ningún hijo, o -1 si no tenemos hijos
          con errno=10 (No child process). Así nos quitamos esos mensajes*/

         if (WIFEXITED(pidstatus))
           {

         /* Tal vez querremos mirar algo cuando se ha cerrado un hijo correctamente */
         if (WEXITSTATUS(pidstatus)==99)
           {
             printf("\nSe ha pedido el cierre del programa\n");
             activated=0;
           }
           }
       }
     loop++;
     }

     close(socket_host);

     return 0;
}

     /* No usamos addr, pero lo dejamos para el futuro */
int DemasiadosClientes(int socket, struct sockaddr_in addr)
{
     char buffer[BUFFERSIZE];
     int bytecount;

     memset(buffer, 0, BUFFERSIZE);

     sprintf(buffer, "Demasiados clientes conectados. Por favor, espere unos minutos\n");

     if((bytecount = send(socket, buffer, strlen(buffer), 0))== -1)
       error(6, "No puedo enviar información");

     close(socket);

     return 0;
}

int AtiendeCliente(int socket, struct sockaddr_in addr)
{

     char buffer[BUFFERSIZE];
     char aux[BUFFERSIZE];
     int bytecount;
     int fin=0;
     int code=0;         /* Código de salida por defecto */
     time_t t;
     struct tm *tmp;

     while (!fin)
       {

     memset(buffer, 0, BUFFERSIZE);
     if((bytecount = recv(socket, buffer, BUFFERSIZE, 0))== -1)
       error(5, "No puedo recibir información");


     //verificamos si lo que mandan es una ip y entonces la cambiamos por MAC
     if (strncmp(buffer, "IP", 2)==0)
     {
         printf("Se trata de in IPHONE\n");
         std::string comando(buffer);
         comando=comando.substr(3);
         comando="weon:"+GetMac(comando);

         printf("El comando dice:");
         printf(comando.c_str());

         comando.copy(buffer,comando.length(),0);
     }
     ///////////////////////////////////////
     /* Evaluamos los comandos */
     /* El sistema de gestión de comandos es muy rudimentario, pero nos vale */
     /* Comando TIME - Da la hora */
     //weon:mac
     if (strncmp(buffer, "weon", 4)==0)
       {
         t = time(NULL);
         tmp = localtime(&t);
         //separo la mac address
         std::string mac(buffer);
         mac=mac.substr(5,17);


         //registro el inicio de sesion, talvez solo registro todos

         memset(buffer, 0, 7);
         strftime(buffer, BUFFERSIZE, "echo '%H|", tmp);
         std::string txt(buffer);
         txt.append(mac);
         txt.append("' >> /home/rock/WeOn/logs/started_sections.txt");
         memset(buffer, 0, txt.length());
         txt.copy(buffer,txt.length(),0);
         system(buffer);
         printf(buffer);
         //coloco la regla que logea
         //se registrara todo, esta linea no es necesaria

         txt="iptables -A FORWARD -p tcp --dport 443 -m mac --mac-source ";
         txt.append(mac);
         txt.append(" -m state --state NEW -j LOG --log-prefix 'weon:");
         txt.append(mac);
         txt.append("' --log-level 4 ");
         memset(buffer, 0, BUFFERSIZE);
         txt.copy(buffer,txt.length(),0);
         system(buffer);
         printf(buffer);

         //coloco la regla que concede permisos
         //std::string txt;
         txt="/sbin/iptables -A FORWARD -m mac --mac-source ";
         txt.append(mac);
         txt.append(" -j ACCEPT");
         memset(buffer, 0,BUFFERSIZE);
         txt.copy(buffer,txt.length(),0);
         system(buffer);
         printf(buffer);

         //regla que manda todo a squid
         txt="/sbin/iptables -t nat -I PREROUTING 2 -m mac --mac-source ";
         txt.append(mac);
         txt.append(" -p tcp --dport 80 -j DNAT --to-destination 192.168.1.250:3128");
         memset(buffer, 0,BUFFERSIZE);
         txt.copy(buffer,txt.length(),0);
         system(buffer);
         printf(buffer);
         //esta regla deja saliro todo el trafico que no va al 80
         txt="/sbin/iptables -t nat -I PREROUTING 3 -m mac --mac-source ";
         txt.append(mac);
         txt.append(" -j ACCEPT");
         memset(buffer, 0,BUFFERSIZE);
         txt.copy(buffer,txt.length(),0);
         system(buffer);
         printf(buffer);

         //regreso mesage de concedido
         txt="OK:"+mac;
         memset(buffer, 0, BUFFERSIZE);
         txt.copy(buffer,txt.length(),0);
         fin=1;
       }

     else if (strncmp(buffer, "check", 5)==0)
     {

         std::string cmd(buffer);
         cmd=cmd.substr(6);
         memset(buffer,0,BUFFERSIZE);
         cmd.copy(buffer,cmd.length(),0);
         system(buffer);
         fin=1;
     }
     /* Comando DATE - Da la fecha */
     else if (strncmp(buffer, "DATE", 4)==0)
       {
         memset(buffer, 0, BUFFERSIZE);

         t = time(NULL);
         tmp = localtime(&t);

         strftime(buffer, BUFFERSIZE, "Hoy es %d/%m/%Y\n", tmp);
       }
     /* Comando HOLA - Saluda y dice la IP */
     else if (strncmp(buffer, "HOLA", 4)==0)
       {
         memset(buffer, 0, BUFFERSIZE);
         sprintf(buffer, "Hola %s, ¿cómo estás?\n", inet_ntoa(addr.sin_addr));
       }
     /* Comando EXIT - Cierra la conexión actual */
     else if (strncmp(buffer, "E", 1)==0)
       {
         memset(buffer, 0, BUFFERSIZE);
         sprintf(buffer, "Hasta luego. Vuelve pronto %s\n", inet_ntoa(addr.sin_addr));
         fin=1;
       }
     /* Comando CERRAR - Cierra el servidor */
     else if (strncmp(buffer, "Q",1)==0)
       {
         memset(buffer, 0, BUFFERSIZE);
         sprintf(buffer, "Adiós. Cierro el servidor\n");
         fin=1;
         code=99;        /* Salir del programa */
       }
     else
       {
         sprintf(aux, "ECHO: %s\n", buffer);
         strcpy(buffer, aux);
       }

     if((bytecount = send(socket, buffer, strlen(buffer), 0))== -1)
       error(6, "No puedo enviar información");
       }

     close(socket);
     return code;
}

void reloj(int loop)
{
   if (loop==0)
     printf("[SERVIDOR] Esperando conexión  ");

   printf("\033[1D");        /* Introducimos código ANSI para retroceder 2 caracteres */
   switch (loop%4)
     {
     case 0: printf("|"); break;
     case 1: printf("/"); break;
     case 2: printf("-"); break;
     case 3: printf("\\"); break;
     default:            /* No debemos estar aquí */
       break;
     }

   fflush(stdout);       /* Actualizamos la pantalla */
}

void error(int code, char *err)
{
   char *msg=(char*)malloc(strlen(err)+14);
   sprintf(msg, "Error %d: %s\n", code, err);
   fprintf(stderr, msg);
   exit(1);
}
