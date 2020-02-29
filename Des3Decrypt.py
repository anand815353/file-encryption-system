from Cryptodome.Cipher import DES3
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
            decrypt(keyfile_text, filename_text)
            label = self.ids.success
            label.text = "SUCCESS"
        except Exception:
            label = self.ids.success
            label.text = "PROCESS FAILED TRY AGAIN"


def decrypt(in_key_file, filename):
    chunk_size = 64 * 1024
    output_file_name = filename[9:]

    with open(in_key_file, 'rb') as key_file:
        key = key_file.read(16)

    with open(filename, 'rb') as in_file:
        orig_size = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]
        iv = in_file.read(8)

        cipher = DES3.new(key=key, mode=DES3.MODE_CBC, iv=iv)

        with open(output_file_name, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)

                if len(chunk) == 0:
                    break

                out_file.write(cipher.decrypt(chunk))
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
#        key_file = input("key file: ")
#        decrypt(key_file, filename)
#        "Done."
#    else:
#        "No Option selected, closing..."

class Des3DecryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    Des3DecryptApp().run()