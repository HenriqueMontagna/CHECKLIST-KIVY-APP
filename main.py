#Coding: utf-8
#Autor: Henrique Ferreira La Montagna
#Ultima Atualização 28/07/2019

import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
import sqlite3

Kvlang = '''

<Tarefas>:
    orientation: 'vertical'
    ScrollView:
        BoxLayout:
            id: box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
    BoxLayout:
        size_hint_y: None
        size_hint_y: 0.1
        TextInput:
            id: entrada
        Button:
            size_hint_x: None
            size_hint_x: 0.15
            text: "Add"
            on_release: root.addWidget()

<Tarefa>:
    id: linha
    size_hint_y: None
    height: 150
    Label:
        id: texto
        font_size: 30
    Button:
        text: 'X'
        color: [1, 0, 0, 1]
        font_size: 50
        size_hint_x: None
        size_hint_x: 0.15
        on_press: root.removeWidget()
        on_release: app.root.ids.box.remove_widget(root) 
    Button:
        id: conc
        text: 'Feito'
        font: 'Wingdings'
        size_hint_x: None
        size_hint_x: 0.15
        on_release: root.colorChange()
'''


class Tarefa(BoxLayout):

    # DEFINE A CLASSE TAREFA E SEUS PARAMETROS PARA SER USADA NA CLASSE "TAREFAS"
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.ids.texto.text = text

    # MUDA A COR DO TEXTO E DO BOTÃO PARA VERDE, SE PRESSIONADO, OU VOLTA À COR ORIGINAL
    def colorChange(self):
        if self.ids.texto.color == [1, 1, 1, 1]:
            self.ids.texto.color = [0, 1, 0, 1]
            self.ids.conc.color = [0, 1, 0, 1]
            # Conecta com o BD para excluir a Tarefa
            self.conn = sqlite3.connect('ListaDeTarefas.db')
            # Habilita a modificação das Tabelas
            self.cursor = self.conn.cursor()
            # Altera para 0 (não concluido)
            self.cursor.execute("UPDATE listas SET feito = 1 WHERE tarefa = " + "'" + self.ids.texto.text + "'" + ";")
            # Atualiza e Salva o Banco de Dados
            self.conn.commit()

        else:
            self.ids.texto.color = [1, 1, 1, 1]
            self.ids.conc.color = [1, 1, 1, 1]
            # Conecta com o BD para excluir a Tarefa
            self.conn = sqlite3.connect('ListaDeTarefas.db')
            # Habilita a modificação das Tabelas
            self.cursor = self.conn.cursor()
            # Altera para 0 (não concluido)
            self.cursor.execute("UPDATE listas SET feito = 0 WHERE tarefa = " + "'" + self.ids.texto.text + "'" + ";")
            # Atualiza e Salva o Banco de Dados
            self.conn.commit()

    def removeWidget(self):
    # Conecta com o BD para excluir a Tarefa
        self.conn = sqlite3.connect('ListaDeTarefas.db')
    # Habilita a modificação das Tabelas
        self.cursor = self.conn.cursor()
    # Deleta a linha da tarefa atual
        self.cursor.execute("DELETE FROM listas WHERE tarefa = "+"'"+self.ids.texto.text+"'" + ";")
    # Atualiza e Salva o Banco de Dados
        self.conn.commit()

class Tarefas(BoxLayout):

    # ADICIONA TAREFAS PARA CADA ELEMENTO DA LISTA
    def __init__(self, tarefas, **kwargs):
        super().__init__(**kwargs)
        for tarefa in tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))
    # ADICIONA TAREFAS QUE O USUARIO DIGITOU E LIMPA A CAIXA DE TEXTO
    def addWidget(self):
        if self.ids.entrada.text != '':
            texto = self.ids.entrada.text
            self.ids.box.add_widget(Tarefa(text=texto))
        # Adiciona no banco de dados
            self.conn = sqlite3.connect('ListaDeTarefas.db')
            self.cursor = self.conn.cursor()
            texto_add = self.ids.entrada.text
            self.cursor.execute("INSERT INTO listas VALUES(Null, " + "'" + texto_add + "'" + ");")
            #Salva no banco de dados
            self.conn.commit()
        # Limpa a Caixa de Texto
            self.ids.entrada.text = ''


class Test(App):

    # CLASSE PRINCIPAL DA APLICAÇÃO
    def build(self):
        # Carrega o Código KV
        Builder.load_string(Kvlang)
        # Conecta com o Banco de Dados
        self.conn = sqlite3.connect('ListaDeTarefas.db')
        # Permite selecionar e percorrer o Banco de Dados
        self.cursor = self.conn.cursor()
        # Cria duas listas onde o BD vai retornar os valores
        self.listas, self.lista = [], []
        # BD retorna os Valores em Tuplas, aqui nós convertemos cada valor de "Tupla" para "Lista" e adicionamos
        # dentro de "listas"
        for row in self.cursor.execute("SELECT tarefa FROM listas"):
            self.listas.append(list(row))
        # Como os valores retornados em 'listas' são listas dentro de listas, vamos desempacotar a lista,
        # elemento por elemento, e adicionar para 'lista'
        for x, y in enumerate(self.listas):
            self.lista.append(self.listas[x][0])
        return Tarefas(self.lista)


janela = Test()
janela.run()

