#include <Wire.h>
#include <PinChangeInt.h>

#define MAJOR_SOFT_VERSION 0
#define MINOR_SOFT_VERSION 5

#define SLAVE_ADDRESS 0x05
#define NB_ENCODER_MAX 8

#define PIN_MODE_MSG_ID  0x01
#define DIGITAL_READ_MSG_ID  0x02
#define DIGITAL_WRITE_MSG_ID  0x03
#define DIGITAL_WRITES_MSG_ID  0x04
#define ANALOG_READ_MSG_ID  0x05
#define ANALOG_WRITE_MSG_ID  0x06
#define DEFINE_ENCODER_MSG_ID  0x07
#define GET_ENCODER_COUNTER_MSG_ID 0x08
#define GET_SOFT_VERSION_MSG_ID 0x09
#define GET_STATUS_MSG_ID 0x0A
#define GET_TYPE_ARDUINO_MSG_ID 0x0B
#define GET_IDL_VERSION_MSG_ID 0x0C

#define DIGITAL_READ_VALUE_MSG_ID  0xF2
#define ANALOG_READ_VALUE_MSG_ID  0xF5
#define ENCODER_COUNTER_MSG_ID 0xF8
#define STATUS_MSG_ID 0xFA
#define TYPE_ARDUINO_MSG_ID 0xFB
#define IDL_VERSION_MSG_ID 0xFC
#define SOFT_VERSION_MSG_ID 0xF9

byte g_pIdlVersion[2] = {0, 2};
byte g_Status = 3;
byte g_TypeArduino = 0x12;


const int Led = 11; 
byte g_pInputMsgBuf[32];
byte g_pOutputMsgBuf[32];
int g_OutputMsgSize = 0;

byte g_EncoderCounterIdRequest = 0;
byte g_DigitalePinReadRequest = 0;
byte g_AnalogPinReadRequest = 0;

typedef struct EncoderStruct
{
  int Id; // TBD_PP a supprimer
  int pinA;
  int pinB;
  int tick_counter;
  void (*ptr_InterruptA) (void);
  void (*ptr_InterruptB) (void);
  byte cptA, prevCptA; // Compteurs d'interruption A
  byte cptB, prevCptB; // Compteurs d'interruption B  
}EncoderStruct;

EncoderStruct g_pEncoderTab[NB_ENCODER_MAX];


void prepareMsg2Send(byte* p_pData, int p_MsgSize);

void getIdlVersionMsg_received();
void pinModeMsg_received(byte* p_pData, int p_MsgSize);
void digitalWriteMsg_received(byte* p_pData, int p_MsgSize);
void digitalWritesMsg_received(byte* p_pData, int p_MsgSize);
void analogWriteMsg_received(byte* p_pData, int p_MsgSize);
void defineEncoderMsg_received(byte* p_pData, int p_MsgSize);
void getEncoderCounterMsg_received(byte* p_pData, int p_MsgSize);

void digitaleReadMsg_received(byte* p_pData, int p_MsgSize);
void analogReadMsg_received(byte* p_pData, int p_MsgSize);

void getSoftVersionMsg_received();
void getStatusMsg_received();
void getTypeArduinoMsg_received();

void display_encoder_info(int p_Id);
void display_encoder_info_light(int p_Id);
void display_all_Encoder_info_light();


void setup() {
  pinMode(Led, OUTPUT);

  Serial.begin(9600); // start serial for output

  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  // initialisation du tableau des encodeurs
  for (int i=0;  i<NB_ENCODER_MAX; i++)
    g_pEncoderTab[i].Id = -1;

  g_pEncoderTab[0].ptr_InterruptA = &interruptA_0;
  g_pEncoderTab[0].ptr_InterruptB = &interruptB_0;
  g_pEncoderTab[1].ptr_InterruptA = &interruptA_1;
  g_pEncoderTab[1].ptr_InterruptB = &interruptB_1;

  Serial.println("Pret");
}

void loop() {
  delay(100);
//display_all_Encoder_info_light();
}


// callback for received data
void receiveData(int p_ByteCount){
  int l_BufIndex = 0;
  
  while(Wire.available()) {
    g_pInputMsgBuf[l_BufIndex++] = Wire.read();
  }
  
  Serial.print("\n\n** receiveData : [");

  for (int i=0; i< p_ByteCount; i++)
  {
     Serial.print(" " );
     Serial.print(g_pInputMsgBuf[i] );
  }
  Serial.println(" ]");  

  // Decodage du message
  decodeMessage(g_pInputMsgBuf, p_ByteCount);
}


