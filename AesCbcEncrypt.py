import os
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Hash import SHA256
import struct
from kivy.app import App
from kivy.uix.widget import Widget


class GuiWindow(Widget):
    def user(self, *args):
        filename = self.ids.filename_input
        filename_text = filename.text
        password = self.ids.password_input
        password_text = password.text
        try:
            encrypt(get_key(p2b(password_text)), filename_text)
            label = self.ids.success
            label.text = "SUCCESS"
        except Exception:
            label = self.ids.success
            label.text = "PROCESS FAILED TRY AGAIN"


def p2b(password):
    password_in_bytes = str.encode(password)
    return password_in_bytes


def encrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = "encrypted" + filename
    file_size = os.path.getsize(filename)

    iv = Random.new().read(AES.block_size)

    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

    with open(filename, 'rb') as in_file:
        with open(output_file, 'wb') as out_file:
            out_file.write(struct.pack('<Q', file_size))
            out_file.write(iv)

            while True:
                chunk = in_file.read(chunk_size)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                out_file.write(cipher.encrypt(chunk))


def get_key(password):
    h = SHA256.new()
    h.update(password)
    return h.digest()


class AesCbcEncryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    AesCbcEncryptApp().run()
