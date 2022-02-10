from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.picker import MDDatePicker
from kivy.clock import Clock
from kivymd.icon_definitions import md_icons
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
import tcc_v3, datetime
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

plt.style.use("seaborn-dark")

for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey

for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey

plt.rcParams['axes.linewidth'] = 0.5
colors = [
    '#08F7FE',  # teal/cyan
    '#f7536a',  # vermelho
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    '#a9fde8',  
    '#befda9',  
    '#e8a9fd',  
    '#fda9be',  
    '#f78e53'   
]

screen_helper = """
ScreenManager:
    LoginScreen:
    InfoScreen:
    DcustomerScreen:
    DenelScreen:
    AcustomerScreen:
    AenelScreen:

<LoginScreen>:
    name: 'login'
    Image:
        size_hint: .2, .2
        pos_hint: {"center_x": .5, "center_y": .75}
        source: 'enelblue2.jpg'
        allow_stretch: True
        keep_ratio: True
        #size_hint_y: None
        size_hint_x: 0.5
        #width: self.parent.width * 0.6
        #height: self.parent.width/self.image_ratio *0.8
    MDTextField:
        id: cpf
        icon_right: "email"
        hint_text: "CPF ou Email"
        mode: "rectangle"
        helper_text: "Omita pontos e traço"
        helper_text_mode: "on_focus"
        pos_hint: {'center_x':0.5,'center_y':0.55}
        size_hint_x: None
        width: 300
        halign: 'center'
    MDTextField:
        id: senha
        hint_text: "Senha"
        mode: "rectangle"
        icon_right: 'eye-off'
        helper_text: "Muito cuidado :)"
        helper_text_mode: "on_focus"
        pos_hint: {'center_x':0.5,'center_y':0.45}
        size_hint_x: None
        width: 300
        halign: 'center'
        password: True
        on_icon_right: root.show()
    MDRectangleFlatIconButton:
        icon: 'lightning-bolt'
        text: 'Login'
        pos_hint: {'center_x':0.5,'center_y':0.32}
        on_release: root.testa_login()
    
<InfoScreen>:
    name: 'info'
    ScrollView:
        MDList:
            id: scroll
            MDToolbar:
                title: "Informações gerais"
                pos_hint: {"top": 1}
                elevation: 10
            OneLineAvatarIconListItem:
                id: nome_label
                text: 'Nome: '
                IconLeftWidget:
                    icon: "account" 
            OneLineAvatarIconListItem:
                id: cpf_label
                text: 'CPF: '
                IconLeftWidget:
                    icon: "card-account-details" 
            OneLineAvatarIconListItem:
                id: email_label
                text: 'Email: '
                IconLeftWidget:
                    icon: "gmail" 
            OneLineAvatarIconListItem:
                id: estado_label
                text: 'Estado: '
                IconLeftWidget:
                    icon: "flag-variant" 
            OneLineAvatarIconListItem:
                id: cidade_label
                text: 'Cidade: '
                IconLeftWidget:
                    icon: "city-variant" 
            OneLineAvatarIconListItem:
                id: bairro_label
                text: 'Bairro: '
                IconLeftWidget:
                    icon: "home-city" 
            OneLineAvatarIconListItem:
                id: rua_label
                text: 'Rua: '
                IconLeftWidget:
                    icon: "home-variant" 
            OneLineAvatarIconListItem:
                id: preco_label
                text: 'Preço da fatura atual: R$ 120 reais'
                IconLeftWidget:
                    icon: "cash" 
    MDRectangleFlatButton:
        text: 'Logout'
        pos_hint: {'center_x':0.5,'center_y':0.07}
        on_press: root.manager.current = 'login'
    MDFloatingActionButtonSpeedDial:
        id: speeddial
        data: root.data
        root_button_anim: True
        right_pad: True
        callback: root.callback  

<DcustomerScreen>:
    name: 'dcustomer'
    ScrollView:
        MDList:
            id: scroll
            MDToolbar:
                title: "Consumo detalhado (Customer)"
                pos_hint: {"top": 1}
                elevation: 10
    MDBoxLayout:
        id: destination
        adaptive_height: True
        adaptive_width: True
        pos_hint: {'top': 0.88}
        size: root.width, root.height*0.75
    MDFloatingActionButtonSpeedDial:
        data: root.data
        root_button_anim: True
        callback: root.callback
    MDRectangleFlatIconButton:
        icon: 'chart-line'
        text: 'Gerar gráfico'
        pos_hint: {'center_x':0.65,'center_y':0.07}
        on_press: root.gera_grafico()
    MDRectangleFlatIconButton:
        icon: 'calendar'
        text: 'Selecionar Intervalo'
        pos_hint: {'center_x':0.35,'center_y':0.07}
        on_release: root.show_date_picker()

<DenelScreen>:
    name: 'denel'
    MDBoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "Consumo detalhado (Enel)"
            pos_hint: {"top": 1}
            size: root.width, root.height*0.08
            elevation: 5
        MDTabs:
            id: tabs
            default_tab: 2
            pos_hint: {"top": 1}
            size: root.width, root.height*0.02
            on_tab_switch: root.on_tab_switch(*args)
            Tab:
                icon: "card-account-details"
                title: "Customers"
                MDBoxLayout:
                    id: destination
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
            Tab:
                icon: "flag-variant"
                title: "Estado"
                MDBoxLayout:
                    id: destination2
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico_2()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
            Tab:
                icon: "city-variant"
                title: "Cidade"
                MDBoxLayout:
                    id: destination3
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico_3()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
            Tab:
                title: "Bairro"
                icon: "home-city"
                MDBoxLayout:
                    id: destination4
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico_4()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()

<AcustomerScreen>:
    name: 'acustomer'
    ScrollView:
        MDList:
            id: scroll
            MDToolbar:
                title: "Consumo agregado (Customer)"
                pos_hint: {"top": 1}
                elevation: 10
    MDBoxLayout:
        id: destination
        adaptive_height: True
        adaptive_width: True
        pos_hint: {'top': 0.88}
        size: root.width, root.height*0.75
    MDFloatingActionButtonSpeedDial:
        data: root.data
        root_button_anim: True
        callback: root.callback
    MDRectangleFlatIconButton:
        icon: 'chart-line'
        text: 'Gerar gráfico'
        pos_hint: {'center_x':0.65,'center_y':0.07}
        on_press: root.gera_grafico()
    MDRectangleFlatIconButton:
        icon: 'calendar'
        text: 'Selecionar Intervalo'
        pos_hint: {'center_x':0.35,'center_y':0.07}
        on_release: root.show_date_picker()

<AenelScreen>:
    name: 'aenel'
    MDBoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "Consumo agregado (Enel)"
            pos_hint: {"top": 1}
            size: root.width, root.height*0.08
            elevation: 5
        MDTabs:
            id: tabs
            default_tab: 2
            pos_hint: {"top": 1}
            size: root.width, root.height*0.02
            on_tab_switch: root.on_tab_switch(*args)
            Tab:
                icon: "card-account-details"
                title: "Customers"
                MDBoxLayout:
                    id: destination
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
            Tab:
                icon: "flag-variant"
                title: "Estado"
                MDBoxLayout:
                    id: destination2
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico_2()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
            Tab:
                icon: "city-variant"
                title: "Cidade"
                MDBoxLayout:
                    id: destination3
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico_3()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
            Tab:
                title: "Bairro"
                icon: "home-city"
                MDBoxLayout:
                    id: destination4
                    adaptive_height: True
                    adaptive_width: True
                    pos_hint: {'top': 1}
                    size: root.width, root.height*0.74
                MDFloatingActionButtonSpeedDial:
                    data: root.data
                    root_button_anim: True
                    callback: root.callback
                MDRectangleFlatIconButton:
                    icon: 'chart-line'
                    text: 'Gerar gráfico'
                    pos_hint: {'center_x':0.65,'center_y':0.07}
                    on_press: root.gera_grafico_4()
                MDRectangleFlatIconButton:
                    icon: 'calendar'
                    text: 'Selecionar Intervalo'
                    pos_hint: {'center_x':0.35,'center_y':0.07}
                    on_release: root.show_date_picker()
"""

