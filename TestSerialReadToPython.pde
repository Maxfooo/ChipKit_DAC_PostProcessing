// Source: https://github.com/vascop/Python-Arduino-Proto-API-v2
// vascop

#ifndef SERIAL_RATE
#define SERIAL_RATE         115200
#endif

#ifndef SERIAL_TIMEOUT
#define SERIAL_TIMEOUT      5
#endif

unsigned char pythonReady = '0';

void setup()
{
 Serial.begin(SERIAL_RATE);
 Serial.setTimeout(SERIAL_TIMEOUT);
}

void loop()
{
  switch (readData()) 
  {
    case 0:
      Serial.println("Hello World");
      break;
    
    case 1:
      Serial.println("Connected");
      break;
    
    case 99:
      // dummy
      break;
    
  }
}

char readData() 
{
  Serial.println("w");
  while(1) {
      if(Serial.available() > 0) {
          return Serial.parseInt();
      }
  }
}
