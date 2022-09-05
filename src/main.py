from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty

import gui.navbar

Builder.load_file('gui/main.kv')
Builder.load_file('gui/navbar.kv')

class main_kv(Widget):
    apple = NumericProperty(0)

    def thingy(self):
        self.apple += 1
        self.ids.first.text = str(self.apple)


class MTGScanner(App):
    def build(self):
        self.x = 150
        self.y = 400
        return main_kv()

if __name__ == '__main__':
    MTGScanner().run()