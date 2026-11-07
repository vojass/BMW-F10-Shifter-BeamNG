#include <SPI.h>
#include <mcp_can.h>

#define CAN_CS 10
#define CAN_INT 2

MCP_CAN CAN0(CAN_CS);

// =========================
// CAN ID
// =========================
#define GWS_POSITION_ID 0x197
#define GWS_DISPLAY_ID  0x3FD

// =========================
// POZICE PÁKY
// =========================
#define POS_R   0x2F

#define POS_N1  0x1F
#define POS_N2  0x3F

#define POS_D   0x4F

#define POS_MS_UP      0x5F
#define POS_MS_DOWN    0x6F
#define POS_MS_CENTER  0x7F

// =========================
// DISPLAY
// =========================
#define DISPLAY_P 0x20
#define DISPLAY_R 0x40
#define DISPLAY_N 0x60
#define DISPLAY_D 0x81

// =========================
// PROMĚNNÉ
// =========================
byte displayValue = DISPLAY_P;
byte counter = 0;

bool inDrive = false;
bool inMS = false;

byte lastPosition = 0xFF;
bool lastP = false;

unsigned long lastNeutral = 0;

// =========================
// CRC8
// =========================
byte crc8(byte *data, byte len) {

  byte crc = 0x00;

  for (byte i = 0; i < len; i++) {

    crc ^= data[i];

    for (byte j = 0; j < 8; j++) {

      if (crc & 0x80)
        crc = (crc << 1) ^ 0x1D;
      else
        crc <<= 1;
    }
  }

  return crc ^ 0x70;
}

// =========================
// ODESLÁNÍ DISPLAY
// =========================
void sendDisplay() {

  byte frame[5];

  frame[1] = counter;
  frame[2] = displayValue;
  frame[3] = 0x00;
  frame[4] = 0x00;

  frame[0] = crc8(&frame[1], 4);

  CAN0.sendMsgBuf(GWS_DISPLAY_ID, 0, 5, frame);

  counter++;

  if (counter > 0x0E)
    counter = 0;
}

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(115200);

  while (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) != CAN_OK) {
    Serial.println("CAN chyba...");
    delay(500);
  }

  CAN0.setMode(MCP_NORMAL);

  pinMode(CAN_INT, INPUT);

  Serial.println("GWS CAN START");
}

// =========================
// LOOP
// =========================
void loop() {

  // ==========================================
  // ČTENÍ GWS
  // ==========================================

  if (CAN0.checkReceive() == CAN_MSGAVAIL) {

    unsigned long id;
    byte len;
    byte data[8];

    CAN0.readMsgBuf(&id, &len, data);

    if (id == GWS_POSITION_ID) {

      byte position = data[2];

      // ======================================
      // P
      // ======================================

      bool pPressed = (data[3] == 0xD5);

      if (pPressed && !lastP) {

        displayValue = DISPLAY_P;

        inDrive = false;
        inMS = false;

        Serial.println("P");
      }

      lastP = pPressed;

      // ======================================
      // R
      // ======================================

      if (position == POS_R && lastPosition != POS_R) {

        displayValue = DISPLAY_R;

        inDrive = false;
        inMS = false;

        Serial.println("R");
      }

      // ======================================
      // N
      // ======================================

      if (
        (position == POS_N1 || position == POS_N2) &&
        (millis() - lastNeutral >= 3000)
      ) {

        lastNeutral = millis();

        displayValue = DISPLAY_N;

        inDrive = false;
        inMS = false;

        Serial.println("N");
      }

      // ======================================
      // D
      // ======================================

      if (position == POS_D && lastPosition != POS_D) {

        displayValue = DISPLAY_D;

        inDrive = true;
        inMS = false;

        Serial.println("D");
      }

      // ======================================
      // M/S STŘED
      // ======================================

      if (
        position == POS_MS_CENTER &&
        lastPosition != POS_MS_CENTER
      ) {

        if (inDrive) {

          inMS = true;

          displayValue = DISPLAY_D;

          Serial.println("MS");
        }
      }

      // ======================================
      // M+ = K SOBĚ
      // ======================================

      if (
        position == POS_MS_DOWN &&
        lastPosition != POS_MS_DOWN
      ) {

        if (inMS) {

          Serial.println("UP");
        }
      }

      // ======================================
      // M- = OD SEBE
      // ======================================

      if (
        position == POS_MS_UP &&
        lastPosition != POS_MS_UP
      ) {

        if (inMS) {

          Serial.println("DOWN");
        }
      }

      // ======================================
      // ULOŽENÍ POZICE
      // ======================================

      lastPosition = position;
    }
  }

  // ==========================================
  // 3FD POSÍLÁME BEZ ČEKÁNÍ
  // ==========================================

  sendDisplay();
}
