#include <lwm2m_wakaama.h>
#include "arduino_secrets.h"
#include <WiFiNINA.h>
#include <WiFiUdp.h>

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;

int status = WL_IDLE_STATUS;

//should be included in "arduino_secrets.h"
//char ssid[] = "";   // your network SSID (name)
//char pass[] = "";   // your network password (use for WPA, or use as key for WEP)


//TODO rename
void A(uint8_t * buffer, size_t length) 
{
    Serial.println("Inside funcion A now in ino");
    
    Serial.println("SUCCESS!! INSIDE connection_send()");
    Serial.println(length);
    for(int i=0;i<length;i++)
    {
        Serial.print(i);
        Serial.print(":");
        Serial.print(buffer[i],HEX);
        Serial.print(":");
        Serial.write(buffer[i]);
        Serial.println("");
    }
    Serial.println("Send packet using WiFiNINA");

    //qleisan - remove hardcoding, IP should be read from data structure
    IPAddress address(192, 168, 0, 23);
    Udp.beginPacket(address, 5683);
    Udp.write(buffer, length);
    Udp.endPacket();
    Serial.println("Packet Sent!");
}


void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}
 
void loop() {
    Serial.print("Boot delay...");
    delay(3000);
    Serial.print("Arduino lwm2m wakaama client initializing\r\n");

    WakaamaClient myclient(&A); //problem if outside loop()

    // check for the WiFi module:
    if (WiFi.status() == WL_NO_MODULE) {
        Serial.println("Communication with WiFi module failed!");
        // don't continue
        while (true);
    }

    // attempt to connect to Wifi network:
    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
        status = WiFi.begin(ssid, pass);

        // wait 10 seconds for connection:
        delay(10000);
    }
    Serial.println("Connected to wifi");

    // connecting to socket should be done connection.c ?
    Udp.begin(56830); 

    uint8_t buffer[MAX_PACKET_SIZE];
    int numBytes;

    for(;;) {
        myclient.step();
        digitalWrite(LED_BUILTIN, HIGH);
        delay(500);
        if (Udp.parsePacket()) {
            Serial.println("packet received");
            numBytes = Udp.read(buffer, MAX_PACKET_SIZE);
            Serial.print("numbytes = ");
            Serial.println(numBytes);
            myclient.handle_packet(numBytes, buffer);
        } else {
            Serial.println("no packet...");
        }
        digitalWrite(LED_BUILTIN, LOW);
        delay(500);
    }
}
