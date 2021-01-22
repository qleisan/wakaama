#include "Arduino.h"
#include "lwm2m_wakaama.h"

#include "liblwm2m.h"

extern lwm2m_object_t * get_object_device(void);
// extern void free_object_device(lwm2m_object_t * objectP);
extern lwm2m_object_t * get_server_object(void);
// extern void free_server_object(lwm2m_object_t * object);
extern lwm2m_object_t * get_security_object(void);
// extern void free_security_object(lwm2m_object_t * objectP);

extern char * get_server_uri(lwm2m_object_t * objectP, uint16_t secObjInstID);

extern lwm2m_object_t * get_test_object(void);
// extern void free_test_object(lwm2m_object_t * object);

#define MAX_PACKET_SIZE 1024

typedef struct _connection_t
{
    struct _connection_t *  next;
    int                     sock;
#ifndef ARDUINO
    struct sockaddr_in6     addr;
#else
    int                     addr;
#endif
    size_t                  addrLen;
} connection_t;


typedef struct
{
    lwm2m_object_t * securityObjP;
    int sock;
    connection_t * connList;
    int addressFamily;
} client_data_t;

void * lwm2m_connect_server(uint16_t secObjInstID,
                            void * userData)
{
//     client_data_t * dataP;
//     char * uri;
//     char * host;
//     char * port;
//     connection_t * newConnP = NULL;

//     dataP = (client_data_t *)userData;

//     uri = get_server_uri(dataP->securityObjP, secObjInstID);

//     if (uri == NULL) return NULL;

//     //fprintf(stdout, "Connecting to %s\r\n", uri);
//     fprintf(stdout, "Connecting to SOMETHING\r\n");

//     // parse uri in the form "coaps://[host]:[port]"
//     if (0 == strncmp(uri, "coaps://", strlen("coaps://")))
//     {
//         host = uri+strlen("coaps://");
//     }
//     else if (0 == strncmp(uri, "coap://", strlen("coap://")))
//     {
//         host = uri+strlen("coap://");
//     }
//     else
//     {
//         goto exit;
//     }
//     port = strrchr(host, ':');
//     if (port == NULL) goto exit;
//     // remove brackets
//     if (host[0] == '[')
//     {
//         host++;
//         if (*(port - 1) == ']')
//         {
//             *(port - 1) = 0;
//         }
//         else goto exit;
//     }
//     // split strings
//     *port = 0;
//     port++;

//     newConnP = connection_create(dataP->connList, dataP->sock, host, port, dataP->addressFamily);
//     if (newConnP == NULL) {
//         fprintf(stderr, "Connection creation failed.\r\n");
//     }
//     else {
//         dataP->connList = newConnP;
//     }

// exit:
//     lwm2m_free(uri);
//     return (void *)newConnP;

    // TODO: Fixme
    //QLEISAN - WARNING UGLY TEMP HACK
    return (connection_t *)lwm2m_malloc(sizeof(connection_t));
}

void lwm2m_close_connection(void * sessionH,
                            void * userData)
{
    // client_data_t * app_data;
    // connection_t * targetP;

    // app_data = (client_data_t *)userData;
    // targetP = (connection_t *)sessionH;

    // if (targetP == app_data->connList)
    // {
    //     app_data->connList = targetP->next;
    //     lwm2m_free(targetP);
    // }
    // else
    // {
    //     connection_t * parentP;

    //     parentP = app_data->connList;
    //     while (parentP != NULL && parentP->next != targetP)
    //     {
    //         parentP = parentP->next;
    //     }
    //     if (parentP != NULL)
    //     {
    //         parentP->next = targetP->next;
    //         lwm2m_free(targetP);
    //     }
    // }
}


#define OBJ_COUNT 4


//extern "C" int myfun(int);
//extern int main2(int argc, char *argv[]);

char * args[] = {"", "-4","-n","ArduinoLightClient"};

WakaamaClient::WakaamaClient(int x)
{
    apa = x;
}

// for now this never returns...
void WakaamaClient::run()
{
    client_data_t data;
    lwm2m_context_t * lwm2mH = NULL;
    lwm2m_object_t * objArray[OBJ_COUNT];

    char * name = "testlwm2mclient";
    int result;

    memset(&data, 0, sizeof(client_data_t));

    // socket is should be created in the "sketch"

    objArray[0] = get_security_object();
    if (NULL == objArray[0])
    {
      Serial.println("Failed to create security object");
      goto error;
    }
    data.securityObjP = objArray[0];

    objArray[1] = get_server_object();
    if (NULL == objArray[1])
    {
      Serial.println("Failed to create server object");
      goto error;
    }

    objArray[2] = get_object_device();
    if (NULL == objArray[2])
    {
      Serial.println("Failed to create Device object");
      goto error;
    }

    objArray[3] = get_test_object();
    if (NULL == objArray[3])
    {
      Serial.println("Failed to create Test object");
      goto error;
    }

    /*
     * The liblwm2m library is now initialized with the functions that will be in
     * charge of communication
     */
    lwm2mH = lwm2m_init(&data);
    if (NULL == lwm2mH)
    {
        Serial.println("lwm2m_init() failed");
        goto error;
    }

    /*
     * We configure the liblwm2m library with the name of the client - which shall be unique for each client -
     * the number of objects we will be passing through and the objects array
     */
    result = lwm2m_configure(lwm2mH, name, NULL, NULL, OBJ_COUNT, objArray);
    if (result != 0)
    {
        //fprintf(stderr, "lwm2m_configure() failed: 0x%X\r\n", result); //not supporting proper printf now
        Serial.println("lwm2m_configure() failed");
        goto error;
    }

    while(1) {
        // main loop       

        struct timeval tv;
        tv.tv_sec = 60;
        tv.tv_usec = 0;

        /*
         * This function does two things:
         *  - first it does the work needed by liblwm2m (eg. (re)sending some packets).
         *  - Secondly it adjusts the timeout value (default 60s) depending on the state of the transaction
         *    (eg. retransmission) and the time before the next operation
         */
        result = lwm2m_step(lwm2mH, &(tv.tv_sec));
        if (result != 0)
        {
            //fprintf(stderr, "lwm2m_step() failed: 0x%X\r\n", result);
            Serial.println("lwm2m_step() failed");
            goto error;
        }
     
        //TODO: Not OK to block here, need to loop some time before packet is sent?

        Serial.println("LOOPING FOREVER");
        // blink slow
        for(;;) {
            digitalWrite(LED_BUILTIN, HIGH);
            delay(500);
            digitalWrite(LED_BUILTIN, LOW);
            delay(500);
        }
    }

    // ------------------------------------------------------------------

    error:
      Serial.println("ERROR LOOP");
      // blink fast
      for(;;) {
          digitalWrite(LED_BUILTIN, HIGH);
          delay(50);
          digitalWrite(LED_BUILTIN, LOW);
          delay(50);
    }
}


