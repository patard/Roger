/**
 * @file enICCma.cpp
*/


#include "enICCma.h"


#define IDL_VERSION_BUFFER_SIZE 2
char g_pIdlVersionBuffer[IDL_VERSION_BUFFER_SIZE];


/**
*  @param [in] p_pData : buffer contenant le message a decoder
*  @param [in] p_MsgSize : taille du message a decoder
*  @param [out] p_pPin : pointeur sur la valeur de pin decodee
*  @param [out] p_pMode : pointeur sur la valeur de mode decodee
*                (Input/Output/Pullup)
*
*  @return true si decodage reussi, false sinon
*/
bool enICCma::decodePinModeMsg(char* p_pData, 
				int p_MsgSize, 
				int* p_pPin, 
				char* p_pMode)
{
  bool l_success = true;

  *p_pPin = p_pData[1] >> 2;
  
  (*p_pMode) = p_pData[1] & 0x3;
  if ( ((*p_pMode) != INPUT_PIN_MODE) &&
	((*p_pMode) != OUTPUT_PIN_MODE) &&
	((*p_pMode) != PULLUP_PIN_MODE) )
   l_success = false;  

  return l_success;
}
///** @htmlinclude DataStructure.txt */

/**
*  @brief Decode le message AnalogWrite
*  @param [in] p_pData : buffer contenant le message a decoder
*  @param [in] p_MsgSize : taille du message a decoder
*  @param [out] p_pPin : pointeur sur la valeur de pin decodee
*  @param [out] p_pMode : pointeur sur la valeur de de mode decodee
*                (Input/Output/Pullup)
*
*  @return true si decodage reussi, false sinon
*/
bool enICCma::decodeAnalogWriteMsg(char* p_pData, 
				int p_MsgSize, 
				int* p_pPin, 
				char* p_pValue)
{
  *p_pPin = p_pData[1];
  *p_pValue= p_pData[2];
  return true;
}




/**
 * @page IDL_VERSION
 * # Message IDL_VERSION
 * - Registre : __0xFC__
 * - Attributs :
 *   -# Major : Entier non signé sur 4 bits [0;15]
 *   -# Minor : Entier non signé sur 4 bits [0;15]
 *
 * \n
<table >
<tr style="border:2px solid black">
	<td style="border:2px solid black"> B7-B0
	<td>B7<td>B6<td>B5<td>B4<td>B3<td>B2<td>B1<td>B0
<tr style="border:2px solid black">
	<td style="border:2px solid black">0xFC
	<td colspan="4"  align="center">Major
	<td colspan="4"  align="center">Minor
</table>
* \n
* ### Fonctions associées :
* @ref enICCma::encodeIdlVersionMsg pour l'encodage dans un buffer.\n
* @ref enICCma::decodeIdlVersionMsg pour decoder un buffer.
*/




/**
* Voir la page \ref IDL_VERSION pour la définition de la structure de données.
*/
void enICCma::encodeIdlVersionMsg(char** p_pData, int* p_pMsgSize)
{
  g_pIdlVersionBuffer[0] = IDL_VERSION_MSG_ID;
  g_pIdlVersionBuffer[1] = MAJOR_IDL_VERSION;
  g_pIdlVersionBuffer[1] = ((g_pIdlVersionBuffer[1] << 4) | MINOR_IDL_VERSION);
  (*p_pMsgSize) = IDL_VERSION_BUFFER_SIZE;
  p_pData = (char**)(&(g_pIdlVersionBuffer));
}

