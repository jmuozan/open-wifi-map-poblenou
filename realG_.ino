/*
* MDEF Measuring the World
* Team realG
*
* 18 Feb 2023
* Added comments for documentation and removed sensitive information
*
* This is code for Barduino. It turns on the board, connects to a hard-coded wifi,
* finds all available networks and sends the count of available networks and count of 
* avaiable networks with no wifi password to the hard-coded MQTT broker
*
* The broker will receive this example message: 10, 3
* It means there are 10 networks and 3 of them are open/no password.
*
* This code only sends a single message.
*/
#include <WiFi.h> // library for wifi
#include <PubSubClient.h> // library for MQTT connection
#include <Adafruit_NeoPixel.h> // library for built-in LED

#define PIN 38

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 1  // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

const char* ssid = ""; // put wifi name
const char* password = ""; // put the wifi password
WiFiClient wifiClient;

const char* mqttBroker = ""; // put MQTT broker url
const char* mqttClientName = "futurehacker"; // you can replace this with your own client name
const char* mqttUser = ""; // MQTT User Authentification
const char* mqttPass = ""; // MQTT Password Authentification
const char* topic = "lab/mdef/realg"; // replace this with the topic you will use
PubSubClient mqttClient(wifiClient);

void mqttConnect() {
  
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
  
    if (mqttClient.connect(mqttClientName, mqttUser, mqttPass)) {
      Serial.println("connected");
      mqttClient.publish(topic, mqttClientName);
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  
  Serial.begin(115200);
  Serial.println("Hello");
  pixels.begin();  // INITIALIZE NeoPixel strip object (REQUIRED)

  pixels.setPixelColor(0, pixels.Color(150, 0, 0));
  pixels.show();  // Turn light to red

  // Connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  pixels.setPixelColor(0, pixels.Color(0, 0, 150));
  pixels.show();  // Turn light to blue when connected to wifi
  
  // MQTT setup
  mqttClient.setServer(mqttBroker, 1883); // replace 1883 with port
}

char msg[50];
bool msgSent = false;

void loop() {
  if(!msgSent) {
    // Check if we are still connected to the MQTT broker
    if (!mqttClient.connected()) {
      mqttConnect();
    }

    // Let PubSubClient library do his magic
    mqttClient.loop();

    // Scan for existing networks:
    Serial.println("Scanning available networks...");
    String numNetworks = listNetworks();

    numNetworks.toCharArray(msg, 50);
    Serial.print("sending to broker: ");
    Serial.println(numNetworks);

    mqttClient.publish(topic, msg);

    pixels.setPixelColor(0, pixels.Color(0, 150, 0));
    pixels.show();  // Turn light green when data is sent

    msgSent = true;
  }
}

String listNetworks() {
  int numFree = 0;

  // Scan for nearby networks:
  Serial.println("** Scan Networks **");
  int numSsid = WiFi.scanNetworks();
  if (numSsid != -1) {
    // Print the list of networks seen:
    Serial.print("number of available networks:");
    Serial.println(numSsid);

    // Print the network number and name for each network found:
    for (int thisNet = 0; thisNet < numSsid; thisNet++) {
      Serial.print(thisNet);
      Serial.print(") ");
      Serial.print(WiFi.SSID(thisNet));
      Serial.print("\tSignal: ");
      Serial.print(WiFi.RSSI(thisNet));
      Serial.print(" dBm");
      Serial.print("\tEncryption: ");
      Serial.println(WiFi.encryptionType(thisNet) ? 0: "Goodpeople");
      // check and add to count of the network has no password 
      if(WiFi.encryptionType(thisNet) == 0) {
        numFree++;
      }
    }
  } 
    return String(numSsid) + "," + String(numFree);
}

 
