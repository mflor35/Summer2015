
#include <OneWire.h> // needed for the temp sensor
//micros

#define XBEE Serial1 // communication from Mega to xbee
#define DEBUG_OUTPUT Serial // opens Arduinos serial monitor
#define DEBUG 1 // comment out when not needed
#define TERMINATOR "!"// 
#define LED 13 // for led pin
//setting up

OneWire wire(42);
//gloval variables for freq measurement
//ARDUNINO Mega - pin 49
unsigned long Time;//
int neg;// negative temp sign
int stillon;// for statement
int onOroff;// for led

//global variables for temp measurement
double temperature;// 
String package;
float SetPoint=20;//Temperature setpoint defualt set to 20

int deviationup = 2;//Temperature minimum deviation
int deviationdown = 2;//Temperature maximum deviation
byte addr[8];//Holds the identification information of the temperature sensor.
//-----------------------------------------------------
  
  
//----------------------------------------------------

void setup() {
  // put your setup code here, to run once:
  XBEE.begin(9600);//Serial on Xbee
  pinMode(LED,OUTPUT);//for led  
  // bottom code for debugging
  #ifdef DEBUG// calls Arduinos Serial to begin if enabled on top
    DEBUG_OUTPUT.begin(9600);
    //DEBUG_OUTPUT.println("Arduino Mega booted\n");
  #endif  
  //XBEE.println("HEY");
  //min of 75ms so that temp sensor value is store right off the bat
  //Time=millis(); // stores how much time has passed -here 750ms
  wire.reset_search();// this is to check if sensor is attached
  if(!wire.search(addr)){//enters if not
    #ifdef DEBUG
      DEBUG_OUTPUT.println("No temperature sensor found!"); 
    #endif //ifdef DEBUG
    XBEE.println("NO Temperature Sensor Found!");
    wire.reset_search();
    return;
  }
  if(OneWire::crc8(addr, 7)!= addr[7]){
    //potentially add a debug statement here
    #ifdef DEBUG
      DEBUG_OUTPUT.println("CRC for address is invalid");
    #endif
    XBEE.println("CRC for address is invalid");
    return;
  }
  wire.reset();//Resets the temperature sensor bus which is needsed before communication.
  wire.select(addr);//Selects the device addr, which is the single temperature sensor in the circuit.
  // once called must wait 750 millisecond
  wire.write(0x44);//The convert T command. Initiates the temperature conversion command.
  Time=millis(); // stores how much time has passed -here 750ms
  delay(751);// needs to delay a min of 75ms so that temp sensor value is store right off the bat
  
}

void thermometerRequestTemperature(void){// function responsible to start sensor when requested
   wire.reset();//Resets the temperature sensor bus which is needsed before communication.
   wire.select(addr);//Selects the device addr, which is the single temperature sensor in the circuit.
   wire.write(0x44);//The convert T command. Initiates the temperature conversion command.
}

void thermometerReadTemperature(byte data[12]){// function responsible for reading data stored in RAM in the sensor temp
  int i;
  wire.reset();//Resets the temperature sensor bus which is needsed before communication.
  wire.select(addr);//Selects the device addr, which is the single temperature sensor in the circuit.
  wire.write(0xBE); //The read Scratchpad command. 
  for(i=0; i<9; i++){
    data[i]=wire.read();
  }
}