('Código Antigo, antes de tentar verificar o status "Feito" \n'
 '\n'
 'from kivy.app import App\n'
 'from kivy.uix.boxlayout import BoxLayout\n'
 'from kivy.lang.builder import Builder\n'
 'import sqlite3\n'
 '\n'
 'Kvlang =\n'
 '\n'
 '<Tarefas>:\n'
 '    orientation: \'vertical\'\n'
 '    ScrollView:\n'
 '        BoxLayout:\n'
 '            id: box\n'
 '            orientation: \'vertical\'\n'
 '            size_hint_y: None\n'
 '            height: self.minimum_height\n'
 '    BoxLayout:\n'
 '        size_hint_y: None\n'
 '        size_hint_y: 0.1\n'
 '        TextInput:\n'
 '            id: entrada\n'
 '        Button:\n'
 '            size_hint_x: None\n'
 '            size_hint_x: 0.15\n'
 '            text: "Add"\n'
 '            on_release: root.addWidget()\n'
 '\n'
 '<Tarefa>:\n'
 '    size_hint_y: None\n'
 '    height: 150\n'
 '    Label:\n'
 '        id: texto\n'
 '        font_size: 30\n'
 '    Button:\n'
 '        text: \'X\'\n'
 '        color: [1, 0, 0, 1]\n'
 '        font_size: 50\n'
 '        size_hint_x: None\n'
 '        size_hint_x: 0.15\n'
 '        on_release: app.root.ids.box.remove_widget(root)\n'
 '    Button:\n'
 '        id: conc\n'
 '        text: \'Feito\'\n'
 '        size_hint_x: None\n'
 '        size_hint_x: 0.15\n'
 '        on_release: root.colorChange()\n'
 '\n'
 '\n'
 '\n'
 'class Tarefa(BoxLayout):\n'
 '\n'
 '# DEFINE A CLASSE TAREFA E SEUS PARAMETROS PARA SER USADA NA CLASSE "TAREFAS"\n'
 '    def __init__(self, text=\'\', **kwargs):\n'
 '        super().__init__(**kwargs)\n'
 '        self.ids.texto.text = text\n'
 '\n'
 '# MUDA A COR DO TEXTO E DO BOTÃO PARA VERDE, SE PRESSIONADO, OU VOLTA À COR ORIGINAL\n'
 '    def colorChange(self):\n'
 '        if self.ids.texto.color == [1, 1, 1, 1]:\n'
 '            self.ids.texto.color = [0, 1, 0, 1]\n'
 '            self.ids.conc.color = [0, 1, 0, 1]\n'
 '        else:\n'
 '            self.ids.texto.color = [1, 1, 1, 1]\n'
 '            self.ids.conc.color = [1, 1, 1, 1]\n'
 '\n'
 '\n'
 'class Tarefas(BoxLayout):\n'
 '\n'
 '# ADICIONA TAREFAS PARA CADA ELEMENTO DA LISTA\n'
 '    def __init__(self, tarefas, **kwargs):\n'
 '        super().__init__(**kwargs)\n'
 '        for tarefa in tarefas:\n'
 '            self.ids.box.add_widget(Tarefa(text=tarefa))\n'
 '\n'
 '# ADICIONA TAREFAS QUE O USUARIO DIGITOU E LIMPA A CAIXA DE TEXTO\n'
 '    def addWidget(self):\n'
 '        if self.ids.entrada.text != \'\':\n'
 '            texto = self.ids.entrada.text\n'
 '            self.ids.box.add_widget(Tarefa(text=texto))\n'
 '            self.conn = sqlite3.connect(\'ListaDeTarefas.db\')\n'
 '            self.cursor = self.conn.cursor()\n'
 '            texto_add = self.ids.entrada.text\n'
 '            self.cursor.execute("INSERT INTO listas VALUES(Null, "+ "\'" + texto_add + "\'" +");")\n'
 '            self.conn.commit()\n'
 '            self.ids.entrada.text = \'\'\n'
 '\n'
 '\n'
 'class Test(App):\n'
 '\n'
 '# CLASSE PRINCIPAL DA APLICAÇÃO\n'
 '    def build(self):\n'
 '    #Carrega o Código KV\n'
 '        Builder.load_string(Kvlang)\n'
 '    #Conecta com o Banco de Dados\n'
 '        self.conn = sqlite3.connect(\'ListaDeTarefas.db\')\n'
 '    #Permite selecionar e percorrer o Banco de Dados\n'
 '        self.cursor = self.conn.cursor()\n'
 '    #Cria duas listas onde o BD vai retornar os valores\n'
 '        self.listas, self.lista = [], []\n'
 '    #BD retorna os Valores em Tuplas, aqui nós convertemos cada valor de "Tupla" para "Lista" e adicionamos dentro de "listas"\n'
 '        for row in self.cursor.execute("SELECT tarefa FROM listas"):\n'
 '            self.listas.append(list(row))\n'
 '    #Como os valores retornados em \'listas\' são listas dentro de listas, vamos desempacotar a lista, elemento por elemento, e adicionar para \'lista\'\n'
 '        for x, y in enumerate(self.listas):\n'
 '            self.lista.append(self.listas[x][0])\n'
 '        return Tarefas(self.lista)\n'
 '\n'
 '\n'
 '\n'
 'Test().run()\n'
 '\n'
 '\n')