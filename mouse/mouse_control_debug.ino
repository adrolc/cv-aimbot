#include <hidboot.h>
#include <usbhub.h>
#include <Mouse.h>
// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

class MouseRptParser : public MouseReportParser
{
protected:
	void OnMouseMove	(MOUSEINFO *mi);
	void OnLeftButtonUp	(MOUSEINFO *mi);
	void OnLeftButtonDown	(MOUSEINFO *mi);
	void OnRightButtonUp	(MOUSEINFO *mi);
	void OnRightButtonDown	(MOUSEINFO *mi);
	void OnMiddleButtonUp	(MOUSEINFO *mi);
	void OnMiddleButtonDown	(MOUSEINFO *mi);
};
void MouseRptParser::OnMouseMove(MOUSEINFO *mi)
{
    Serial.print("dx=");
    Serial.print(mi->dX, DEC);
    Serial.print(" dy=");
    Serial.println(mi->dY, DEC);
    Mouse.move(mi->dX, mi->dY, 0);
};
void MouseRptParser::OnLeftButtonUp	(MOUSEINFO *mi)
{
    Serial.println("L Butt Up");
    Mouse.release(MOUSE_LEFT);
};
void MouseRptParser::OnLeftButtonDown	(MOUSEINFO *mi)
{
    Serial.println("L Butt Dn");
    Mouse.press(MOUSE_LEFT);
};
void MouseRptParser::OnRightButtonUp	(MOUSEINFO *mi)
{
    Serial.println("R Butt Up");
    Mouse.release(MOUSE_RIGHT);
};
void MouseRptParser::OnRightButtonDown	(MOUSEINFO *mi)
{
    Serial.println("R Butt Dn");
    Mouse.press(MOUSE_RIGHT);
};
void MouseRptParser::OnMiddleButtonUp	(MOUSEINFO *mi)
{
    Serial.println("M Butt Up");
    Mouse.release(MOUSE_MIDDLE);
};
void MouseRptParser::OnMiddleButtonDown	(MOUSEINFO *mi)
{
    Serial.println("M Butt Dn");
    Mouse.press(MOUSE_MIDDLE);
};

USB     Usb;
USBHub     Hub(&Usb);
HIDBoot<USB_HID_PROTOCOL_MOUSE>    HidMouse(&Usb);

MouseRptParser                               Prs;

int randDist;

void setup()
{
    Serial.begin( 115200 );
#if !defined(__MIPSEL__)
    while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
    Mouse.begin();
    randomSeed(analogRead(0));
    Serial.println("Start");

    if (Usb.Init() == -1)
        Serial.println("OSC did not start.");

    delay( 200 );

    HidMouse.SetReportParser(0, &Prs);
}

void loop()
{
  Usb.Task();
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

    // use the integers to move the mouse
    // Mouse.move(x, y, 0);
  }
}