void loop() {//main loop
  int HighByte, LowByte, TReading, SignBit, Tc_100, Whole, Fract;
  int setpointmax, setpointmin;
  byte data[12];
  // from setup to loop
  if ((millis()-Time >= 750)){// enters if statement every .75 secs
   thermometerReadTemperature(data);// once entered calls function with information of temperature stored in data[]
   if( OneWire::crc8(data, 8)!= data[8]){//enters if malfunction is prensent 
      #ifdef DEBUG
        DEBUG_OUTPUT.println("CRC for temperature sensor is not correct");
        DEBUG_OUTPUT.println(OneWire::crc8(data,8), HEX);        
      #endif //ifdef debug
      XBEE.println("CRC for temperature data is not correct"); //make this xbee
    }
    thermometerRequestTemperature();// calls function that reads temperature value 
    Time=millis();// sets Time as how much time has passed.
    LowByte = data[0];
    HighByte = data[1];
    TReading = (HighByte << 8) + LowByte;
    SignBit = TReading & 0x8000;  // test most sig bit
    if (SignBit) // negative
    {
      TReading = (TReading ^ 0xffff) + 1; // 2's comp
    }
    Tc_100 = (6 * TReading) + TReading / 4;    // multiply by (100 * 0.0625) or 6.25

    Whole = Tc_100 / 100;  // separate off the whole and fractional portions
    Fract = Tc_100 % 100;
    if (SignBit) // If its negative
    {
      neg=1;
      #ifdef DEBUG
        DEBUG_OUTPUT.print("-");
      #endif//ifdef debug
    }
    else{
      neg=0;
    }
    
    #ifdef DEBUG
      //DEBUG_OUTPUT.print("Celsius: ");
      //DEBUG_OUTPUT.print(Whole);
      //DEBUG_OUTPUT.print(".");
    #endif//ifdef
      if (Fract < 10){
        #ifdef DEBUG
          //DEBUG_OUTPUT.print("0");
        #endif//ifdef debug
    }
    #ifdef DEBUG
      //DEBUG_OUTPUT.print(Fract);
      //DEBUG_OUTPUT.print("\n");
    #endif//ifdef //
    
    double Split= Fract/100.0;
    temperature=(Whole+Split);// stores temperature as a whole number
    Serial.println(temperature);
    
    

  }
//..................................................................................//
    
    if (XBEE.available()){//If data comes in from XBee, send it out to serial monitor
      String tempStore;// defines vairbale as a string , char array but more powerfull-see arduino ref
      tempStore = XBEE.readString();// reads message that we recieved from xbee
      int j = tempStore.indexOf(TERMINATOR);// frame from xbee ends with '!' yields the index location
      package= tempStore.substring(0,j+1);// stores xbee message and splits it every !
      if(package.startsWith(":",8)){// checks for SetPoint package by key characters at the 8th index
        package.remove(0,10);// removes unwanted info from index 0 to 9... with spaces.. no space actually need 
        SetPoint=package.toFloat();// leaves simply the number
        XBEE.print("Set Point Recieved ");XBEE.println(SetPoint);
      }
    
        //arrays used for comparison
      char off[]= "OFF!";
      char on[]= "ON!";
      char temp[]="Temp!";
      char stat[]="Status!";
      
        
        
        
//....................................................... smart commands........... 
        
      if(package.equals(on)){//checls if still on
         onOroff=1;
         stillon=1;
         XBEE.println("Water Heater turned On");
         #ifdef DEBUG
           DEBUG_OUTPUT.println("Water Heater turned On");
         #endif
       }
      if(package.equals(off)){
         onOroff=0;
         stillon=0;
         XBEE.println("Water Heater turned Off");
         #ifdef DEBUG
           DEBUG_OUTPUT.println("Water Heater turned Off");
         #endif
       }
      if(package.equals(temp)){           
        XBEE.print("TEMPERATURE: ");
        if (neg==1){
           XBEE.print("-");
         }
         XBEE.print(temperature);XBEE.println(" C");
         #ifdef DEBUG
           DEBUG_OUTPUT.print("TEMPERATURE: ");
           if(neg==1){
             DEBUG_OUTPUT.print("-");
           }
           
           DEBUG_OUTPUT.print(temperature);DEBUG_OUTPUT.print(" Celsius");
         #endif//ifdef
         }
       if(package.equals(stat)){
         
          XBEE.print("Temp: ");XBEE.print(temperature);XBEE.println(" C");
          if(stillon== 1){
            XBEE.print("Water Heater turned On");
          }
          else{
            XBEE.print("Water Heater turned off");
            
         }
          #ifdef DEBUG
    
            DEBUG_OUTPUT.print("Temp: ");DEBUG_OUTPUT.print(temperature);DEBUG_OUTPUT.println(" C");
            if(stillon == 1){
              DEBUG_OUTPUT.print("Water Heater turned On");
              
            }
            else{
              DEBUG_OUTPUT.print("Water Heater turned Off");
              
           }
           #endif//ifdef
        }
   
    }
    
    
    
   
     float thresholdup= SetPoint + deviationup;
     float thresholddown= SetPoint - deviationdown;
     if(temperature <= thresholddown && onOroff == 1 ){//LED turns on if temperature is under setpoint and On is enabled from the XCTU menu.
          
          digitalWrite(LED,HIGH);
        }
      if(temperature >= thresholdup || onOroff == 0){//LED turns off if Off is enabled from the XCTU menu.
          digitalWrite(LED,LOW); // or statement overrides off
        }

}
  
  
  
   
      
  