class Tab(MDTabsBase,FloatLayout):
    pass

def interval():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    start = yesterday - datetime.timedelta(days=7)
    return start, yesterday

def staile(frame, title="", group=""):
    fig, ax = plt.subplots()

    if "agregado" not in title: frame.groupby(group).plot.line(x = "data", y = "consumo", ax=ax, marker='o')
    else: frame.pivot(index='data', columns=group, values='consumo real').plot.bar(ax=ax, color=colors)
   
    L = ax.legend()
    plt.setp(L.texts, fontname="DejaVu Sans", fontweight='bold')

    ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background
    if "agregado" not in title: 
        ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
        ax.set_ylim(0)
        ax.set_ybound(frame['consumo'].min() - 0.2, frame['consumo'].max() + 0.2)
    else:
        ax.set_ylim([frame['consumo real'].min() - 10, frame['consumo real'].max() + 12])
        plt.xticks(rotation='horizontal')

    
    ax.legend(frame[group].unique())
    ax.set_title(f"{title}", fontsize=23, fontweight='bold', fontname="DejaVu Sans", path_effects=[pe.withStroke(linewidth=1, foreground="white")])
    plt.xlabel('Data', fontsize=16, fontweight='bold', fontname="DejaVu Sans", path_effects=[pe.withStroke(linewidth=1, foreground="white")])
    plt.ylabel('Consumo (kWh)', fontsize=16, fontweight='bold', fontname="DejaVu Sans", path_effects=[pe.withStroke(linewidth=1, foreground="white")])
    plt.rcParams["figure.figsize"] = (20,3)
    
    return plt

