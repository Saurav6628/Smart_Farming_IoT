// including all the header file for using diiferent sensors and using wifi module
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include "DHT.h"
#include <DallasTemperature.h>
#include <OneWire.h>
// defining the pins for usage of sensors
#define ONE_WIRE_BUS D7 
#define DHTTYPE DHT11 // type of the temperature sensor
const int sensor_pin = A0;  
const int DHTPin = D1; //--> The pin used for the DHT11 sensor is Pin D1 
DHT dht(DHTPin, DHTTYPE); //--> Initialize DHT sensor, DHT dht(Pin_used, Type_of_DHT_Sensor);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);   
// setting the variable for wifi module to use
const char* ssid = "happy birthday"; //--> Your wifi name or SSID.
const char* password = "12345678"; //--> Your wifi password.

//----------------------------------------Host & httpsPort
const char* host = "script.google.com";
const int httpsPort = 443;
//----------------------------------------

WiFiClientSecure client; //--> Create a WiFiClientSecure object.

String GAS_ID = "AKfycbzFVCiowQpoFYNym_Wm71w3Pr4Ek1mWVtRRxLQqDUs2ZJm7wL8glA6ReQaOOlnXbgNF"; //--> spreadsheet script ID

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);
  dht.begin();  //--> Start reading DHT11 sensors
  delay(500);  
  WiFi.begin(ssid, password); //--> Connect to your WiFi router
  client.setInsecure();
  pinMode(D5, OUTPUT);
  sensors.begin();
}

void loop() {
  float soilmoist;
  int irrigation=0;
  //Reading Sensor values
  soilmoist = ( 100.00 - ( (analogRead(sensor_pin)/1023.00) * 100.00 ) );
  sensors.requestTemperatures();  
  float soiltemp= sensors.getTempCByIndex(0);
  int h = dht.readHumidity();
  float t = dht.readTemperature();
  // Implementing the irrigation system
  if(soilmoist<20)
  { irrigation=1;digitalWrite(D5,HIGH);}
  else
  {irrigation=0;digitalWrite(D5, LOW);}
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t))
    return;
  //Sending data to excel sheet
  sendData(t, h,soilmoist, soiltemp,irrigation);
  delay(2000);
}

// Subroutine for sending data to Google Sheets
void sendData(float tem, int hum, float soilmoist, float soiltemp, int irrigation) {
  //Connect to Google host
  if (!client.connect(host, httpsPort)) {
    Serial.println("Not Connect");
    return;
  }
  //Processing data and sending data
  String string_temperature =  String(tem);
  String string_humidity =  String(hum, DEC);
  String string_soilmoist =  String(soilmoist);
  String string_soiltemp =  String(soiltemp);
  String string_irrigation =  String(irrigation);
  
  String url = "/macros/s/" + GAS_ID + "/exec?temperature=" + string_temperature + 
  "&humidity=" + string_humidity+ "&soilmoist=" + string_soilmoist+ "&soiltemp=" + 
  string_soiltemp+ "&irrigation=" + string_irrigation;
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
         "Host: " + host + "\r\n" +
         "User-Agent: BuildFailureDetectorESP8266\r\n" +
         "Connection: close\r\n\r\n\r\n");
  Serial.println(string_temperature);
  
}
