from Cryptodome import Random
from Cryptodome.PublicKey import RSA
import os
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
import struct
from kivy.app import App
from kivy.uix.widget import Widget


class GuiWindow(Widget):
    def user(self, *args):
        filename = self.ids.filename_input
        filename_text = filename.text
        keyfile = self.ids.keyfile_input
        keyfile_text = keyfile.text

        try:
            encrypt(keyfile_text, filename_text)
            label = self.ids.success
            label.text = "SUCCESS"
        except Exception:
            label = self.ids.success
            label.text = "PROCESS FAILED TRY AGAIN"


def encrypt(key_file, filename):
    chunk_size = 64 * 1024
    output_file = "encrypted" + filename
    file_size = os.path.getsize(filename)
    session_key = Random.get_random_bytes(32)

    with open(key_file, 'rb') as public_key_file:
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key_file.read()))

    cipher = AES.new(key=session_key, mode=AES.MODE_EAX)

    with open(filename, 'rb') as in_file:
        with open(output_file, 'wb') as out_file:
            out_file.write(struct.pack('<Q', file_size))
            out_file.write(cipher_rsa.encrypt(session_key))

            while True:
                chunk = in_file.read(chunk_size)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                    ciphertext, tag = cipher.encrypt_and_digest(chunk)
                    [out_file.write(x) for x in (cipher.nonce, tag, ciphertext)]


#def main():
#    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")
#
#    if choice == 'E':
#        filename = input("File to encrypt: ")
#        key_file = input("Public Key File ")
#        encrypt(key_file, filename)
#        "Done."
#    elif choice == 'D':
#        #filename = input("File to decrypt: ")
#        #password = input("Password: ")
#        #decrypt(get_key(password), filename)
#        "Done."
#    else:
#        "No Option selected, closing..."

class RsaEncryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    RsaEncryptApp().run()