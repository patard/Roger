#include "enICCma.h"
#include <Wire.h>


#define SLAVE_ADDRESS 0x05
#define NB_ENCODER_MAX 2

#define BUFFER_SIZE_MAX 4

byte g_Status = 3;

byte g_pInputMsgBuf[BUFFER_SIZE_MAX];
byte g_pOutputMsgBuf[BUFFER_SIZE_MAX];
int g_OutputMsgSize = 0;

byte g_EncoderCounterIdRequest = 0;
byte g_DigitalePinReadRequest = 0;
byte g_AnalogPinReadRequest = 0;

typedef struct EncoderStruct
{
  int Id;
  int pinA;
  int pinB;
  int tick_counter;
  void (*ptr_InterruptA) (void); // callback associé au capteur A
  void (*ptr_InterruptB) (void); // callback associé au capteur B
  byte cptA, prevCptA; // Compteurs d'interruption A
  byte cptB, prevCptB; // Compteurs d'interruption B
} EncoderStruct;

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

// Remplit le buffer qui sera utilise lors de l'envoi de donnees sur le bus I2C : sendData()
void prepareMsg2Send(byte* p_pData, int p_MsgSize)
{
  for (int i = 0; i < p_MsgSize; i++)
  {
    g_pOutputMsgBuf[i] = p_pData[i];
  }
  g_OutputMsgSize = p_MsgSize;
}


void setup() {
  Serial.begin(57600); // start serial for output

  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  // initialisation du tableau des encodeurs
  for (int i = 0;  i < NB_ENCODER_MAX; i++)
    g_pEncoderTab[i].Id = -1;

  g_pEncoderTab[0].ptr_InterruptA = &interruptA_0;
  g_pEncoderTab[0].ptr_InterruptB = &interruptB_0;
  g_pEncoderTab[1].ptr_InterruptA = &interruptA_1;
  g_pEncoderTab[1].ptr_InterruptB = &interruptB_1;

  Serial.println("Pret");
}


// ============================== //
// boucle principale
// ============================== //
void loop() {
  delay(2000);
}


// ============================== //
// callback for received data
// ============================== //
void receiveData(int p_ByteCount) {
  int l_BufIndex = 0;

  while (Wire.available()) {
    g_pInputMsgBuf[l_BufIndex++] = Wire.read();
  }

  // Decodage du message
  TreatMsgReception(g_pInputMsgBuf, p_ByteCount);
}


// ============================== //
// callback for sending data
// ============================== //
void sendData() {
  if (g_OutputMsgSize)
    Wire.write(g_pOutputMsgBuf, g_OutputMsgSize);
  g_OutputMsgSize = 0;
}




void encoderItA(EncoderStruct* p_pEncoder)
{
  p_pEncoder->prevCptA = p_pEncoder->cptA;
  p_pEncoder->cptA = digitalRead(p_pEncoder->pinA);
  if (p_pEncoder->cptA == p_pEncoder->prevCptB) {
    p_pEncoder->tick_counter--;
  }
  else p_pEncoder->tick_counter++;
}

void encoderItB(EncoderStruct* p_pEncoder)
{
  p_pEncoder->prevCptB = p_pEncoder->cptB;
  p_pEncoder->cptB = digitalRead(p_pEncoder->pinB);
  if (p_pEncoder->prevCptA == p_pEncoder->cptB) {
    p_pEncoder->tick_counter++;
  }
  else p_pEncoder->tick_counter--;
}


void interruptA_0()
{
  encoderItA(&(g_pEncoderTab[0]));
}
void interruptB_0()
{
  encoderItB(&(g_pEncoderTab[0]));
}
void interruptA_1()
{
  encoderItA(&(g_pEncoderTab[1]));
}
void interruptB_1()
{
  encoderItB(&(g_pEncoderTab[1]));
}



