import hashlib
import struct

class ChaosCipher:
    def __init__(self, key: str):
        # 1. Key Expansion: Anahtarı kaotik parametrelere dönüştür
        # SHA-256 kullanarak deterministik ama dağıtık bir başlangıç noktası alıyoruz.
        key_hash = hashlib.sha256(key.encode()).digest()
        
        # Hash'in ilk 8 byte'ını float'a çevirip x0 (0-1 arası) yapıyoruz
        val = struct.unpack("Q", key_hash[:8])[0]
        self.x = (val % 10**8) / 10**8  # 0 < x < 1
        
        # r parametresini kaotik bölgeye (3.9 - 4.0) sabitliyoruz
        val_r = struct.unpack("Q", key_hash[8:16])[0]
        self.r = 3.9 + ((val_r % 1000) / 10000.0) 
        
        # Dinamik S-Box'ı oluştur
        self.s_box = self._generate_dynamic_sbox()
        self.inv_s_box = [0] * 256
        for i, s in enumerate(self.s_box):
            self.inv_s_box[s] = i

    def _logistic_map(self):
        """Kaotik seriden bir sonraki değeri üretir."""
        self.x = self.r * self.x * (1 - self.x)
        return self.x

    def _generate_dynamic_sbox(self):
        """Fisher-Yates algoritması + Kaos ile S-Box karıştırma."""
        sbox = list(range(256))
        # Kaos motorunu "ısındır" (Transient behavior'dan kurtulmak için)
        for _ in range(100):
            self._logistic_map()
            
        for i in range(255, 0, -1):
            chaos_val = self._logistic_map()
            j = int(chaos_val * 100000) % (i + 1)
            sbox[i], sbox[j] = sbox[j], sbox[i]
        return sbox

    def _rotate_byte(self, value, n):
        """Bitwise rotation (Dairesel kaydırma)."""
        n = n % 8
        return ((value << n) | (value >> (8 - n))) & 0xFF

    def _reverse_rotate_byte(self, value, n):
        """Ters bitwise rotation."""
        n = n % 8
        return ((value >> n) | (value << (8 - n))) & 0xFF

    def encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = bytearray()
        temp_x = self.x # Durumu sakla (her blokta devam etsin)
        
        for byte in plaintext:
            # 1. Kaotik Anahtar Akışı (Stream Key)
            chaos_val = self._logistic_map()
            key_byte = int(chaos_val * 255) & 0xFF
            
            # 2. XOR (Confusion I)
            xored = byte ^ key_byte
            
            # 3. Substitution (Confusion II - Dinamik S-Box)
            substituted = self.s_box[xored]
            
            # 4. Bitwise Rotation (Diffusion)
            # Kaos değerinin virgülden sonraki kısmına göre ne kadar döneceğine karar ver
            rot_amount = int(chaos_val * 100) % 8
            final_byte = self._rotate_byte(substituted, rot_amount)
            
            ciphertext.append(final_byte)
            
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        # Decryption için state'i sıfırlamamız gerekir veya 
        # state'i senkron tutacak bir mimari gerekir. 
        # Burada basitlik adına init'teki state'in devam ettiğini varsayıyoruz.
        # *Gerçek uygulamada IV (Initialization Vector) kullanılmalıdır.*
        
        # Not: Bu örnekte decrypt fonksiyonu, encrypt çağrısından hemen sonra
        # çağrılırsa state bozulmuş olur. Test için instance yeniden oluşturulmalı.
        pass 
        
        # Mantık encrypt'in tam tersi:
        # Reverse Rotate -> Inverse S-Box -> XOR
        
        plaintext = bytearray()
        for byte in ciphertext:
            chaos_val = self._logistic_map()
            key_byte = int(chaos_val * 255) & 0xFF
            rot_amount = int(chaos_val * 100) % 8
            
            # 1. Reverse Rotation
            rotated = self._reverse_rotate_byte(byte, rot_amount)
            
            # 2. Inverse Substitution
            inv_sub = self.inv_s_box[rotated]
            
            # 3. XOR
            original = inv_sub ^ key_byte
            plaintext.append(original)
            
        return bytes(plaintext)

# --- TEST SENARYOSU ---
if __name__ == "__main__":
    key = "GizliTechLeadSifresi_2025!"
    message = "Merhaba, bu bir kaos sifrelemesidir."
    
    # Şifreleme
    cipher_engine = ChaosCipher(key)
    encrypted_data = cipher_engine.encrypt(message.encode())
    
    print(f"Orijinal: {message}")
    print(f"Şifreli (Hex): {encrypted_data.hex()}")
    
    # Deşifreleme (State'i sıfırlamak için yeni instance açıyoruz - simülasyon)
    decrypt_engine = ChaosCipher(key)
    decrypted_data = decrypt_engine.decrypt(encrypted_data)
    
    print(f"Çözülmüş: {decrypted_data.decode()}")