// callback for sending data
void sendData(){
  Serial.print("\n\n** sendData [");  

  for (int i=0; i< g_OutputMsgSize; i++)
  {
     Serial.print(" " );
     Serial.print(g_pOutputMsgBuf[i] );
  }  
  Serial.println(" ]");

  if (g_OutputMsgSize)
    Wire.write(g_pOutputMsgBuf, g_OutputMsgSize);
  g_OutputMsgSize = 0; 
}


void trace_buffer(byte* p_pMsgBuffer, int p_BufferSize)
{
  Serial.print(" bytes [" );
  for (int i=0; i< p_BufferSize; i++)
  {
     Serial.print(" " );
     Serial.print(p_pMsgBuffer[i] );
  }
  Serial.println(" ]"); 
  
}

boolean decodeMessage(byte* p_pMsgBuffer, int p_BufferSize)
{
  boolean l_Success = true;

  Serial.println("decodeMessage start");
    
  // decodage de l'identifiant du message
  Serial.print("l_MsgId = "); 
  Serial.print(p_pMsgBuffer[0]);

  switch (p_pMsgBuffer[0])
  {
    case DEFINE_ENCODER_MSG_ID:
    {
      Serial.println(" => DefineEncoderMsg");
      defineEncoderMsg_received(p_pMsgBuffer, p_BufferSize);
      break;   
    }
    case GET_ENCODER_COUNTER_MSG_ID:
    {
      Serial.println(" => GetEncoderCounterMsg");
      getEncoderCounterMsg_received(p_pMsgBuffer, p_BufferSize);
      break;   
    }
    case PIN_MODE_MSG_ID:
    {
      Serial.println(" => PinModerMsg");
      pinModeMsg_received(p_pMsgBuffer, p_BufferSize);
      break;       
    }
    case DIGITAL_WRITE_MSG_ID:
    {
      Serial.println(" => DigitalWriteMsg");
      digitalWriteMsg_received(p_pMsgBuffer, p_BufferSize);
      break;       
    }
    case DIGITAL_WRITES_MSG_ID:
    {
      Serial.println(" => DigitalWritesMsg");
      digitalWritesMsg_received(p_pMsgBuffer, p_BufferSize);
      break;       
    }      
    case ANALOG_WRITE_MSG_ID:
    {
      Serial.println(" => AnalogWriteMsg");
      analogWriteMsg_received(p_pMsgBuffer, p_BufferSize);
      break;       
    }
     case GET_IDL_VERSION_MSG_ID:
    {
      Serial.println(" => GetIdlVersionMsg");
      getIdlVersionMsg_received();
      break;   
    }
     case GET_SOFT_VERSION_MSG_ID:
    {
      Serial.println(" => GetSoftVersionMsg");
      getSoftVersionMsg_received();
      break;   
    }
    case GET_STATUS_MSG_ID:
    {
      Serial.println(" => GetStatusMsg");
      getStatusMsg_received();
      break;   
    }   
    case GET_TYPE_ARDUINO_MSG_ID:
    {
      Serial.println(" => GetArduinoTypeMsg");
      getTypeArduinoMsg_received();
      break;   
    } 
    case DIGITAL_READ_MSG_ID:
    {
      Serial.println(" => digitaleReadMsg_received");
      digitaleReadMsg_received(p_pMsgBuffer, p_BufferSize);
      break;
    }
    case ANALOG_READ_MSG_ID:
    {
      Serial.println(" => analogReadMsg_received");
      analogReadMsg_received(p_pMsgBuffer, p_BufferSize);
      break;
    }
    default :
    {
      Serial.println("   .. UNKNOWN ID !");
      l_Success = false;
      break;
    }
  }
  
  return l_Success;
}