void defineEncoderMsg_received(byte* p_pData, int p_MsgSize)
{
  // on recuepre l'identifiant de l'encodeur
  int l_EncoderId = p_pData[1];

  g_pEncoderTab[l_EncoderId].Id = l_EncoderId ;
  g_pEncoderTab[l_EncoderId].pinA = p_pData[2];
  g_pEncoderTab[l_EncoderId].pinB = p_pData[3];
  g_pEncoderTab[l_EncoderId].tick_counter = 0;
  g_pEncoderTab[l_EncoderId].cptA = g_pEncoderTab[l_EncoderId].prevCptA = 0;
  g_pEncoderTab[l_EncoderId].cptB = g_pEncoderTab[l_EncoderId].prevCptB = 0;

  pinMode(p_pData[2], INPUT_PULLUP);
  pinMode(p_pData[3], INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(p_pData[2]), g_pEncoderTab[l_EncoderId].ptr_InterruptA, CHANGE);
  attachInterrupt(digitalPinToInterrupt(p_pData[3]), g_pEncoderTab[l_EncoderId].ptr_InterruptB, CHANGE);
  Serial.print("attachInterrupt "); Serial.println(p_pData[2]);
  Serial.print("attachInterrupt "); Serial.println(p_pData[3]);
}



void getEncoderCounterMsg_received(byte* p_pData, int p_MsgSize)
{
  // il faut determiner s'il s'agit de la requete ou de la demande de lecture
  if (p_MsgSize == 2)
  {
    // il s'agit de la requete
    g_EncoderCounterIdRequest = p_pData[1];
  }
  else if (p_MsgSize == 1)
  {
    // il s'agit de la demande de recuperation des datas
    byte l_pBuffer[2];
    int l_Counter = g_pEncoderTab[g_EncoderCounterIdRequest].tick_counter;
    l_pBuffer[0] = ENCODER_COUNTER_MSG_ID;
    l_pBuffer[1] = ((g_EncoderCounterIdRequest << 5)  );
    if (l_Counter < 0)
    {
      l_pBuffer[1] |= 0x10;
      l_Counter *= -1;
    }
    l_pBuffer[1] |= ((l_Counter >> 8) & 0x0F);
    l_pBuffer[2] = l_Counter & 0xFF;

    prepareMsg2Send(l_pBuffer, 3);
    g_pEncoderTab[g_EncoderCounterIdRequest].tick_counter = 0;
  }
}

void pinModeMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin;
  char l_Mode;
  if (enICCma::decodePinModeMsg((char*)p_pData,  p_MsgSize, &l_Pin, &l_Mode))
  {
    switch ( l_Mode)
    {
      case INPUT_PIN_MODE:
        l_Mode = INPUT;
        break;
      case OUTPUT_PIN_MODE:
        l_Mode = OUTPUT;
        break;
      case PULLUP_PIN_MODE:
        l_Mode = INPUT_PULLUP;
        break;
    }

    pinMode(l_Pin, l_Mode);
  }
  else
  {
    // TBD traiter le cas d'erreur
  }
}


#define DIGITAL_LOW 0
#define DIGITAL_HIGH 1
void digitalWriteMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin = p_pData[1] >> 2;
  byte l_Value = p_pData[1] & 0x1;

  if (l_Value == DIGITAL_LOW)
    l_Value = LOW;
  else
    l_Value = HIGH;

  digitalWrite(l_Pin, l_Value);
}


void digitalWritesMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin1 = p_pData[1] >> 2;
  int l_Pin2 = p_pData[2] >> 2;
  byte l_Value1 = p_pData[1] & 0x1;
  byte l_Value2 = p_pData[2] & 0x1;

  if (l_Value1 == DIGITAL_LOW)
    l_Value1 = LOW;
  else
    l_Value1 = HIGH;

  digitalWrite(l_Pin1, l_Value1);

  if (l_Value2 == DIGITAL_LOW)
    l_Value2 = LOW;
  else
    l_Value2 = HIGH;

  digitalWrite(l_Pin2, l_Value2);
}

// ----------------------------------------
// traitement du message AnalogWrite
// ----------------------------------------
void analogWriteMsg_received(byte* p_pData, int p_MsgSize)
{
  int l_Pin;
  char l_Value;
  if (enICCma::decodeAnalogWriteMsg((char*)p_pData, p_MsgSize,
                                &l_Pin, &l_Value))
  {
    analogWrite(l_Pin, l_Value);
  }
  else
  {
    // TBD traiter le cas d'erreur
  }
}


