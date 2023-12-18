# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from interfaz import Interfaz
from lista import ListaInterfaz

Builder.load_file('interfaz.kv')
Builder.load_file('lista.kv')

class KaraokeApp(App):
    def build(self):
        self.title = 'Karaoke'

        # Crea un ScreenManager
        screen_manager = ScreenManager()

        # Crea las pantallas
        main_screen = Screen(name='main')
        main_screen.add_widget(Interfaz())  # No es necesario pasar screen_manager como argumento

        participants_screen = Screen(name='participants')
        participants_screen.add_widget(ListaInterfaz())  # No es necesario pasar screen_manager como argumento

        # Agrega las pantallas al ScreenManager
        screen_manager.add_widget(main_screen)
        screen_manager.add_widget(participants_screen)

        return screen_manager

if __name__ == '__main__':
    KaraokeApp().run()
