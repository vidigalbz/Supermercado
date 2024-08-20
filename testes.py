from tkinter import *
import tkinter.messagebox as tkmsg #Importa o tkinter.messagebox como tkmsg
import json as j
import os

usuarios = {}
estoque = {}

def produtos_comprados():
    global entry_nome_prod, entry_qtd, entry_cate, entry_prclote, entry_prcuni, entry_prcvenda, entry_lote
    
    label_nome_prod= Label(root, text="Nome do Produto")
    label_nome_prod.place(x=10, y=50)
    entry_nome_prod = Entry(root, width=30)
    entry_nome_prod.place(x=15, y=75)

    label_cate = Label(root, text="Categoria:")
    label_cate.place(x=10, y=100)
    entry_cate = Entry(root, width=30)
    entry_cate.place(x=15, y=125)

    label_lote = Label(root, text="Lote/Validade:")
    label_lote.place(x=10, y=150)
    entry_lote = Entry(root, width=30)
    entry_lote.place(x=15, y=175)

    label_qtd = Label(root, text="Quantidade:")
    label_qtd.place(x=10, y=200)
    entry_qtd = Entry(root, width=30)
    entry_qtd.place(x=15, y=225)

    label_prclote = Label(root, text="Preço do LOTE:")
    label_prclote.place(x=10, y=250)
    entry_prclote = Entry(root, width=30)
    entry_prclote.place(x=15, y=275)

    label_prcuni = Label(root, text="Preço unitário")
    label_prcuni.place(x=10, y=300)
    entry_prcuni = Entry(root, width=30)
    entry_prcuni.place(x=15, y=325)

    label_prcvenda = Label(root, text="Preço de venda:")
    label_prcvenda.place(x=10, y=350)
    entry_prcvenda = Entry(root, width=30)
    entry_prcvenda.place(x=15, y=375)

    butao_confirmar = Button(root, text="CONFIRMAR")
    butao_confirmar.place(x=60, y = 450)

    frame_estoque = Frame(root, width=400, height=500)
    frame_estoque.place(x=400, y=50)

    button_cancel = Button(root, text='cancelar', width=10, command=lambda: [clear(), botoes()])
    button_cancel.place(x= 700, y = 600)
    

def salvarprodutos():
    if entry_nome_prod.get() in usuarios.keys():
        tkmsg.showerror("ERRO", "produto já cadastrado")
    elif entry_nome_prod.get() == entry_lote.get():
        usuarios[entry_nome_prod.get()] = entry_lote.get()
        with open("supermercado.json" , "w", encoding="utf-8") as file:
            j.dump(usuarios, file, indent=2)
        tkmsg.showinfo("SUCESSO", "Cadastro feito com sucesso!")
    else:
        tkmsg.showerror("ERRO", "As senhas devem ser iguais")


def carregar_usuarios():
    global usuarios
    if os.path.exists("supermercado.json"):
        try:
            with open("supermercado.json", "r", encoding="utf-8") as arquivo:
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
        with open("supermercado.json" , "w", encoding="utf-8") as file:
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

def rastreamento_de_vendas():
    label_codigo = Label(root, text="Informe o ID do item que deseja rastrear:")
    label_codigo.place(x=275, y=95)
    entry_codigo = Entry(root, width=50)
    entry_codigo.place(x=250, y=115)
    button_cancel = Button(root, text='cancelar', width=10, command=lambda: [clear(), botoes()])
    button_cancel.place(x= 700, y = 600)
    
    

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

def clear():
    for i in root.winfo_children():
        i.destroy()

def botoes():
    frame_buttonsss = Frame(root)
    
    butao_estoque = Button(root, text='GERENCIAR ESTOQUE', width=25, height=10, command=lambda: [clear(), produtos_comprados()])
    butao_estoque.place(x=100, y=220)
    

    butao_produtos = Button(root, text='PRODUTOS COMPRADOS', width=25, height=10, command=clear)
    butao_produtos.place(x=325, y=220)

    butao_rastreamentos = Button(root, text='RASTREAMENTO DE VENDAS', width=25, height=10, command=lambda: [clear(), rastreamento_de_vendas()])
    butao_rastreamentos.place(x=550, y=220)

def main():
    global root
    root = Tk()
    root.geometry("850x700")
    root.title("telamuitotopmesmochave")
    botoes()
    
    root.withdraw()    
    tab_login()    
    root.mainloop()


if __name__ == "__main__":
    carregar_usuarios()
    main()