class LoginScreen(Screen):  # Tela de Login
    def testa_login(self):
        global cpf, nome, email, estado, cidade, bairro, rua
        cpf = self.ids.cpf.text   # Salva o cpf como variável global (para ser usado em outras telas)
        verifica = tcc_v3.login(self.ids.cpf.text, self.ids.senha.text)    # Chama função para verificar se o login é válido

        if verifica == True:   # Se a senha estiver correta
            informacoes = tcc_v3.info_user(cpf)
            nome = informacoes["nome"]
            email = informacoes["email"]
            estado = informacoes["estado"]
            cidade = informacoes["cidade"]
            bairro = informacoes["bairro"]
            rua = informacoes["rua"]
            self.manager.current = 'info' 
        else:    # Caso a senha estiver incorreta
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Senha incorreta, tente novamente", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de senha incorreta
            self.ids.senha.text = ""
            return (False)
   
    def close_dialog(self, obj):   # Função para fechar aviso de senha incorreta
        self.dialog.dismiss()


class InfoScreen(Screen):  # Info tela
    data = {
        'Detalhado': 'chart-line',
        'Agregado': 'chart-bar',
        'Info': 'account-circle',
    }
    
    def on_enter(self):
        Clock.schedule_once(self.define_info)
    def define_info(self, dt):
        self.ids.nome_label.text = f"Nome: {nome}"
        self.ids.cpf_label.text = f"CPF: {cpf}"
        self.ids.email_label.text = f"Email: {email}"
        self.ids.estado_label.text = f"Estado: {estado}"
        self.ids.cidade_label.text = f"Cidade: {cidade}"
        self.ids.bairro_label.text = f"Bairro: {bairro}"
        self.ids.rua_label.text = f"Rua: {rua}"

    def callback(self, instance):
        if instance.icon == "chart-line":
            if cpf == "1234": self.manager.current = 'denel'
            else: self.manager.current = 'dcustomer'
        elif instance.icon == "chart-bar":
            if cpf == "1234": self.manager.current = 'aenel'
            else: self.manager.current = 'acustomer'
        elif instance.icon == "account-circle": print("Open the general info page: info page already opened!")

