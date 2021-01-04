#include <lwm2m_wakaama.h>
#include "arduino_secrets.h"
#include <WiFiNINA.h>
#include <WiFiUdp.h>

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;

WakaamaClient myclient(5);

int status = WL_IDLE_STATUS;
//should be included in "arduino_secrets.h"
//char ssid[] = "";   // your network SSID (name)
//char pass[] = "";   // your network password (use for WPA, or use as key for WEP)

//char * args[] = {"", "-4","-n","ArduinoLightClient"};

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}
 
void loop() {
    Serial.print("Boot delay...");
    delay(3000);
    Serial.print("continue\r\n");

    Serial.println(myclient.apa);

    Serial.println("arduinoclient is alive!");

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

    myclient.run();

    Serial.println("loop forever\r\n");

    for(;;) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
    }
}

