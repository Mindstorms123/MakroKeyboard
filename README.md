# MakroKeyboard
Script for a Makrokeyboards using an ESP32 and Cherrylike switches

Stuff I used:
  - esp32 C3: https://de.aliexpress.com/item/1005006149784075.html?spm=a2g0o.order_list.order_list_main.28.18045c5fI0yOi7&gatewayAdapt=glo2deu
  - cherrylike switches: https://s.click.aliexpress.com/e/_EHSSh6s

3d Print files:  
  - Base of the macro pad: https://makerworld.com/de/models/696565-6-button-esp32-iot-macro-pad#profileId-1606478
  - keycap generator: https://makerworld.com/de/models/1385177-customizable-keycaps?from=search#profileId-1434411
  - Emojis: 📁🔉🔊📄📋📸

The Connection pattern is the following:
  1. Connect one side of all the switches together and then connect that to ground
  2. Connect the other side of every switch to one of the following pins: 4,5,6,7,8,9
  3. Check if you like your layout and change it in the code if needed.

How to programm the esp32:
  1. Connect the USB-C Port of the esp32 to your computer
  2. Download the Arduino IDE https://www.arduino.cc/en/software/
  3. Open the Makropad_ESP32.ino Sketch file in the Arduino IDE
  4. Select the correct COM port in the IDE and select the Adqafruit QT Py ESP32-C3 as the device (if you dont see any devices with that name download the esp32 library first)
  5. Upload the Skatch via the upload button

How to use the Python code to use the Makrokeyboard on PC:
  1. download python https://www.python.org/downloads/
  2. open the terminal as administrator
  3. install independencies: pip install pyserial
                             pip install keyboard
                             pip install win10toast
  4.  change the folder in the macropad.vbs file to the on on your system
  5.  put the macropad.vbs file in the startupfolder:
      1. Press Windows + R
      2. write shell:startup
      3. press enter
      4. copy the macropad.vbs file to the startupfolder


Scripts for the Makrokeyboard © 2026 by Leon Wüste is licensed under Creative Commons Attribution-NonCommercial 4.0 International
