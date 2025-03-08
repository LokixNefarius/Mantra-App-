from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader

class ContadorApp(App):
    def build(self):
        # Configura a tela preta inicial
        Window.clearcolor = (0, 0, 0, 1)

        self.contagem = 30  # Valor inicial do contador
        self.binaural = SoundLoader.load("binaural.mp3")  # Carrega o som binaural
        self.cor_atual = 0  # Estado inicial da cor (0 = preto, 1 = azul)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Rótulo do contador
        self.label = Label(text=str(self.contagem), font_size=150, color=(1, 1, 1, 1))
        self.layout.add_widget(self.label)

        # Slider para escolher o tempo de contagem
        self.slider = Slider(min=20, max=60, value=30, step=1)
        self.slider.bind(value=self.atualizar_contagem_inicial)
        self.layout.add_widget(self.slider)

        # Botão para iniciar/reiniciar
        self.botao = Button(text="Iniciar", font_size=40, size_hint=(None, None), size=(200, 100))
        self.botao.bind(on_press=self.iniciar_contagem)
        self.layout.add_widget(self.botao)

        return self.layout

    def atualizar_contagem_inicial(self, instance, value):
        self.contagem = int(value)
        self.label.text = str(self.contagem)

    def iniciar_contagem(self, instance):
        self.botao.disabled = True  # Desativa botão durante a contagem
        self.contagem = int(self.slider.value)  # Reinicia a contagem com o valor escolhido
        self.label.text = str(self.contagem)

        # Inicia o som binaural se não estiver tocando
        if self.binaural:
            self.binaural.loop = True
            self.binaural.play()

        # Define o intervalo de acordo com a contagem
        intervalo = 2  # Tempo fixo de 2 segundos para cada número
        Clock.schedule_interval(self.atualizar_contagem, intervalo)  
        Clock.schedule_interval(self.pulsar_fundo, intervalo)  # Agora sincronizado com a contagem

    def atualizar_contagem(self, dt):
        if self.contagem > 0:
            self.contagem -= 1
            self.label.text = str(self.contagem)
        else:
            Clock.unschedule(self.atualizar_contagem)
            Clock.unschedule(self.pulsar_fundo)
            self.botao.disabled = False  # Reativa o botão
            if self.binaural:
                self.binaural.stop()  # Para o som binaural

    def pulsar_fundo(self, dt):
        """ Alterna a cor do fundo no mesmo ritmo do contador """
        self.cor_atual = 1 - self.cor_atual  # Alterna entre 0 e 1
        Window.clearcolor = (0, 0, 0.5) if self.cor_atual else (0, 0, 0)  # Alterna entre azul escuro e preto

if __name__ == "__main__":
    ContadorApp().run()
