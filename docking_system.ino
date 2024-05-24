#include <WiFiManager.h> 
// #include <U8g2lib.h>
#include <PubSubClient.h>
#include <U8x8lib.h>
#include <Wire.h>


U8X8_SH1106_128X64_NONAME_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);


int positionY=24;
bool stop = 0;
int sensor_pin = 13;
String message = "";

const char* mqtt_server = "172.16.16.102";
// const char* mqtt_server = "192.168.0.101";

const int mqtt_port = 1883;

const char* Topic = "cameraDisplay";

WiFiManager wm;
WiFiClient espClient;
PubSubClient client(espClient);

IPAddress staticIP(172, 16, 16, 160); // Set the static IP address
IPAddress gateway(172, 16, 16, 1);    // Set the gateway IP address
IPAddress subnet(255, 255, 255, 0);   // Set the subnet mask
IPAddress dns(172, 16, 16, 1);        // Set the DNS server IP address



void pre(void)
{
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_f);    
  u8x8.clear();

  u8x8.inverse();
  u8x8.print("      A380      ");
  u8x8.setFont(u8x8_font_chroma48medium8_r);  
  u8x8.noInverse();
  u8x8.setFont(u8x8_font_open_iconic_arrow_4x4);
}


void ShowAnimation(String x){
  Serial.print("position .............");
  Serial.println(x);
  if( x == "Right"){
  //Right 
    pre();
    for(int i =0; i<=4; i++){
      u8x8.drawGlyph(i, 10, '@'+10); //Right arrow
      delay(100);
    }
  } else if(x =="Left"){
    //Left
    pre();
    for(int i =12; i>=9; i--){
      u8x8.drawGlyph(i, 10, '@'+9); //Left arrow
      delay(100);
    }
  } else if(x == "Middle"){
    //middle
    pre();
    u8x8.setFont(u8x8_font_open_iconic_arrow_2x2);
    for(int i = 6; i>=2; i--){
      u8x8.drawGlyph(7, i, '@'+11); //Up arrow
      delay(100);
    }
  }
}


void connectToWiFi() {
  u8x8.clear();
  u8x8.setFont(u8x8_font_chroma48medium8_r);
  u8x8.drawString(2,10,"connecting to ");
  u8x8.drawString(2,5,"WiFi...");
  delay(1000);

  wm.setSTAStaticIPConfig(staticIP, gateway, subnet, dns);
  bool res = wm.autoConnect("VDGS", "VDGS@123");  //(ssid, pass)

    if (!res) {
      u8x8.clear();
      u8x8.setFont(u8x8_font_5x8_f);
      u8x8.drawString(2,10,"connecting to");
      u8x8.drawString(2,5,"WiFi failed");
      Serial.println("Failed to connect");   
      delay(3000); 
      connectToWiFi();
    } 
    else {
      u8x8.clear();
      u8x8.setFont(u8x8_font_5x8_f);
      u8x8.drawString(2,10,"Connected to");
      u8x8.drawString(2,5,"WiFi");
      Serial.println("Connected...yeey :)");
      delay(1000);
    }
}

void ConnectMqtt(){
  u8x8.clear();
  u8x8.setFont(u8x8_font_5x8_f);
  u8x8.drawString(2,10,"connecting to ");
  u8x8.drawString(2,5,"MQTT...");
  delay(1000);

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Connect to MQTT broker
  if (client.connect("ESP8266MQTT")) {
    Serial.println("Connected to MQTT broker");
    u8x8.clear();
    u8x8.drawString(2,10,"Connected to");
    u8x8.drawString(2,5,"MQTT");

    client.subscribe(Topic);
  } else {
    Serial.println("MQTT connection failed, please check your settings");
    u8x8.clear();
    u8x8.drawString(2,10,"Connecting to");
    u8x8.drawString(2,5,"MQTT failed!");
    delay(2000);
    ConnectMqtt();

  }
}

void setup() {
    WiFi.mode(WIFI_STA); 
    u8x8.begin();
    Serial.begin(115200);
    pinMode(sensor_pin,INPUT);
    connectToWiFi();
    ConnectMqtt();
}

void loop() {
  if (!client.connected()) {
    ConnectMqtt();
  }
  ShowAnimation(message);
  stop = !digitalRead(sensor_pin);
  if(stop){
    u8x8.clear();
    u8x8.setFont(u8x8_font_profont29_2x3_f);
    u8x8.drawString(4,12,"STOP");
    message="";
    delay(1000);

  } else{
    client.loop();
  }
}


void callback(char* topic, byte* payload, unsigned int length) {
  
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");

    message = "";

    for (int i = 0; i < length; i++) {
      message += (char)payload[i];
    }

    Serial.println(message);
    message = message.c_str();
    
}
