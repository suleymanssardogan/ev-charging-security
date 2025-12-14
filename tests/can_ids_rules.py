"""
CAN ID Rules Module

Bu dosya sistemde 'yetkili' kabul edilen CAN ID'lerini tanımlar.
⚠️ Bilinçli zayıflık: Kaynak ECU doğrulaması veya kriptografik kontrol YOK.
(SWOT - Weakness)
"""

ALLOWED_CAN_IDS = {
    0x180: "Battery Status ECU",
    0x181: "Charging Control ECU",
    0x200: "Start Charging Command"
}
