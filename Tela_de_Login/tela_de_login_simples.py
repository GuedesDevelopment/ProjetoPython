import PySimpleGUI as sg
import os
import json

class Tela_de_login:
    def __init__(self):    
        self.filename = 'save data.json'

        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.filename), 'r+') as save:
            try:
                self.save_data = json.load(save)
            except json.JSONDecodeError:
                json.dump({}, save)

    def popup(self, titulo, texto):
        _, _ = sg.Window(f'{titulo}', [[sg.Text(f'{texto}')], [sg.Yes('Ok', s=5)]], disable_close=True, modal=True).read(close=True)


    def adiciona_user(self, usuario, senha):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.filename), 'r+') as arquivo:
            dados = json.load(arquivo)
            
            if usuario == '' or senha == '':
                self.self.popup('Erro!', 'Não deixe campos em brnaco')


            else:
                if  dados == {}:
                    
                    dados.update({usuario:senha})
                    arquivo.seek(0)
                    json.dump(dados, arquivo)
                    self.popup('Aviso!','Cadastro concluído com sucesso')
                    return True

                else:
                    for usuarios in dados:
                        if usuario == usuarios:
                            self.popup('Aviso!', 'Esse nome de usuario já está em uso')
                            
                        else:
                            dados.update({usuario:senha})
                            arquivo.seek(0)
                            json.dump(dados, arquivo)

                            self.popup('Aviso!','Cadastro concluído com sucesso')
                            return True


    def tela_cadastro(self):

        sg.theme('Default1')

        layout = [  [sg.Text('Digite seu usuário:', p=((0,20.5),(0,0))), sg.Input(k='cadastro_user', expand_x=True)],
                    [sg.Text('Digite seu email:', p=((0,31.5),(0,0))), sg.Input(k= 'nao_salvar' , expand_x=True)],
                    [sg.Text('Digite sua senha:', p=((0,27.5),(0,0))), sg.Input(do_not_clear=False, k='cadastro_senha', password_char='*', expand_x=True)],
                    [sg.Text('Confirme sua senha:', p=((0,10),(0,0))), sg.Input(do_not_clear=False, k='cadastro_confirma', password_char='*', expand_x=True)],
                    [sg.Button('Cadastre-se'), sg.Button('Cancelar')]  ]


        janela_cadastro = sg.Window('Faça seu cadastro', layout=layout, modal=True)


        while True:
            evento, valores = janela_cadastro.read()

            if evento == 'Cancelar' or evento == sg.WIN_CLOSED:
                break

            elif evento == 'Cadastre-se':
                if valores['cadastro_senha'] != valores['cadastro_confirma']:
                    self.popup('Erro!', 'As senhas não correspondem')

                else:
                    check = self.adiciona_user(valores['cadastro_user'], valores['cadastro_senha'])
                    if check:
                        janela_cadastro.close()

                    
        
        janela_cadastro.close()


    def redefinir_senha(self):
        sg.theme('SystemDefaultForReal')

        layout = [  [sg.Text('Digite seu usuário:'), sg.Input(k= 'redefinir_usuario' , expand_x=True)],
                    [sg.Text('Digite sua nova senha:'), sg.Input(k= 'redefinir_senha', password_char='*' , expand_x=True)],  
                    [sg.Text('Confirme sua nova senha:'), sg.Input(k= 'redefinir_confirma', password_char='*' , expand_x=True)],
                    [sg.Button('Redefinir Senha'), sg.Button('Cancelar')]  ]
        
        janela_redefinir = sg.Window('Redefina sua senha', layout=layout)

        while True:
            evento, valores = janela_redefinir.read()

            if evento == 'Cancelar' or evento == sg.WIN_CLOSED:
                break
            
            elif evento == 'Redefinir Senha':
                
                if valores['redefinir_senha'] != valores['redefinir_confirma']:
                    self.popup('Erro!', 'As senhas não correspondem')

                else:
                    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.filename), 'r+') as ler_senha:
                        usuarios = json.load(ler_senha)
                        
                        if valores['redefinir_usuario'] not in usuarios:
                            self.popup('Erro!', 'Esse usuário não existe')

                        elif valores['redefinir_senha'] == usuarios[valores['redefinir_usuario']]:
                            self.popup('Erro!', 'A senha informada já está em uso')

                        else:
                            usuarios[valores['redefinir_usuario']]= str(valores['redefinir_senha'])
                            ler_senha.seek(0)
                            json.dump(usuarios, ler_senha)

                            self.popup('Aviso!', 'Senha alterada com sucesso!')
                            break


        janela_redefinir.close()

# Tela Inicial
    def tela_inicial(self):
        sg.theme('LightPurple')

        layout = [[sg.Text('Aguarde um momento, você será redirecionado')]]

        janela_inicial = sg.Window('Tela de início', layout=layout)

        _, _ = janela_inicial.read(timeout=1500)

        janela_inicial.close()


    def login(self, usuario, senha):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.filename), 'r+') as login:
            usuarios = json.load(login)

            if usuario not in usuarios:
                self.popup('Erro!', 'Esse usuário não existe, favor realizar o cadastro')

            else:
                if usuarios[usuario] != senha:
                    self.popup('Erro!', 'Senha inválida')
                
                else:
                    self.tela_inicial() 
                    return True

    def tela_login(self):
        sg.theme('LightPurple')

        layout = [  [sg.Text('Digite seu usuário:'), sg.Input(do_not_clear=False, k='login_user', s=(30))],
                    [sg.Text('Digite sua senha:  '), sg.Input(do_not_clear=False, k='login_senha', password_char='*', s=(30))],
                    [sg.Button('Login'),sg.Button('Cadastrar'),sg.Button('Redefinir Senha'),sg.Button('Sair')] ]

        janela_login = sg.Window('Faça seu login', layout=layout)

        while True:
            evento, valores = janela_login.read()

            if evento == 'Sair' or evento == sg.WIN_CLOSED:
                break

            elif evento == 'Cadastrar':
                self.tela_cadastro()
            
            elif evento == 'Login':
                check = self.login(valores['login_user'], valores['login_senha'])
                if check:
                    break

            elif evento == 'Redefinir Senha':
                self.redefinir_senha()

        janela_login.close()