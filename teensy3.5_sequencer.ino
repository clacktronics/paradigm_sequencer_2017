#include "sequence.h"

uint8_t pin[] = {5,3,29,2,6,4,30,7};
uint8_t dip_pin[] = {25,26,27,28};

uint16_t count = sequence[0][0];
uint16_t step_end = sequence[0][1];
uint16_t step_now,loops;

uint32_t debounce_trig = millis();
uint32_t elapsed_step = micros();
bool wait = true;

const uint16_t NUMSEQUENCES = sizeof(sequence)/3/2; // each entry is in 3 secions and each is 16bits so /2 

void setup() {

  Serial.begin(9600);
  delay(10);


  analogWriteResolution(8);

  for(int i;i<8;i++)
  {
    pinMode(pin[i], OUTPUT);
  }

    for(int i;i<4;i++)
  {
    pinMode(dip_pin[i], INPUT_PULLUP);
    
  }

  analogWriteFrequency(5, 200);
  analogWriteFrequency(3, 200);
  analogWriteFrequency(29, 200);
  analogWriteFrequency(2, 200);

  pinMode(11,INPUT);
  attachInterrupt(11, stepTrigger, RISING) ;

  

}


void loop() {

  while(!digitalRead(dip_pin[0]) ){
    
  for(int i=0;i<8;i++)
  {
    analogWrite(pin[i],0);
  }
  
  for(int i=0;i<8;i++)
  {
    analogWrite(pin[i],100);
    delay(500);
    analogWrite(pin[i],255);
    delay(500);
    analogWrite(pin[i], 0);
    delay(1000);
    if(digitalRead(dip_pin[0])){break;}
  }
    
  }

  if(!wait && micros() - elapsed_step > delays[step_now])
  {
    
    renderStep(count);
    count ++;
    if(count > step_end) { wait = true;}
    elapsed_step = micros();
  }

}

void nextloop()
{ 
      loops++;
}

void nextsequence()
{
      
      step_now++;
      if(step_now >= NUMSEQUENCES) {step_now=0;} 
      count = sequence[step_now][0];
      step_end = sequence[step_now][1]; // where to end
      loops = 0; 
}

void stepTrigger()
{
  if((millis() - debounce_trig) > 100) // Debounce just in case
   {
    wait=false;
    elapsed_step = 0;
    nextloop();
    if(loops >= sequence[step_now][2]){nextsequence();}
    count = sequence[step_now][0]; 
    debounce_trig = millis();
    }
}


void renderStep(uint16_t Step)

{

  uint8_t otpt;
  for(uint8_t i;i<8;i++) { 
    otpt = map(sequence_data[Step][i],0,9,0,255);
    analogWrite(pin[i],otpt); 
   } 
}

void clearPins()
{
  for(int i;i<8;i++) { analogWrite(pin[i],0); }
}


