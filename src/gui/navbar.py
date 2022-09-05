from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget

class FileDropDown(DropDown):
    pass

class EditDropDown(DropDown):
    pass

class NavBar(Widget):
    file_dropdown = FileDropDown()
    edit_dropdown = EditDropDown()

    file_main_button = Button(text='File', size_hint=(None, None))
    edit_main_button = Button(text='Edit', size_hint=(None, None))

    file_main_button.bind(on_release=file_dropdown.open)
    edit_main_button.bind(on_release=edit_dropdown.open)

    # file_dropdown.bind(on_select=lambda instance, x: setattr(file_main_button, 'text', x))
    # edit_dropdown.bind(on_select=lambda instance, x: setattr(edit_main_button, 'text', x))