class DcustomerScreen(Screen):  # Tela Customer Details
    data = {
        'Detalhado': 'chart-line',
        'Agregado': 'chart-bar',
        'Info': 'account-circle',
    }

    def on_enter(self):
        Clock.schedule_once(self.define_info)
    def define_info(self, dt):
        pass

    def callback(self, instance):
        if instance.icon == "chart-line": print("Open the details page: details page already opened!")
        elif instance.icon == "chart-bar": self.manager.current = 'acustomer'
        elif instance.icon == "account-circle": self.manager.current = 'info'
    
    def close_dialog(self, obj):   # Função para fechar aviso intervalo não selecionado
        self.dialog.dismiss()
    
    def on_save(self, instance, value, date_range):  # Função para salvar valores do date picker
        global start_picker_date, end_picker_date
        start_picker_date = date_range[0]
        end_picker_date = date_range[-1]
        
    def on_cancel(self, instance, value):   # Função quando o botão de cancelar do date picker é pressionado
        pass

    def show_date_picker(self):   # Função para abrir o date picker
        date_dialog = MDDatePicker(mode="range", date_range_text_error="Selecione um intervalo válido, meu querido") 
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel) 
        date_dialog.open()
    
    def gera_grafico(self):
        try:
            y = tcc_v3.details(startdate=start_picker_date, enddate=end_picker_date, tipo="customer", cpf=cpf)
            plt = staile(y, "Consumo detalhado", group="cpf")            
            self.ids.destination.clear_widgets()
            self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            print(e)
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado
    

class DenelScreen(Screen):  # Tela Enel Details
    data = {
        'Detalhado': 'chart-line',
        'Agregado': 'chart-bar',
        'Info': 'account-circle',
    }
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if instance_tab.icon == 'flag-variant':
            start, yesterday = interval()
            y = tcc_v3.details(startdate=start, enddate=yesterday, tipo="estado", cpf=cpf)
            plt = staile(y, "Consumo detalhado", group="estado")       
            self.ids.destination2.clear_widgets()
            self.ids.destination2.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        elif instance_tab.icon == 'city-variant':
            start, yesterday = interval()
            y = tcc_v3.details(startdate=start, enddate=yesterday, tipo="cidade", cpf=cpf, estado="SP")
            plt = staile(y, "Consumo detalhado", group="cidade")       
            self.ids.destination3.clear_widgets()
            self.ids.destination3.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        elif instance_tab.icon == 'home-city':
            start, yesterday = interval()
            y = tcc_v3.details(startdate=start, enddate=yesterday, tipo="bairro", cpf=cpf, estado="SP", cidade="São Bernardo do Campo")
            plt = staile(y, "Consumo detalhado", group="bairro")       
            self.ids.destination4.clear_widgets()
            self.ids.destination4.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def on_enter(self):
        Clock.schedule_once(self.define_info)

    def define_info(self, dt):
        #start, yesterday = interval()
        #y = tcc_v3.details(startdate=start, enddate=yesterday, tipo="customer", cpf=cpf)
        #plt = staile(y, "Consumo detalhado", group="cpf")       
        #self.ids.destination.clear_widgets()
        #self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        pass

    def callback(self, instance):
        if instance.icon == "chart-line": print("Open the details page: details page already opened!")
        elif instance.icon == "chart-bar": self.manager.current = 'aenel'
        elif instance.icon == "account-circle": self.manager.current = 'info'

    def close_dialog(self, obj):   # Função para fechar aviso intervalo não selecionado
        self.dialog.dismiss()
    
    def on_save(self, instance, value, date_range):  # Função para salvar valores do date picker
        global start_picker_date, end_picker_date
        start_picker_date = date_range[0]
        end_picker_date = date_range[-1]
        
    def on_cancel(self, instance, value):   # Função quando o botão de cancelar do date picker é pressionado
        print("Cancelou")

    def show_date_picker(self):   # Função para abrir o date picker
        date_dialog = MDDatePicker(mode="range", date_range_text_error="Selecione um intervalo válido, meu querido") 
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel) 
        date_dialog.open()
    
    def gera_grafico(self): #Customer
        try:
            y = tcc_v3.details(startdate=start_picker_date, enddate=end_picker_date, tipo="customer", cpf=cpf)
            plt = staile(y, "Consumo detalhado", group="cpf")            
            self.ids.destination.clear_widgets()
            self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            print(e)
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado
    
    def gera_grafico_2(self): #Estado
        try:
            y = tcc_v3.details(startdate=start_picker_date, enddate=end_picker_date, tipo="estado", cpf=cpf)
            plt = staile(y, "Consumo detalhado", group="estado")            
            self.ids.destination2.clear_widgets()
            self.ids.destination2.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            print(e)
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado
    
    def gera_grafico_3(self): # Cidade
        try:
            y = tcc_v3.details(startdate=start_picker_date, enddate=end_picker_date, tipo="cidade", cpf=cpf, estado="SP")
            plt = staile(y, "Consumo detalhado", group="cidade")            
            self.ids.destination3.clear_widgets()
            self.ids.destination3.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            print(e)
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado
    
    def gera_grafico_4(self): # Bairro
        try:
            y = tcc_v3.details(startdate=start_picker_date, enddate=end_picker_date, tipo="bairro", cpf=cpf, estado="SP", cidade="São Bernardo do Campo")
            plt = staile(y, "Consumo detalhado", group="bairro")            
            self.ids.destination4.clear_widgets()
            self.ids.destination4.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            print(e)
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado

