from tkinter import *
import tkinter.messagebox as tkmsg #Importa o tkinter.messagebox como tkmsg
import json as j
import os

usuarios = {}

def carregar_usuarios():
    global usuarios
    if os.path.exists("supermercado.json"):
        try:
            with open("UC5/supermercado.json", "r", encoding="utf-8") as arquivo:
                usuarios = j.load(arquivo)
        except j.JSONDecodeError:
            usuarios = {}
    else:
        usuarios = {}

def verficar_cadastro():
    if entry_username2.get() in usuarios.keys():
        tkmsg.showerror("ERRO", "Usuario já cadastrado")
    elif entry_password2.get() == entry_password3.get():
        usuarios[entry_username2.get()] = entry_password3.get()
        with open("UC5/supermercado.json" , "w", encoding="utf-8") as file:
            j.dump(usuarios, file, indent=2)
        tkmsg.showinfo("SUCESSO", "Cadastro feito com sucesso!")
    else:
        tkmsg.showerror("ERRO", "As senhas devem ser iguais")

def verificar_login():
    username = entry_username.get()
    password = entry_password.get()

    if username in usuarios.keys() and password in usuarios.values():
        tkmsg.showinfo('login', 'login bem-sucedido!')
        root.deiconify()
        login.destroy()
    else:
        tkmsg.showerror('login', 'credenciais inválidas')

def tab_cadastro():
   global entry_username2, entry_password2, entry_password3
   login.withdraw()
   cadastro = Toplevel(login)
   cadastro.title('Cadastro')
   cadastro.geometry('375x667')
   
   label_username2 = Label(cadastro, text='nome de usuário:')
   label_username2.pack()
   entry_username2 = Entry(cadastro, width=30)
   entry_username2.pack(pady=5)
   
   label_password2 = Label(cadastro, text='Senha:')
   label_password2.pack()
   entry_password2 = Entry(cadastro, show='*', width=30)
   entry_password2.pack(pady=5)
   
   label_confirm = Label(cadastro, text='Confirmar senha')
   label_confirm.pack()
   entry_password3 = Entry(cadastro, show='*', width=30)
   entry_password3.pack(pady=5)
   
   button_confirm = Button(cadastro, text='Cadastrar', width=20, command=verficar_cadastro)
   button_confirm.pack(side=LEFT, padx=20, pady=20)

   button_cancel2 = Button(cadastro, text='Cancelar', width=20, command=lambda: [cadastro.destroy(), login.deiconify()])
   button_cancel2.pack(side=RIGHT, padx=20, pady=20)

def tab_login():
    global login, entry_password, entry_username 
    login = Toplevel(root)
    login.title('Tela de Login')
    login.geometry('375x270')

    
    placeholder_image = PhotoImage(width=1, height=1)
    label_image = Label(login, image=placeholder_image)
    label_image.pack(pady=1)
    
    label_username = Label(login, text='nome de usuário:')
    label_username.pack()
    entry_username = Entry(login, width=30)
    entry_username.pack(pady=5)
    
    label_password = Label(login, text='senha:')
    label_password.pack()
    entry_password = Entry(login, show='*', width=30)
    entry_password.pack(pady=5)
    
    frame_buttons = Frame(login)
    frame_buttons.pack(pady=20)
    
    button_login = Button(frame_buttons, text='login', width=10, command=verificar_login)
    button_login.pack(side=LEFT, padx=10)
    
    button_cancel = Button(frame_buttons, text='cancelar', width=10, command=login.quit)
    button_cancel.pack(side=RIGHT, padx=10)
    
    button_createAccount = Button(frame_buttons, text='Criar Conta', width=20, command=tab_cadastro)
    button_createAccount.pack(side=RIGHT, padx=20)

def main():
    global root
    root = Tk()
    root.geometry("850x700")
    root.title("telamuitotopmesmochave")

    frame_buttonsss = Frame(root)
    
    butao_estoque = Button(root, text='GERENCIAR ESTOQUE', width=25, height=10, command= None)
    butao_estoque.place(x=100, y=220)

    butao_produtos = Button(root, text='PRODUTOS COMPRADOS', width=25, height=10, command= None)
    butao_produtos.place(x=325, y=220)

    butao_rastreamentos = Button(root, text='RASTREAMENTO DE VENDAS', width=25, height=10, command= None)
    butao_rastreamentos.place(x=550, y=220)

    
    root.withdraw()    
    tab_login()    
    root.mainloop()

if __name__ == "__main__":

    main()