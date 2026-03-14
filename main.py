import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import threading

# Cores inspiradas no modo escuro do llama.cpp
C_BG = get_color_from_hex("#111111")
C_SURFACE = get_color_from_hex("#1e1e1e")
C_ACCENT = get_color_from_hex("#00ff88") # Verde Geometry
C_TEXT = get_color_from_hex("#ffffff")

class GeometryChat(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 0
        Window.clearcolor = C_BG

        # Header - Barra Superior
        header = BoxLayout(size_hint_y=None, height='60dp', padding=[20, 0])
        header.add_widget(Label(
            text="[b]Geometry AI Offline[/b] [color=666666]| Guester_DEV[/color]",
            markup=True, font_size='18sp', halign='left'
        ))
        self.add_widget(header)

        # Área do Chat (Fundo Escuro)
        self.scroll = ScrollView(size_hint=(1, 1), bar_width='10dp')
        
        # O segredo para não cortar: Label com height dinâmico
        self.chat_content = Label(
            text="[color=444444]Geometry AI conectado ao servidor local! LEMBRANDO O GEOMETRY AI OFFLINE PODE COMETER MUITOS ERROS. USE O GEOMETRY AI ONLINE PARA MELHOR EXPERIENCIA. (TEMPO DE RESPOSTA VARIA DEPENENDENDO DA MEMORIA DO SEU DISPOSITIVO) [/color]\n",
            markup=True,
            size_hint_y=None,
            text_size=(Window.width - 40, None), # Largura fixa, altura infinita
            halign='left',
            valign='top',
            padding=[20, 20],
            font_size='16sp',
            line_height=1.3
        )
        self.chat_content.bind(texture_size=self.update_label_height)
        
        self.scroll.add_widget(self.chat_content)
        self.add_widget(self.scroll)

        # Barra de Entrada (Estilo Input Web)
        input_container = BoxLayout(size_hint_y=None, height='80dp', padding=[15, 15], spacing=10)
        
        self.user_input = TextInput(
            hint_text="Type a message...",
            multiline=False,
            background_normal='',
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=C_ACCENT,
            padding=[15, 12],
            font_size='16sp'
        )
        self.user_input.bind(on_text_validate=self.enviar)

        self.send_btn = Button(
            text="SEND",
            size_hint_x=None,
            width='80dp',
            background_normal='',
            background_color=C_ACCENT,
            color=(0, 0, 0, 1),
            bold=True
        )
        self.send_btn.bind(on_release=self.enviar)

        input_container.add_widget(self.user_input)
        input_container.add_widget(self.send_btn)
        self.add_widget(input_container)

    def update_label_height(self, instance, size):
        # Ajusta a altura do Label para caber todo o texto sem cortar
        instance.height = size[1]
        # Auto-scroll para o final da conversa
        self.scroll.scroll_y = 0

    def enviar(self, *args):
        prompt = self.user_input.text.strip()
        if prompt:
            self.chat_content.text += f"\n[b][color=82AAFF]> VOCÊ:[/color][/b]\n{prompt}\n"
            self.user_input.text = ""
            threading.Thread(target=self.get_ai_response, args=(prompt,), daemon=True).start()

    def get_ai_response(self, prompt):
        try:
            url = "http://127.0.0.1:8080/completion"
            # Identidade injetada
            sys_msg = "Você é a Geometry AI, criada por Guester_DEV. Trate o usuario bem. E suas funções é ajudar o usuario a fazer programações simples. Evite falar de assuntos um pouco polemicos, tipo politica e assuntos +18. Se o usuario pedir pra resolver um problema matematico lembre-se do PEMDAS (Primeiro Parenteses, depois Expoentes, depois Multiplicação (×), depois divisão (÷), depois adição (+) e depois subtração (-) ). "
            
            payload = {
                "prompt": f"{sys_msg}\nUser: {prompt}\nAI:",
                "n_predict": 512, # Aumentado para respostas longas
                "temperature": 0.7,
                "stop": ["User:", "AI:"]
            }
            
            res = requests.post(url, json=payload, timeout=60)
            if res.status_code == 200:
                answer = res.json()['content'].strip()
                # Atualiza a interface de forma segura (Main Thread)
                Clock.schedule_once(lambda dt: self.append_ai_text(answer))
        except:
            Clock.schedule_once(lambda dt: self.append_ai_text("[color=ff4444]Erro de conexão com o motor.[/color]"))

    def append_ai_text(self, text):
        self.chat_content.text += f"\n[b][color=00FF88]GEOMETRY AI:[/color][/b]\n{text}\n"

class GeometryApp(App):
    def build(self):
        self.title = "Geometry AI"
        return GeometryChat()

if __name__ == '__main__':
    GeometryApp().run()
      