void encoderItA(EncoderStruct* p_pEncoder)
{
  p_pEncoder->prevCptA = p_pEncoder->cptA;
  p_pEncoder->cptA = digitalRead(p_pEncoder->pinA);
  if(p_pEncoder->cptA == p_pEncoder->prevCptB) {
    p_pEncoder->tick_counter--;
  }
  else p_pEncoder->tick_counter++;
//  Serial.print("tick_counter = ");   Serial.println(p_pEncoder->tick_counter);
}
void encoderItB(EncoderStruct* p_pEncoder)
{
  p_pEncoder->prevCptB = p_pEncoder->cptB;
  p_pEncoder->cptB = digitalRead(p_pEncoder->pinB);
  if(p_pEncoder->prevCptA == p_pEncoder->cptB) {
    p_pEncoder->tick_counter++;
  }
  else p_pEncoder->tick_counter--;
//  Serial.print("tick_counter = ");   Serial.println(p_pEncoder->tick_counter);
}


void interruptA_0()
{
  Serial.println("interruptA_0");
  encoderItA(&(g_pEncoderTab[0]));
}

void interruptB_0()
{
  Serial.println("interruptB_0");
  encoderItB(&(g_pEncoderTab[0]));
}
void interruptA_1()
{
  Serial.println("interruptA_1");
  encoderItA(&(g_pEncoderTab[1]));
}

void interruptB_1()
{
  Serial.println("interruptB_1");
  encoderItB(&(g_pEncoderTab[1]));
}



void display_encoder_info(int p_Id)
{
  Serial.print("g_pEncoderTab[");Serial.print(p_Id);Serial.println("]");
  Serial.print("\tId\t:");Serial.println((g_pEncoderTab[p_Id]).Id);
  Serial.print("\tpinA\t:");Serial.println((g_pEncoderTab[p_Id]).pinA);
  Serial.print("\tpinB\t:");Serial.println((g_pEncoderTab[p_Id]).pinB);
  Serial.print("\tpinA\t:");Serial.print((g_pEncoderTab[p_Id]).pinA);  Serial.print("\tpinB\t:");Serial.println((g_pEncoderTab[p_Id]).pinB);  
  Serial.print("\tcounter\t:");Serial.println((g_pEncoderTab[p_Id]).tick_counter);
}
void display_encoder_info_light(int p_Id)
{
  Serial.print("EncoderTab[");Serial.print(p_Id);Serial.print("]");
  Serial.print("\tpinA\t:");Serial.print((g_pEncoderTab[p_Id]).pinA);  Serial.print("\tpinB\t:");Serial.print((g_pEncoderTab[p_Id]).pinB);  
  Serial.print("\tcounter\t:");Serial.println((g_pEncoderTab[p_Id]).tick_counter);
}
void display_all_Encoder()
{
  for (int i=0;  i<NB_ENCODER_MAX; i++)
  {
    if (g_pEncoderTab[i].Id != -1)    display_encoder_info(g_pEncoderTab[i].Id);
  }
}
void display_all_Encoder_info_light()
{
  for (int i=0;  i<NB_ENCODER_MAX; i++)
  {
    if (g_pEncoderTab[i].Id != -1)    display_encoder_info_light(g_pEncoderTab[i].Id);
  }
}




void defineEncoderMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_EncoderId = 0;
  Serial.println("defineEncoderMsg_received start");
  trace_buffer(p_pData, p_MsgSize); 
 
  l_EncoderId =p_pData[1];  
  g_pEncoderTab[l_EncoderId].Id = l_EncoderId ;
  g_pEncoderTab[l_EncoderId].pinA = p_pData[2];
  g_pEncoderTab[l_EncoderId].pinB = p_pData[3];
  g_pEncoderTab[l_EncoderId].tick_counter = 0;
  g_pEncoderTab[l_EncoderId].cptA = g_pEncoderTab[l_EncoderId].prevCptA = 0;
  g_pEncoderTab[l_EncoderId].cptB = g_pEncoderTab[l_EncoderId].prevCptB = 0;
  display_all_Encoder();


  pinMode(p_pData[2], INPUT_PULLUP);
  pinMode(p_pData[3], INPUT_PULLUP);
  PCintPort::attachInterrupt(p_pData[2], g_pEncoderTab[l_EncoderId].ptr_InterruptA, CHANGE);
  PCintPort::attachInterrupt(p_pData[3], g_pEncoderTab[l_EncoderId].ptr_InterruptB, CHANGE);

 //attachInterrupt(digitalPinToInterrupt(p_pData[2]), g_pEncoderTab[l_EncoderId].ptr_InterruptA, CHANGE);
  //attachInterrupt(digitalPinToInterrupt(p_pData[3]), g_pEncoderTab[l_EncoderId].ptr_InterruptB, CHANGE);
 }