void digitaleReadMsg_received(byte* p_pData, int p_MsgSize)
{
  // il faut determiner s'il s'agit de la requete ou de la demande de lecture
  if (p_MsgSize == 2)
  {
    // il s'agit de la prepa
    g_DigitalePinReadRequest = p_pData[1];
  }
  else if (p_MsgSize == 1)
  {
    // il s'agit de la demande de recuperation des datas
    byte l_pBuffer[2];
    bool l_Value = digitalRead(g_DigitalePinReadRequest);
    l_pBuffer[0] = DIGITAL_READ_VALUE_MSG_ID;
    l_pBuffer[1] = l_Value | ((g_DigitalePinReadRequest << 2)  );

    prepareMsg2Send(l_pBuffer, 2);
  }
}

void analogReadMsg_received(byte* p_pData, int p_MsgSize)
{
  // il faut determiner s'il s'agit de la requete ou de la demande de lecture
  if (p_MsgSize == 2)
  {
    // il s'agit de la prepa
    g_AnalogPinReadRequest = p_pData[1];
  }
  else if (p_MsgSize == 1)
  {
    // il s'agit de la demande de recuperation des datas
    byte l_pBuffer[3];
    int l_Value = analogRead(g_AnalogPinReadRequest);
    l_pBuffer[0] = ANALOG_READ_VALUE_MSG_ID;
    l_pBuffer[1] = (l_Value >> 8) | ((g_AnalogPinReadRequest << 2)  );
    l_pBuffer[2] = l_Value & 0xFF;

    prepareMsg2Send(l_pBuffer, 3);
  }
}




// ----------------------------------------
// traitement de la requete GetIdlVersion
// ----------------------------------------
void getIdlVersionMsg_received()
{
  /*
  byte l_pBuffer[2];
  l_pBuffer[0] = IDL_VERSION_MSG_ID;
  l_pBuffer[1] = MAJOR_IDL_VERSION;
  l_pBuffer[1] = ((l_pBuffer[1] << 4) | MINOR_IDL_VERSION);
  prepareMsg2Send(l_pBuffer, 2);
  */
  char* l_pBuffer = NULL;
  int l_MsgSize = 0;
  enICCma::encodeIdlVersionMsg(&l_pBuffer, &l_MsgSize);
  prepareMsg2Send((byte*)(*l_pBuffer), l_MsgSize);
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
  l_pBuffer[0] = STATUS_MSG_ID;
  l_pBuffer[1] =  g_Status;
  prepareMsg2Send(l_pBuffer, 2);
}

void getTypeArduinoMsg_received()
{
  byte l_pBuffer[2];
  l_pBuffer[0] = TYPE_ARDUINO_MSG_ID;
  l_pBuffer[1] = TYPE_ARDUINO;
  prepareMsg2Send(l_pBuffer, 2);
}




void TreatMsgReception(byte* p_pMsgBuffer,
                   int p_BufferSize)
{
  switch (p_pMsgBuffer[0])
  {
    case DEFINE_ENCODER_MSG_ID:
      {
        defineEncoderMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case GET_ENCODER_COUNTER_MSG_ID:
      {
        getEncoderCounterMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case PIN_MODE_MSG_ID:
      {
        pinModeMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case DIGITAL_WRITE_MSG_ID:
      {
        digitalWriteMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case DIGITAL_WRITES_MSG_ID:
      {
        digitalWritesMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case ANALOG_WRITE_MSG_ID:
      {
        analogWriteMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case GET_IDL_VERSION_MSG_ID:
      {
        getIdlVersionMsg_received();
        break;
      }
    case GET_SOFT_VERSION_MSG_ID:
      {
        getSoftVersionMsg_received();
        break;
      }
    case GET_STATUS_MSG_ID:
      {
        getStatusMsg_received();
        break;
      }
    case GET_TYPE_ARDUINO_MSG_ID:
      {
        getTypeArduinoMsg_received();
        break;
      }
    case DIGITAL_READ_MSG_ID:
      {
        digitaleReadMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    case ANALOG_READ_MSG_ID:
      {
        analogReadMsg_received(p_pMsgBuffer, p_BufferSize);
        break;
      }
    default :
      {
        Serial.println("   .. UNKNOWN ID !");
        break;
      }
  }
}
