from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config

Config.set("kivy", "window_title", "Kivy Hello World - Your Name - Roll No")


class HelloApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        self.message = Label(
            text="Hello, Welcome!",
            font_size=24
        )

        button = Button(
            text="Click Me",
            font_size=18,
            size_hint=(1, 0.3)
        )

        button.bind(on_press=self.button_clicked)

        layout.add_widget(self.message)
        layout.add_widget(button)

        return layout

    def button_clicked(self, instance):
        self.message.text = "Button clicked successfully!"


if __name__ == "__main__":
    HelloApp().run()
