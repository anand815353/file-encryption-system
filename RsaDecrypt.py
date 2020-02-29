import struct
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from kivy.app import App
from kivy.uix.widget import Widget


class GuiWindow(Widget):
    def user(self, *args):
        filename = self.ids.filename_input
        filename_text = filename.text
        keyfile = self.ids.keyfile_input
        keyfile_text = keyfile.text

        try:
            decrypt(keyfile_text, filename_text)
            label = self.ids.success
            label.text = "SUCCESS"
        except Exception:
            label = self.ids.success
            label.text = "PROCESS FAILED TRY AGAIN"


def decrypt(key_file, filename):
    chunk_size = 64 * 1024
    output_file_name = filename[9:]

    with open(key_file, 'rb') as private_key_file:
        private_key = RSA.import_key(private_key_file.read())
    cipher_rsa = PKCS1_OAEP.new(private_key)

    with open(filename, 'rb') as in_file:
        with open(output_file_name, 'wb') as out_file:
            orig_size = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]
            session_key = cipher_rsa.decrypt(in_file.read(private_key.size_in_bytes()))

            while True:
                nonce, tag, chunk = [in_file.read(x) for x in (16, 16, chunk_size)]
                if len(chunk) == 0:
                    break
                cipher_aes = AES.new(key=session_key, mode=AES.MODE_EAX, nonce=nonce)

                out_file.write(cipher_aes.decrypt_and_verify(chunk, tag))
            out_file.truncate(orig_size)


#def main():
#    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")
#
#    if choice == 'E':
#        #filename = input("File to encrypt: ")
#        #password = input("Password: ")
#        #password_in_bytes = str.encode(password)
#        #encrypt(get_key(password_in_bytes), filename)
#        "Done."
#    elif choice == 'D':
#        filename = input("File to decrypt: ")
#        key_file = input("Private key file ")
#        decrypt(key_file, filename)
#        "Done."
#    else:
#        "No Option selected, closing..."

class RsaDecryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    RsaDecryptApp().run()