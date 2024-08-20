from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmsg #Importa o tkinter.messagebox como tkmsg
import json as j
import os

usuarios = {}
estoque = {}


def clear():
    for i in root.winfo_children():
        i.destroy()

def carregar_usuarios():
    global usuarios
    if os.path.exists("supermercado_usuarios.json"):
        try:
            with open("supermercado_usuarios.json", "r", encoding="utf-8") as arquivo:
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
        with open("supermercado_usuarios.json" , "w", encoding="utf-8") as file:
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
   cadastro.geometry('375x300')
   
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

   button_cancel2 = Button(cadastro, text='Cancelar', width=20, command=lambda: [clear(), tab_login()])
   button_cancel2.pack(side=RIGHT, padx=20, pady=20)

def tab_login():
    global login, entry_password, entry_username 
    login = Toplevel(root)
    login.title('Tela de Login')
    login.geometry('375x300')
    
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

    botaopermissao = Radiobutton(frame_buttons, text="Gerente")
    botaopermissao.pack(side=LEFT, padx=5, pady=15)
    
def cadastrar_produto():
    estoque[entry_id_prod.get()] = {"Nome do Produto": entry_nome_prod.get(), 
                                    "Categoria": entry_categoria.get(), 
                                    "Lote": entry_lote.get(), 
                                    "Quantidade": entry_qtd.get(), 
                                    "Preço do Lote": entry_prclote.get(), 
                                    "Preço do Unitario": entry_prcuni.get(),
                                    "Preço de Venda": entry_prcvenda.get()}
    
    tree_estoque.insert("", "end", values=(entry_id_prod.get(), 
                                           entry_nome_prod.get(), 
                                           entry_categoria.get(), 
                                           entry_lote.get(), entry_qtd.get(), f"R$ {entry_prclote.get()}", f"R$ {entry_prcuni.get()}", f"R$ {entry_prcvenda.get()}"))
   
    with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
            j.dump(estoque, file)


def rastrear_vendas():
    global entry_id_prod
    label_verificarID = Label(root, text="Informe abaixo o ID do produto que deseja rastrear:")
    label_verificarID.place(x=390, y=25)
    entry_verificarID = Entry(root, width=50)
    entry_verificarID.place(x=390, y=50)

    label_verificarLOTE = Label(root, text="Informe abaixo o ID do LOTE que deseja rastrear:")
    label_verificarLOTE.place(x=390, y=100)
    entry_verificarLOTE = Entry(root, width=50)
    entry_verificarLOTE.place(x=390, y=125)

    button_cancel = Button(root, text='CANCELAR', width=10, command=lambda: [clear(), botoes()])
    button_cancel.place(x=60, y = 500)

def compra_de_produtos():
    teste = Label(root, text="TELA DE COMPRAS")
    teste.place(x=500, y=10)

    label_campo1 = Label(root, text='Informe aqui o ID do produto que deseja comprar:')
    label_campo1.place(x=10, y=40)
    entry_campo1 = Entry(root, width=30)
    entry_campo1.place(x=10, y = 65)

    butaodeselecao = Radiobutton(root, text="LOTE")
    butaodeselecao.place(x=10, y = 90)

    butaoselecao2 = Radiobutton(root, text="UNIDADE")
    butaoselecao2.place(x=10, y=115)

    button_cancel2 = Button(root, text='Cancelar', width=20, command=lambda: [clear(), tab_estoque()])
    button_cancel2.pack(side=RIGHT, padx=20, pady=20)

def tab_estoque():
    global entry_id_prod, entry_nome_prod, entry_categoria, entry_lote, entry_qtd, entry_prclote, entry_prcuni, entry_prcvenda, tree_estoque

    teste = Label(root, text="ESTOQUE", font="Arial 20")
    teste.place(x=585, y=10)
    
    label_id_prod= Label(root, text="ID")
    label_id_prod.place(x=10, y=0)
    entry_id_prod = Entry(root, width=30)
    entry_id_prod.place(x=15, y=25)

    label_nome_prod= Label(root, text="Nome do Produto:")
    label_nome_prod.place(x=10, y=50)
    entry_nome_prod = Entry(root, width=30)
    entry_nome_prod.place(x=15, y=75)

    label_categoria = Label(root, text="Categoria:")
    label_categoria.place(x=10, y=100)
    entry_categoria = Entry(root, width=30)
    entry_categoria.place(x=15, y=125)

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

    label_prcuni = Label(root, text="Preço Unitário:")
    label_prcuni.place(x=10, y=300)
    entry_prcuni = Entry(root, width=30)
    entry_prcuni.place(x=15, y=325)

    label_prcvenda = Label(root, text="Preço de Venda:")
    label_prcvenda.place(x=10, y=350)
    entry_prcvenda = Entry(root, width=30)
    entry_prcvenda.place(x=15, y=375)

    butao_confirmar = Button(root, text="CONFIRMAR", command= cadastrar_produto)
    butao_confirmar.place(x=60, y = 450)

    button_cancel = Button(root, text='CANCELAR', width=10, command=lambda: [clear(), botoes()])
    button_cancel.place(x=60, y = 500)

    tree_estoque = ttk.Treeview(root, columns=("ID", "Nome do Produto", "Categoria", "Lote","Quantidade", "Preço do Lote", "Preço do Unitário", "Preço de Venda"), show="headings")
    tree_estoque.place(x=275, y=50)

    botao_compra = Button(root, text='Comprar produtos', width=30, command=lambda: [clear(), compra_de_produtos()])
    botao_compra.place(x=830, y=290)

    botaoremover = Button(root, text="Remover produtos", width = 30, command=None)
    botaoremover.place(x = 600, y = 290)

    
    for i in ["ID", "Nome do Produto", "Categoria", "Lote","Quantidade", "Preço do Lote", "Preço do Unitário", "Preço de Venda"]:
        tree_estoque.heading(f"{i}", text=f"{i}")
    tree_estoque.column("ID", width=50)
    tree_estoque.column("Nome do Produto", width=150)
    tree_estoque.column("Categoria", width=100)
    tree_estoque.column("Lote", width=100)
    tree_estoque.column("Quantidade", width=75)
    tree_estoque.column("Preço do Lote", width=100)
    tree_estoque.column("Preço do Unitário", width=100)
    tree_estoque.column("Preço de Venda", width=100)

    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_estoque.yview)
    scrollbar.place(x=1050, y=50, height=225)

    tree_estoque.configure(yscrollcommand=scrollbar.set)

def botoes():
    frame_buttonsss = Frame(root)
   
    butao_estoque = Button(root, text='GERENCIAR ESTOQUE', width=30, height=10, command=lambda: [clear(), tab_estoque()])
    butao_estoque.place(x=100, y=220)
   
 
    butao_produtos = Button(root, text='PRODUTOS COMPRADOS', width=30, height=10, command=clear)
    butao_produtos.place(x=450, y=220)
 
    butao_rastreamentos = Button(root, text='RASTREAMENTO DE VENDAS', width=30, height=10, command=lambda: [clear(), rastrear_vendas()])
    butao_rastreamentos.place(x=795, y=220)

def main():
    global root
    root = Tk()
    root.geometry("1100x650")
    root.title("telamuitotopmesmochave")
    botoes()

    root.withdraw()
    tab_login()
    root.mainloop()

if __name__ == "__main__":
    carregar_usuarios()
    main()