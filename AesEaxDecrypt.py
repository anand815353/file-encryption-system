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
        with open(output_file_name, 'wb') as out_file:
            orig_size = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]

            while True:
                nonce, tag, chunk = [in_file.read(x) for x in (16, 16, chunk_size)]
                if len(chunk) == 0:
                    break

                cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce)

                out_file.write(cipher.decrypt_and_verify(chunk, tag))
            out_file.truncate(orig_size)


def get_key(password):
    h = SHA256.new()
    h.update(password)
    return h.digest()


class AesEaxDecryptApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    AesEaxDecryptApp().run()