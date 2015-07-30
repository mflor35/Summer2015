## Arduino Water Heater Relay Code

Hardware Used: 
* 1 Arduino MEGA 2560, 1 XBEE/Arduino adapter circuit, 2 XBEE S1 model, 1 DS18B20 Temperature Sensor

 The hardware listed above is implemented into an intergrated circuit in which 1 XBEE, in transparent mode, is connected with an Arduino via circuit adaptor. The XBEE/Arduino adapter consisted of a 2.2uf capacitor, 1 voltage regulater(KY5033), and 1 buffer(SN74AHC125N). The Other XBEE, in API mode,is connected to a labtop running on XCTU software. Both XBEE configured to communicate wirelessly with each other and the Arduino Mega serial monitors. DS18B20 temperature sensor intergrated into circuit:DS18B20 temperature sensor provides 9 to 12 bit celcius temperature measurements from -55° to +125°. Includes data verification. 
 
Software:
* Arduino IDE, XCTU Software

Arduino IDE, version 1.6.5, used to develop and upload code to Arduino Mega microcontroller. The XCTU software was used to configure XBEE's to interface with the Arduino. This program enables the communiction between XBEE devices and the Arduino board. All commands were programmed into software, date that was recieved and transmited from XBEE in AT mode is dependent on frame/package that the XBEE in API mode sent. A sample command is Temp. User would select it and the termperature would be sent to be displayed in the XCTU software.
 
XCTU Commands

5 commands programmed into the XCTU and Arduino: Transmisstd wirelessly. Results displayed on both XBEE and Arduino Monitors

* On! : Frame/package containing message to turn on Water Heater
* OFF! : Frame/package containing message to turn off Water Heater
* Temp! : Frame/package containing message to transmit temperature degrees in Celcuis measurement by DS18B20
* Status! : Frame/package containing message to transmit temperature and current on/off state of Water Heater
* Set_Temp: #! : Frame/package containing message to Set the temperature setpoint. User would replace the # sign with a number. 


 
Arduino Algorithm

Algorithm measures Temperature, waits for XBEE command, if avaiable Arduino code transmits requested data to XCTU.
package response:
ON!: Algorithm enables Water Heater On
OFF!: Algorithm disables Water Heater Off
Temp!: Algorithm transmits temperature measured to XCTU/XBEE
Status!: Algorithm transmits status of Water Heater 
Set_Temp: #!: Algorithm recieves new setpoint value and stores it in a variable and creates deadband zone according.

Note: Water heater can not be turned on unless On command is set.

DS18B20 Temperature Sensor
Data Sheet: http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf

Arduino Implementatin Download: http://www.pjrc.com/teensy/td_libs_OneWire.html

 Implementing the sensor is not a stright forward procedure and certain functions must be called to sucessfully obtain the temperature. The implemented temperature sensor used was presecured to be water proof and the circuits connectors were already made. The temperatur senesor has 3 pins: GND, VDD, and DQ. This is to succesfully connect the sensor to the Arduino board.To externall power the device, the VDD pin is connected to the 5V pin on the Arduino board. GND is connected to the ground on the circuit. DQ is the temperaturen output signal. This is connected to pin 42 on the Arduino. A 4.7K ohm resistor is connected between the VDD and DQ pins. Here is the code to succesfully run the device. To promote abstraction blocks of code will be posted with their funcionalit:
 
 This enables the DS18B20 sensor to pin 42 in the Arduino board.
 
 OneWire wire(42);
 
 This block of code begins the initiation to obtain the temperature. It's put in a void function so it can be later called. 
 
 void thermometerRequestTemperature(void){
 
   wire.reset();
   
   wire.select(addr);
   
   wire.write(0x44)}.
   
 
 
This code is also in a a void function. It takes the scractch pad and puts the data in an array.
 
void thermometerReadTemperature(byte data[12]){

int i;

wire.reset();

wire.select(addr);

wire.write(0xBE); //The read Scratchpad command.

for(i=0; i<9; i++){

data[i]=wire.read();

}
}

Next is the error checking. A CRC verification is performed to make sure that the data received matches with the data expected. If an error occurs, it will be stated to the XCTU teerminal software.

if( OneWire::crc8(data, 8)!= data[8]){
 
malfunction is prensent 
ifdef DEBUG
      
DEBUG_OUTPUT.println("CRC for temperature sensor is not correct");
        
DEBUG_OUTPUT.println(OneWire::crc8(data,8), HEX);
        
endif 
      
XBEE.println("CRC for temperature data is notcorrect");
}

This chunk of code sucesfuly takes the temperature from the data array. It is taken in the hexidecimal fomat. The code below converts it to floating point. The temperature is then outputed to the XCTL monitor upon request.

LowByte = data[0];

HighByte = data[1];

TReading = (HighByte << 8) + LowByte;

SignBit = TReading & 0x8000;  

if (SignBit) 

{
    TReading = (TReading ^ 0xffff) + 1; // 2's comp
}
Tc_100 = (6 * TReading) + TReading / 4;

Whole = Tc_100 / 100;  

Fract = Tc_100 % 100;

if (SignBit){

neg=1;}

else{

neg=0; }

double Split= Fract/100.0;

temperature=(Whole+Split);

Serial.println(temperature);

   


