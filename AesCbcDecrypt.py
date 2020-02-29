from Cryptodome.Cipher import AES
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
            decrypt(get_key(p2b(password_text)), filename_text)
            label = self.ids.success
            label.text = "SUCCESS"
        except Exception:
            label = self.ids.success
            label.text = "PROCESS FAILED TRY AGAIN"


def p2b(password):
    password_in_bytes = str.encode(password)
    return password_in_bytes


def decrypt(key, filename):
    chunk_size = 64 * 1024
    output_file_name = filename[9:]

    with open(filename, 'rb') as in_file:
        orig_size = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]
        iv = in_file.read(16)

        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

        with open(output_file_name, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)

                if len(chunk) == 0:
                    break

                out_file.write(cipher.decrypt(chunk))
            out_file.truncate(orig_size)


def get_key(password):
    h = SHA256.new()
    h.update(password)
    return h.digest()


class AesCbcDecryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    AesCbcDecryptApp().run()
