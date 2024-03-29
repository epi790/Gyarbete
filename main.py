from PIL import Image
import numpy as np
import time
import os
import pickle
import keys
import base64
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as kivyimage
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
import kivy

kivy.require('2.2.1')

# init, load keys

shared_key = ""

if os.path.isfile("client_private_key_pickle.pk"):
    pass
else:
    file = open("client_private_key_pickle.pk", "a")
    file.close()

with open("client_private_key_pickle.pk", 'rb') as fi:
    try:
        private_key = pickle.load(fi)
        private_key = keys.private_pem_to_key(private_key)
        shared_key = pickle.load(fi)
        print(f"LOADING SHARED KEY")

    except:
        private_key = None
        pass

    if private_key != None:
        print("PRIVATE KEY FOUND")
    else:
        print("OVERRIDING KEY")
        private_key = keys.generate_private_key()


if shared_key == "":
    shared_key = keys.generate_shared_key(
        private_key, keys.public_pem_to_key(keys.publicmasterkey))
    with open("client_private_key_pickle.pk", 'wb') as fi:
        print("OPENING FILE")
        pickle.dump(keys.private_key_to_pem(private_key), fi)

        if shared_key != "":
            pickle.dump(shared_key, fi)

######################### shared key loaded guarantee #############################


class SimpleApp(App):

    def build(self):
        # Set the default image
        self.image = kivyimage(source='thatsayesfrom.png')
        self.username = "john"
        self.derivedActive = False
        def on_enter(instance):
            self.username = instance.text

        # Create two buttons
        button1 = Button(text='derived key', on_press=self.derived_clicked)
        button2 = Button(text='public key', on_press=self.change_image2)

        # Create text input
        textinput = TextInput(text='name', multiline=False,
                              size_hint=(0.2, None), height=30)
        textinput.bind(on_text_validate=on_enter)

        # Create a layout and add widgets
        layout = GridLayout(cols=1, spacing=10, size_hint=(
            None, None), width=500, height=500)
        button_layout = GridLayout(
            cols=2, spacing=10, size_hint_y=None, height=50)

        # Add buttons to the button layout
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)

        # Add the button layout and the image to the main layout
        layout.add_widget(button_layout)
        layout.add_widget(self.image),
        layout.add_widget(textinput)
        
        Clock.schedule_interval(self.update_derived, 1)

        return layout
    

    def change_image1(self=None, instance=None):

        derived_key = keys.derive_new_key_from_time(shared_key)
        message = f"{derived_key}, {self.username}".encode()
        print(message)
        qr = keys.generate_qr_from_key(base64.b64encode(message))
        qr.save("derived_key.png")

        # Convert the QR code to a texture and update the Image widget
        texture = self.pil_image_to_texture(qr)

        self.image.source = "derived_key.png"
        self.image.reload()

    def derived_clicked(self, instance):
            self.derivedActive = True
            self.change_image1()
    def update_derived(self, instance):
        if self.derivedActive:
            self.change_image1()

    def change_image2(self, instance):
        self.derivedActive = False
        qr = (keys.generate_qr_from_key(
            f"{keys.public_key_to_pem(private_key.public_key()).decode()},{self.username}"))
        qr.save("public.png")
        self.image.source = "public.png"
        self.image.reload()

    def pil_image_to_texture(self, pil_image):
        # Convert PIL image to numpy array
        np_image = np.array(pil_image)

        # Ensure the array has three dimensions (height, width, channels)
        if len(np_image.shape) == 2:
            np_image = np_image[:, :, np.newaxis]

        # Convert single-channel images to RGB
        if np_image.shape[2] == 1:
            np_image = np.concatenate([np_image] * 3, axis=2)

        # Create a Kivy Texture
        texture = Texture.create(
            size=(np_image.shape[1], np_image.shape[0]), colorfmt='rgb')

        # Blit the buffer into the texture
        texture.blit_buffer(np_image.tobytes(),
                            colorfmt='rgb', bufferfmt='ubyte')

        return texture


if __name__ == '__main__':
    SimpleApp().run()
