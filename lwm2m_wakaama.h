#ifndef MyClass_h
#define MyClass_h

#include "Arduino.h"
#include "liblwm2m.h"

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

class WakaamaClient
{
  public:
    WakaamaClient();
    //void run();
    void step();
    void handle_packet();
    lwm2m_context_t * lwm2mH;
    client_data_t data;
  private:
};

#endif
