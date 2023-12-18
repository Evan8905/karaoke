# interfaz.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from googleapiclient.discovery import build
import webbrowser

class Interfaz(BoxLayout, Screen):
    search_input = ObjectProperty(None)
    lyrics_label = ObjectProperty(None)
    selected_party_type = StringProperty('Ninguno')
    participants_label = ObjectProperty(None)
    participants = []

    songs = {
        'Karaoke': ['Song1', 'Song2', 'Song3'],
        'Música': ['SongA', 'SongB', 'SongC']
    }

    def __init__(self):
        super(Interfaz, self).__init__()

        # Configurar el grupo de botones de alternancia manualmente
        self.party_type_buttons = {
            'Karaoke': ToggleButton(text='Karaoke', group='party_type', on_press=self.on_party_type_selected),
            'Música': ToggleButton(text='Musica', group='party_type', on_press=self.on_party_type_selected)
        }

        # Agregar los botones al layout
        for button in self.party_type_buttons.values():
            self.ids.party_type_layout.add_widget(button)

        # Configurar la etiqueta de la lista de participantes
        self.participants_label = Label(text='Participantes:', size_hint=(None, None), height=44)
        self.ids.participants_layout.add_widget(self.participants_label)

    def get_youtube_instance(self, api_key):
        return build('youtube', 'v3', developerKey=api_key)

    def search_youtube_video(self, youtube, search_query):
        request = youtube.search().list(q=search_query, part='snippet', type='video', maxResults=1)
        response = request.execute()

        if 'items' in response:
            return response['items'][0]['id']['videoId']
        else:
            return None

    def on_party_type_selected(self, instance):
        party_type = instance.text
        if self.selected_party_type.lower() == party_type.lower():
            # Si se hace clic en el botón que ya estaba seleccionado, establecer a "Ninguno"
            self.selected_party_type = 'Ninguno'
        else:
            # Cambiar al nuevo botón seleccionado
            self.selected_party_type = party_type.lower()

        # Desactivar el otro botón cuando se selecciona uno
        for btn in self.party_type_buttons.values():
            if btn.text.lower() != self.selected_party_type:
                btn.state = 'normal'

        print(f'Party Type Selected: {self.selected_party_type}')

    def get_lyrics(self, video_id):
        # Implementa la lógica para obtener las letras de la canción aquí.
        # Puedes utilizar otras bibliotecas o servicios para obtener las letras.
        return 'Letras de la canción para el video con ID: {}'.format(video_id)

    def play_youtube_video(self, video_id):
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        webbrowser.open(video_url)

    def search_youtube(self, search_query):
        if search_query:
            api_key = 'AIzaSyAAcWJG9s5mGEznSeFFpKuifFE5kIB7YaM'
            youtube = self.get_youtube_instance(api_key)

            # Añadir "karaoke" al final de la consulta si está seleccionado "Karaoke"
            if self.selected_party_type.lower() == 'karaoke':
                search_query += ' karaoke'

            video_id = self.search_youtube_video(youtube, search_query)
            if video_id:
                lyrics = self.get_lyrics(video_id)
                if self.lyrics_label:
                    self.lyrics_label.text = lyrics

                self.play_youtube_video(video_id)

                if self.search_input:
                    self.search_input.text = ''
            else:
                if self.lyrics_label:
                    self.lyrics_label.text = 'No se encontraron resultados'
        else:
            if self.lyrics_label:
                self.lyrics_label.text = 'Por favor, ingrese el nombre de la canción'

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