class AcustomerScreen(Screen):  # Tela Customer Aggregates
    data = {
        'Detalhado': 'chart-line',
        'Agregado': 'chart-bar',
        'Info': 'account-circle',
    }

    def on_enter(self):
        Clock.schedule_once(self.define_info)
    def define_info(self, dt):
        #yesterday = datetime.date.today() - datetime.timedelta(days=1)
        #start = yesterday.replace(month=1, day=1)
        #y = tcc_v3.aggregates(startdate=start, enddate=yesterday, tipo="customer", cpf=cpf, granularity="mensal")
        #plt = staile(y, "Consumo agregado", group="cpf")       
        #self.ids.destination.clear_widgets()
        #self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        pass

    def callback(self, instance):
        if instance.icon == "chart-line": self.manager.current = 'dcustomer'
        elif instance.icon == "chart-bar": print("Open the aggregates page: aggregates page already opened!")
        elif instance.icon == "account-circle": self.manager.current = 'info'
    
    def close_dialog(self, obj):   # Função para fechar aviso intervalo não selecionado
        self.dialog.dismiss()

    def on_save(self, instance, value, date_range):  # Função para salvar valores do date picker
        global start_picker_date, end_picker_date
        start_picker_date = date_range[0]
        end_picker_date = date_range[-1]
        
    def on_cancel(self, instance, value):   # Função quando o botão de cancelar do date picker é pressionado
        print("cancelou")

    def show_date_picker(self):   # Função para abrir o date picker
        date_dialog = MDDatePicker(mode="range", date_range_text_error="Selecione um intervalo direito, meu querido") 
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel) 
        date_dialog.open()

    def gera_grafico(self):
        try:
            y = tcc_v3.aggregates(startdate=start_picker_date, enddate=end_picker_date, tipo="customer", cpf=cpf, granularity="mensal")
            plt = staile(y, "Consumo agregado", group="cpf")
            self.ids.destination.clear_widgets()
            self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado

class AenelScreen(Screen):  # Tela Enel Aggregates
    data = {
        'Detalhado': 'chart-line',
        'Agregado': 'chart-bar',
        'Info': 'account-circle',
    }

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if instance_tab.icon == 'flag-variant':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            start = yesterday.replace(month=1, day=1)
            y = tcc_v3.aggregates(startdate=start, enddate=yesterday, tipo="estado", cpf=cpf, granularity="mensal")
            plt = staile(y, "Consumo agregado", group="estado")       
            self.ids.destination2.clear_widgets()
            self.ids.destination2.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        elif instance_tab.icon == 'city-variant':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            start = yesterday.replace(month=1, day=1)
            y = tcc_v3.aggregates(startdate=start, enddate=yesterday, tipo="cidade", cpf=cpf, granularity="mensal", estado="SP")
            plt = staile(y, "Consumo agregado", group="cidade")       
            self.ids.destination3.clear_widgets()
            self.ids.destination3.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        elif instance_tab.icon == 'home-city':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            start = yesterday.replace(month=1, day=1)
            y = tcc_v3.aggregates(startdate=start, enddate=yesterday, tipo="bairro", cpf=cpf, granularity="mensal", estado="SP", cidade="São Bernardo do Campo")
            plt = staile(y, "Consumo agregado", group="bairro")       
            self.ids.destination4.clear_widgets()
            self.ids.destination4.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def on_enter(self):
        Clock.schedule_once(self.define_info)
    def define_info(self, dt):
        #yesterday = datetime.date.today() - datetime.timedelta(days=1)
        #start = yesterday.replace(month=1, day=1)
        #y = tcc_v3.aggregates(startdate=start, enddate=yesterday, tipo="customer", cpf=cpf, granularity="mensal")
        #plt = staile(y, "Consumo agregado", group="cpf")       
        #self.ids.destination.clear_widgets()
        #self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        pass

    def callback(self, instance):
        if instance.icon == "chart-line": self.manager.current = 'denel'
        elif instance.icon == "chart-bar": print("Open the aggregates page: aggregates page already opened!")
        elif instance.icon == "account-circle": self.manager.current = 'info'

    def close_dialog(self, obj):   # Função para fechar aviso intervalo não selecionado
        self.dialog.dismiss()

    def on_save(self, instance, value, date_range):  # Função para salvar valores do date picker
        global start_picker_date, end_picker_date
        start_picker_date = date_range[0]
        end_picker_date = date_range[-1]
        
    def on_cancel(self, instance, value):   # Função quando o botão de cancelar do date picker é pressionado
        print("cancelou")

    def show_date_picker(self):   # Função para abrir o date picker
        date_dialog = MDDatePicker(mode="range", date_range_text_error="Selecione um intervalo direito, meu querido") 
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel) 
        date_dialog.open()

    def gera_grafico(self):
        try:
            y = tcc_v3.aggregates(startdate=start_picker_date, enddate=end_picker_date, tipo="customer", cpf=cpf, granularity="mensal")
            plt = staile(y, "Consumo agregado", group="cpf")
            self.ids.destination.clear_widgets()
            self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado
    
    def gera_grafico_2(self):
        try:
            y = tcc_v3.aggregates(startdate=start_picker_date, enddate=end_picker_date, tipo="estado", cpf=cpf, granularity="mensal")
            plt = staile(y, "Consumo agregado", group="estado")
            self.ids.destination2.clear_widgets()
            self.ids.destination2.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado
    
    def gera_grafico_3(self):
        try:
            y = tcc_v3.aggregates(startdate=start_picker_date, enddate=end_picker_date, tipo="cidade", cpf=cpf, granularity="mensal", estado="SP")
            plt = staile(y, "Consumo agregado", group="cidade")
            self.ids.destination3.clear_widgets()
            self.ids.destination3.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado

    def gera_grafico_4(self):
        try:
            y = tcc_v3.aggregates(startdate=start_picker_date, enddate=end_picker_date, tipo="cidade", cpf=cpf, granularity="mensal", estado="SP", cidade="São Bernardo do Campo")
            plt = staile(y, "Consumo agregado", group="bairro")
            self.ids.destination4.clear_widgets()
            self.ids.destination4.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        except Exception as e:
            close_button = MDRectangleFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Opa!! Assim não pode...", text="Selecione um intervalo, por favor", size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()   # Abre aviso de intervalo não selecionado

# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(InfoScreen(name='info'))
sm.add_widget(DcustomerScreen(name='dcustomer'))
sm.add_widget(DenelScreen(name='denel'))
sm.add_widget(AcustomerScreen(name='acustomer'))
sm.add_widget(AenelScreen(name='aenel'))

class DemoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue" 
        screen = Builder.load_string(screen_helper)
        return screen
    
    def show_data(self, obj):
        dialog = MDDialog(title="Error", text="Senha incorreta", size_hint=(0.7, 1))
        dialog.open()

demo = DemoApp()
demo.run()