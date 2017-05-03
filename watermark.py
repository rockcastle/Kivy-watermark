import re
from PIL import Image, ImageDraw, ImageFont
from kivy.adapters.listadapter import ListAdapter
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListItemButton, ListView

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup

from kivy.core.window import Window
# Window.size = (400, 300)
import os

Builder.load_file('watermark.kv')


class Watermark(Screen):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Watermark, self).__init__(**kwargs)
        print(Window.size)
        # init and add grid layer
        # self.cols = 2
        # self.layout = GridLayout(cols=self.cols)
        # self.add_widget(self.layout)
        # function to set the buttons based on the current window size
        # self.set_content(Window.width, Window.height)
        # bind above function to get called whenever the window resizes
        # Window.bind(on_resize=self.set_content)
        # self._popup = ObjectProperty(None)


    def load(self, path, filename):
        try:
            if not filename == []:
                print(os.path.join(os.path.realpath(path), filename[0]))
                self.text_input.text = ""
                self.save_input.text = ""
                self.text_input.text = str(os.path.join(os.path.realpath(path), filename[0]))
                print(str(os.path.realpath(path))+"/wmarked_"+str(filename[0]))
                self.save_input.text = str(os.path.realpath(path))+"/wmarked_"+str(filename[0])
                self.img.source = self.text_input.text
                # self.img2.source = self.text_input.text
                print(self.img.image_ratio)
            else:
                print(os.path.realpath(path))
                self.text_input.text = ""
                self.save_input.text = ""
                self.text_input.text = str(os.path.realpath(path))
                self.save_input.text = str(os.path.realpath(path))
                self.load_images(self)

            self.dismiss_popup()
        except Exception as ex:
            pass

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def wmark_text_clear(self):
        self.wmark.text = ""

    def watermark_work(self, filename,wmark_text,save_img):
        try:
            filters = ['jpg', 'png', 'jpeg', 'JPG', 'PNG']
            filename = self.text_input.text
            for i in filters:
                if re.search(i,filename):
                    main = Image.open(filename)
                else:
                    for k in self.d:
                        filename+="/"+k
                        main=Image.open(filename)
                        filename=""

            # Open the original image
            #main = Image.open(filename)

            # Create a new image for the watermark with an alpha layer (RGBA)
            #  the same size as the original image
            watermark = Image.new("RGBA", main.size)
            # Get an ImageDraw object so we can draw on the image
            waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
            # Place the text at (10, 10) in the upper left corner. Text will be white.

            font_path = "Copperplate.ttc"
            font = ImageFont.truetype(font_path, 250)

            im = Image.open(filename)
            width, height = im.size
            print(height)
            print(width)
            waterdraw.text((width / 2, height / 2), wmark_text, fill=(255, 255, 255, 128), font=font)

            # Get the watermark image as grayscale and fade the image
            # See <http://www.pythonware.com/library/pil/handbook/image.htm#Image.point>
            #  for information on the point() function
            # Note that the second parameter we give to the min function determines
            #  how faded the image will be. That number is in the range [0, 256],
            #  where 0 is black and 256 is white. A good value for fading our white
            #  text is in the range [100, 200].
            watermask = watermark.convert("L").point(lambda x: min(x, 255))
            # Apply this mask to the watermark image, using the alpha filter to
            #  make it transparent
            watermark.putalpha(watermask)

            # Paste the watermark (with alpha layer) onto the original image and save it
            main.paste(watermark, (0, 0), watermark)
            main.save(save_img)
        except Exception as ex:
            print(str(ex))

    def load_images(self,adapter, *args):
        try:
            self.d = []
            self.lview.item_strings.clear()
            filters= ['jpg', 'png', 'jpeg', 'JPG', 'PNG']
            data =[{"text":str(i)} for i in os.listdir(self.text_input.text) for k in filters if re.search(k,i)]
            args_converter = lambda row_index, rec: {'text': rec['text'], 'size_hint_y': None,'height': 30}
            self.list_adapter = ListAdapter(data=data, args_converter=args_converter, cls=ListItemButton, selection_mode='single', allow_empty_selection=False)
            self.lview.adapter = self.list_adapter

            for i in range(self.list_adapter.get_count()):
                self.d.append(self.list_adapter.data[i]["text"])
            self.list_adapter.adapter.bind(on_selected_item=self.callback)
        except:
            pass

    def callback(self,adapter,*args):
        if len(self.adapter.selection) == 0:
            print("No selected item")
        else:
            print(self.adapter.selection[0].text)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)


sc = ScreenManager()
sc.add_widget(Watermark(name='Watermark'))


class WatermarkApp(App):
    def build(self):
        return sc

    def on_pause(self):
        return True


if __name__ == "__main__":
    WatermarkApp().run()