#define INPUT_PIN_MODE 0
#define OUTPUT_PIN_MODE 1
#define PULLUP_PIN_MODE 2
void pinModeMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin = 0;
  byte l_Mode =0;
  Serial.println("pinModeMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  l_Pin = p_pData[1]>>2;
  l_Mode = p_pData[1] & 0x3;
  
  Serial.print("call pinMode(");Serial.print(l_Pin);
  switch( l_Mode)
  {
    case INPUT_PIN_MODE:
      l_Mode = INPUT;
      Serial.println(", INPUT)");
    break;
    case OUTPUT_PIN_MODE:
      l_Mode = OUTPUT;
      Serial.println(", OUTPUT)");
    break;
    case PULLUP_PIN_MODE:
      l_Mode = INPUT_PULLUP;
      Serial.println(", INPUT_PULLUP)");
    break;
 }
// TBD_PP gerer le cas derreur
  pinMode(l_Pin, l_Mode);
}


#define DIGITAL_LOW 0
#define DIGITAL_HIGH 1
void digitalWriteMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin = 0;
  byte l_Value =0;
  Serial.println("digitalWriteMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  l_Pin = p_pData[1]>>2;
  l_Value = p_pData[1] & 0x1;
  
  Serial.print("call digitalWrite(");Serial.print(l_Pin);
  if (l_Value==DIGITAL_LOW)
  {
    l_Value = LOW;
    Serial.println(", LOW)");
  }
  else
  {
    l_Value = HIGH;
    Serial.println(", HIGH)");
  }  

// TBD_PP gerer le cas derreur
  digitalWrite(l_Pin, l_Value);
}
void digitalWritesMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin1 = 0;
  int l_Pin2 = 0;
  byte l_Value1 =0;
  byte l_Value2 =0;
  Serial.println("digitalWritesMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  l_Pin1 = p_pData[1]>>2;
  l_Value1 = p_pData[1] & 0x1;
  l_Pin2 = p_pData[2]>>2;
  l_Value2 = p_pData[2] & 0x1;
  
  Serial.print("call digitalWrite(");Serial.print(l_Pin1);
  if (l_Value1==DIGITAL_LOW)
  {
    l_Value1 = LOW;
    Serial.println(", LOW)");
  }
  else
  {
    l_Value1 = HIGH;
    Serial.println(", HIGH)");
  }  

// TBD_PP gerer le cas derreur
  digitalWrite(l_Pin1, l_Value1);
  
  Serial.print("call digitalWrite(");Serial.print(l_Pin2);
  if (l_Value2==DIGITAL_LOW)
  {
    l_Value2 = LOW;
    Serial.println(", LOW)");
  }
  else
  {
    l_Value2 = HIGH;
    Serial.println(", HIGH)");
  }  

// TBD_PP gerer le cas derreur
  digitalWrite(l_Pin2, l_Value2);
  
}

void analogWriteMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin = 0;
  byte l_Value =0;


  Serial.println("analogWriteMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  l_Pin = p_pData[1];
  l_Value = p_pData[2];
  
 Serial.print("call analogWrite(");Serial.print(l_Pin);Serial.print(" ,");Serial.print(l_Value); Serial.println(")");
  analogWrite(l_Pin, l_Value);

}

