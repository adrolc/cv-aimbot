#include <Mouse.h>

void setup()
{
    Serial.begin( 115200 );
#if !defined(__MIPSEL__)
    while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
    Mouse.begin();
}

void loop()
{
  if (Serial.available())
  {
    // read the incoming data as a string
    String inData = Serial.readStringUntil('\n');

    // split the data on the comma
    int commaIndex = inData.indexOf(',');
    String xString = inData.substring(0, commaIndex);
    String yString = inData.substring(commaIndex + 1);

    // convert the split data to integers
    int x = xString.toInt();
    int y = yString.toInt();

    if(x >= 0 && y >= 0){
      while(x > 0 || y > 0) {
        if(x > 0){
          Mouse.move(5, 0, 0);
          x -= 1;
        }
        if(y > 0){
          Mouse.move(0, 5, 0);
          y -= 1;
        }
      }
      Mouse.click();
    }

    else if(x >= 0 && y <= 0){
      while(x > 0 || y < 0) {
        if(x > 0){
          Mouse.move(5, 0, 0);
          x -= 1;
        }
        if(y < 0){
          Mouse.move(0, -5, 0);
          y += 1;
        }
      }
      Mouse.click();
    }

    else if(x <= 0 && y >= 0){
      while(x < 0 || y > 0) {
        if(x < 0){
          Mouse.move(-5, 0, 0);
          x += 1;
        }
        if(y > 0){
          Mouse.move(0, 5, 0);
          y -= 1;
        }
      }
      Mouse.click();
    }

    else if(x <= 0 && y <= 0){
      while(x < 0 || y < 0) {
        if(x < 0){
          Mouse.move(-5, 0, 0);
          x += 1;
        }
        if(y < 0){
          Mouse.move(0, -5, 0);
          y += 1;
        }
      }
      Mouse.click();
    }
  }
}

