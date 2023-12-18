# lista.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class ListaInterfaz(BoxLayout, Screen):
    participants_layout = ObjectProperty(None)
    participants_label = ObjectProperty(None)

    participants = []

    def __init__(self, **kwargs):
        super(ListaInterfaz, self).__init__(**kwargs)

        # Configurar la etiqueta de la lista de participantes
        self.participants_label = Label(text='Participantes:', size_hint=(None, None), height=44)
        self.ids.participants_layout.add_widget(self.participants_label)

    def show_participant_popup(self):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_content.add_widget(Label(text='Ingrese el nombre del participante:'))

        participant_input = TextInput(hint_text='Nombre', multiline=False)
        popup_content.add_widget(participant_input)

        popup_content.add_widget(Button(text='Agregar', on_press=lambda x: self.add_participant(participant_input.text), size_hint_y=None, height=44))

        popup = Popup(title='Agregar Participante', content=popup_content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def add_participant(self, name):
        if name:
            self.participants.append({'name': name, 'songs': []})
            self.update_participants_list()
        else:
            print('Por favor, ingrese un nombre válido.')

    def update_participants_list(self):
        participant_names = [participant['name'] for participant in self.participants]
        self.participants_label.text = 'Participantes: \n' + '\n'.join(participant_names)
