import os
from Cryptodome.Cipher import DES3
from Cryptodome import Random
import struct
from kivy.app import App
from kivy.uix.widget import Widget


class GuiWindow(Widget):
    def user(self, *args):
        filename = self.ids.filename_input
        filename_text = filename.text

        try:
            encrypt(get_random_key(), filename_text)
            label = self.ids.success
            label.text = "SUCCESS AND KEY FILE GENERATED"
        except Exception:
            label = self.ids.success
            label.text = "PROCESS FAILED TRY AGAIN"


def encrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = "encrypted" + filename
    file_size = os.path.getsize(filename)

    iv = Random.new().read(DES3.block_size)

    cipher = DES3.new(key=key, mode=DES3.MODE_CBC, iv=iv)

    with open(filename, 'rb') as in_file:
        with open(output_file, 'wb') as out_file:
            out_file.write(struct.pack('<Q', file_size))
            out_file.write(iv)

            while True:
                chunk = in_file.read(chunk_size)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 8 != 0:
                    chunk += b' ' * (8 - len(chunk) % 8)
                out_file.write(cipher.encrypt(chunk))

    output_key = filename + '.key'

    with open(output_key, 'wb') as out_key:
        out_key.write(key)


def get_random_key():
    key = os.urandom(16)
    return key


class Des3EncryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    Des3EncryptApp().run()
