// #include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
// #include <Wire.h>
// #include <Adafruit_INA219.h>

// Define stepper motor connections and steps per revolution:
#define dirPin D0
#define stepPin D5
#define stepsPerRevolution 200

// Connect to the WiFi
const char* ssid = "CBCI-5958-2.4";
const char* password = "dimmed3755chose";
const char* mqtt_server = "10.1.10.183";

WiFiClient espClient;
PubSubClient client(espClient);

const byte ledPin = 0; // Pin with LED on Adafruit Huzzah
int status = WL_IDLE_STATUS; 

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
 char buff_p[length];
for (int i = 0; i < length; i++)
{
buff_p[i] = (char)payload[i];
}
buff_p[length] = '\0';
String msg_p = String(buff_p);
float val = msg_p.toFloat(); //to float
  Serial.println(val);
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266 Client")) {
      Serial.println("connected");
      // ... and subscribe to topic
      client.subscribe("A");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup()
{
  Serial.begin(9600);
 
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}
int steps2take = 100;
void loop()
{
  steps2take = 100;
  if (steps2take > 0) {
    digitalWrite(dirPin, HIGH);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    steps2take--;
  }
  if (steps2take < 0) {
    digitalWrite(dirPin, LOW);
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
    steps2take++;
  }
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
