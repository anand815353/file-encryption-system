from Cryptodome import Random
from Cryptodome.PublicKey import RSA
import os
from kivy.app import App
from kivy.uix.widget import Widget


class GuiWindow(Widget):
    def user(self, *args):
        if (os.access("RsaPublicKey", os.F_OK) and os.access("RsaPrivateKey", os.F_OK)) is True:
            label = self.ids.success
            label.text = "Public Key and Private Key OK!"

        elif (os.access("RsaPublicKey", os.F_OK) and os.access("RsaPrivateKey", os.F_OK)) is False:
            label = self.ids.success
            label.text = "regenerating keys"
            generate_keys()
            label = self.ids.success
            label.text = "Keys Generated"

        else:
            label = self.ids.success
            label.text = "ERROR GENERATING Rsa keys!"


def generate_keys(keys_size=2048):
    public_key = "RsaPublicKey"
    private_key = "RsaPrivateKey"
    random_data = Random.get_random_bytes

    keys = RSA.generate(keys_size, random_data)

    with open(public_key, 'wb') as public_key_file:
        public_key_file.write(keys.publickey().exportKey(format='PEM'))

    with open(private_key, 'wb') as private_key_file:
        private_key_file.write(keys.exportKey(format='PEM'))


class GenerateRsaKeysApp(App):
    def build(self):
        return GuiWindow()


if __name__ == '__main__':
    GenerateRsaKeysApp().run()