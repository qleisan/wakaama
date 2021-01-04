#include "Arduino.h"
#include "lwm2m_wakaama.h"

//extern "C" int myfun(int);
extern int main2(int argc, char *argv[]);

char * args[] = {"", "-4","-n","ArduinoLightClient"};

WakaamaClient::WakaamaClient(int x)
{
  apa = x;
}

void WakaamaClient::run()
{
  Serial.print("calling main2()\r\n");
  main2(4, args);
  Serial.println("return from main2()\r\n");
}
