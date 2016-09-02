/**
 * @file enICCma.h
 * @version 0.1
*/


#ifndef enICCma_H_
#define enICCma_H_

#define MAJOR_SOFT_VERSION 0 /**< Composante majeur du numéro de version */
#define MINOR_SOFT_VERSION 6

#define MAJOR_IDL_VERSION 0
#define MINOR_IDL_VERSION 2

#define TYPE_ARDUINO 0x12

#define PIN_MODE_MSG_ID  0x01
#define DIGITAL_READ_MSG_ID    0x02
#define DIGITAL_WRITE_MSG_ID   0x03
#define DIGITAL_WRITES_MSG_ID  0x04
#define ANALOG_READ_MSG_ID     0x05
#define ANALOG_WRITE_MSG_ID    0x06
#define DEFINE_ENCODER_MSG_ID  0x07
#define GET_ENCODER_COUNTER_MSG_ID 0x08
#define GET_SOFT_VERSION_MSG_ID 0x09
#define GET_STATUS_MSG_ID 0x0A
#define GET_TYPE_ARDUINO_MSG_ID 0x0B
#define GET_IDL_VERSION_MSG_ID 0x0C

#define DIGITAL_READ_VALUE_MSG_ID  0xF2
#define ANALOG_READ_VALUE_MSG_ID   0xF5
#define ENCODER_COUNTER_MSG_ID     0xF8
#define STATUS_MSG_ID 0xFA
#define TYPE_ARDUINO_MSG_ID 0xFB
#define IDL_VERSION_MSG_ID  0xFC
#define SOFT_VERSION_MSG_ID 0xF9

// mode deu message PinMode
#define INPUT_PIN_MODE 0
#define OUTPUT_PIN_MODE 1
#define PULLUP_PIN_MODE 2



/**
| Right | Center | Left  |
| ----: | :----: | :---- |
| 10    | 10     | 10    |
| 1000  | 1000   | 1000  |

 */

/**
\dot
digraph structs {
node [shape=record, fontname = "courier"];
struct [label="{b7-b0|0xF8 } | { {b7|b6|b5}|IdEncoder}| { {b4|b3|b2|b1|b0|b7|b6|b5|b4|b3|b2|b1|b0}|Value}"];
}
\enddot
*/

/**
\dot
digraph structs {
node [shape=record];
struct [fontname = "courier",label="{b7-b0|0xF8 } | { {b7|b6|b5}|IdEncoder}| { {b4|b3|b2|b1|b0|b7|b6|b5|b4|b3|b2|b1|b0}|Value}"];
}
\enddot
*/

/**
\msc
a [label="Maitre"],b [label="Esclave"];
---  [label="envoi de donnees"];
a->b [label="setData(...)"];
b=>b [label="register data"];
...;
---  [label="demande de donnees"];
a->b [label="data resquest(...)"];
b=>b [label="recover data"];
b->a [label="requested data"];
\endmsc
*/

class enICCma
{
   public:
  /** @brief Decode le message PinMode */
  static bool decodePinModeMsg(char* p_pData, int p_MsgSize, int* p_pPin, char* p_pMode);

  /** @brief Decode le message AnalogWrite*/
  static bool decodeAnalogWriteMsg(char* p_pData, int p_MsgSize, int* p_pPin, char* p_pValue);

  /** @brief Encode le message IdlVersion*/
  static void encodeIdlVersionMsg(char** p_pData, int* p_pMsgSize);


};

//extern enICCma _enICCma;

#endif // enICCma_H_