void getEncoderCounterMsg_received(byte* p_pData, int p_MsgSize)
{
  Serial.println("getEncoderCounterMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  // il faut determiner s'il s'agit de la requete ou de la demande de lecture
  if (p_MsgSize == 2)
  {
    // il s'agit de la requete
    Serial.println(" Prepa recup compteur encodeur");
    g_EncoderCounterIdRequest = p_pData[1];
    Serial.print("EncoderId = ");Serial.println(g_EncoderCounterIdRequest);
  }
  else if (p_MsgSize == 1)
  {
    // il s'agit de la demande de recuperation des datas
    byte l_pBuffer[2];
    int l_Counter = g_pEncoderTab[g_EncoderCounterIdRequest].tick_counter;
    Serial.print("envoi compteur encodeur ");Serial.print(g_EncoderCounterIdRequest); Serial.print(" : "); Serial.println( l_Counter );
    
    l_pBuffer[0] = ENCODER_COUNTER_MSG_ID;
    l_pBuffer[1] = ((g_EncoderCounterIdRequest << 5)  );
    if (l_Counter < 0)  
    {
      l_pBuffer[1] |= 0x10;
      l_Counter *= -1;
    }
    l_pBuffer[1] |= ((l_Counter >>8) & 0x0F); 
    l_pBuffer[2] = l_Counter & 0xFF;

    prepareMsg2Send(l_pBuffer, 3);
  }
  
}

void digitaleReadMsg_received(byte* p_pData, int p_MsgSize)
{
  Serial.println("digitaleReadMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  // il faut determiner s'il s'agit de la requete ou de la demande de lecture
  if (p_MsgSize == 2)
  {
    // il s'agit de la prepa
    Serial.println("Prepa recup valeur digitale");
    g_DigitalePinReadRequest = p_pData[1];
    Serial.print("Pin = ");Serial.println(g_DigitalePinReadRequest);
  }
  else if (p_MsgSize == 1)
  {
    // il s'agit de la demande de recuperation des datas
    byte l_pBuffer[2];
    bool l_Value = digitalRead(g_DigitalePinReadRequest);
    Serial.print("envoi valeur pin ");Serial.print(g_DigitalePinReadRequest); Serial.print(" : "); Serial.println( l_Value );
    
    l_pBuffer[0] = DIGITAL_READ_VALUE_MSG_ID;
    l_pBuffer[1] = l_Value| ((g_DigitalePinReadRequest << 2)  );

    prepareMsg2Send(l_pBuffer, 2);
  } 
}

void analogReadMsg_received(byte* p_pData, int p_MsgSize)
{
  Serial.println("analogReadMsg_received start");
  trace_buffer(p_pData, p_MsgSize);

  // il faut determiner s'il s'agit de la requete ou de la demande de lecture
  if (p_MsgSize == 2)
  {
    // il s'agit de la prepa
    Serial.println("Prepa recup valeur analog");
    g_AnalogPinReadRequest = p_pData[1];
    Serial.print("Pin = ");Serial.println(g_AnalogPinReadRequest);
  }
  else if (p_MsgSize == 1)
  {
    // il s'agit de la demande de recuperation des datas
    byte l_pBuffer[3];
    int l_Value = analogRead(g_AnalogPinReadRequest);
    Serial.print("envoi valeur pin ");Serial.print(g_AnalogPinReadRequest); Serial.print(" : "); Serial.println( l_Value );
    
    l_pBuffer[0] = ANALOG_READ_VALUE_MSG_ID;
    l_pBuffer[1] = (l_Value>>8)| ((g_AnalogPinReadRequest << 2)  );
    l_pBuffer[2] = l_Value & 0xFF;

    prepareMsg2Send(l_pBuffer, 3);
  }   
}

void prepareMsg2Send(byte* p_pData, int p_MsgSize)
{
  for (int i=0; i< p_MsgSize; i++)
  {
    g_pOutputMsgBuf[i] = p_pData[i];
  }
  g_OutputMsgSize = p_MsgSize;
}


void getIdlVersionMsg_received()
{
  byte l_pBuffer[2];
  Serial.println("getIdlVersionMsg_received start");
  l_pBuffer[0] = IDL_VERSION_MSG_ID;
  l_pBuffer[1] = ((g_pIdlVersion[0] << 4) | g_pIdlVersion[1]);
  prepareMsg2Send(l_pBuffer, 2);
}
void getSoftVersionMsg_received()
{
  byte l_pBuffer[2];
  l_pBuffer[0] = SOFT_VERSION_MSG_ID;
  l_pBuffer[1] = MAJOR_SOFT_VERSION;
  l_pBuffer[1] = ((l_pBuffer[1] << 4) | MINOR_SOFT_VERSION);
  prepareMsg2Send(l_pBuffer, 2);
}

void getStatusMsg_received()
{
  byte l_pBuffer[2];
  Serial.println("getStatusMsg_received start");
  l_pBuffer[0] = STATUS_MSG_ID;
  l_pBuffer[1] =  g_Status;
  prepareMsg2Send(l_pBuffer, 2);
}

void getTypeArduinoMsg_received()
{
  byte l_pBuffer[2];
  Serial.println("getTypeArduinoMsg_received start");
  l_pBuffer[0] = TYPE_ARDUINO_MSG_ID;
  l_pBuffer[1] =  g_TypeArduino;
  prepareMsg2Send(l_pBuffer, 2);
}
