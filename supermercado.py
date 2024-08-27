from tkinter import *
from tkinter import ttk
from datetime import datetime
import tkinter.messagebox as tkmsg #Importa o tkinter.messagebox como tkmsg
import json as j
import os
 
usuarios = {}
estoque = {}

def cleardois():
    for i in login.winfo_children():
        i.destroy()
 
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
 
def carregar_estoque():
    global estoque
    if os.path.exists("supermercado_estoque.json"):
        try:
            with open("supermercado_estoque.json", "r", encoding="utf-8") as arquivo:
                estoque = j.load(arquivo)
        except j.JSONDecodeError:
            estoque = {}
    else:
        estoque = {}
 
def informacoes_tree_estoque():
     for i in estoque:
                    tree_estoque.insert("", "end", values=(i,
                                                        estoque[i]["Nome do Produto"],
                                                        estoque[i]["Categoria"],
                                                        estoque[i]["Validade"],
                                                        estoque[i]["Quantidade"],
                                                        f"R$ {estoque[i]['Preço do Lote']}",
                                                        f"R$ {estoque[i]['Preço do Unitario']}",
                                                        f"R$ {estoque[i]['Preço de Venda']}"))
def informacoes_tree_ordem_de_compra():
     for i in estoque:
        if estoque[i]["Quantidade"] < 30:
            tree_ordemdecompra.insert("", "end",values=(i, 
                                                        estoque[i]["Nome do Produto"], 
                                                        estoque[i]["Categoria"],
                                                        estoque[i]["Quantidade"],
                                                        "Quantidade em estoque",
                                                        "Pendente"
                                                        ))
        
        data_str = estoque[i]["Validade"]
        data_converçao = datetime.strptime(data_str, "%d/%m/%Y")
        
        if data_converçao < datetime.now():
              tree_ordemdecompra.insert("", "end",values=(i, 
                                                        estoque[i]["Nome do Produto"], 
                                                        estoque[i]["Categoria"],
                                                        estoque[i]["Quantidade"],
                                                        "Validade",
                                                        "Pendente"
                                                        ))
            
def verficar_cadastro():
    if entry_username2.get() in usuarios.keys():
        tkmsg.showerror("ERRO", "Usuario já cadastrado")
    elif "" in (entry_username2.get(), entry_password2.get(), entry_password3.get()):
         tkmsg.showerror("ERRO", "Preencha todos os campos")
    elif entry_password2.get() == entry_password3.get():
        usuarios[entry_username2.get()] = entry_password3.get()
        with open("supermercado_usuarios.json" , "w", encoding="utf-8") as file:
            j.dump(usuarios, file, indent=2)
        tkmsg.showinfo("SUCESSO", "Cadastro feito com sucesso!")
        cleardois()
        tab_login() 
    else:
        tkmsg.showerror("ERRO", "As senhas devem ser iguais")

def verificar_login():
    global password
    username = entry_username.get()
    password = entry_password.get()
 
    for i in usuarios:
        if i == username:
            if usuarios[username] == password:
                root.deiconify()
                login.destroy()
                break
    else:
        tkmsg.showinfo("ERRO", "Login inválido")
        
def remocao_de_produtos():
        selected_item = tree_estoque.selection()
        if not selected_item:
             tkmsg.showerror("ERRO", "Não ha nenhum item selecionado")
        else:
            item_id = tree_estoque.item(selected_item, "values")[0]
            str(item_id)
            del estoque[item_id]
            tree_estoque.delete(selected_item)
            with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
                        j.dump(estoque, file, indent=2)

 
def editar_produto():       #Função para realizar a compra de produtos novos
    select_item = tree_estoque.selection()
    
    if select_item:
        item_id = tree_estoque.item(select_item, "values")[0]
        item_nome = tree_estoque.item(select_item, "values")[1]
        item_categoria = tree_estoque.item(select_item, "values")[2]
        item_validade = tree_estoque.item(select_item, "values")[3]
        item_quantidade = tree_estoque.item(select_item, "values")[4]
        item_prclote = tree_estoque.item(select_item, "values")[5]
        item_prclote_div1 = item_prclote.split("R$ ")
        item_prclote_div2 = item_prclote_div1[1].split(".")
        item_prclote_div2.pop(1)
        item_prcuni = tree_estoque.item(select_item, "values")[6]
        item_prcuni_div1 = item_prcuni.split("R$ ")
        item_prcuni_div2 = item_prcuni_div1[1].split(".")
        item_prcuni_div2.pop(1)
        item_prcvenda = tree_estoque.item(select_item, "values")[7]
        item_prcvenda_div1 = item_prcvenda.split("R$ ")
        item_prcvenda_div2 = item_prcvenda_div1[1].split(".")
        item_prcvenda_div2.pop(1)

        entry_id_prod.delete(0, END)
        entry_id_prod.insert(0, item_id)
        entry_id_prod.config(state="disabled")

        entry_nome_prod.delete(0, END)
        entry_nome_prod.insert(0, item_nome)

        entry_categoria.delete(0, END)
        entry_categoria.insert(0, item_categoria)
        
        entry_validade.delete(0, END)
        entry_validade.insert(0, item_validade)

        entry_qtd.delete(0, END)
        entry_qtd.insert(0, item_quantidade)
        
        entry_prclote.delete(0, END)
        entry_prclote.insert(0, item_prclote_div2)

        entry_prcuni.delete(0, END)
        entry_prcuni.insert(0, item_prcuni_div2)

        entry_prcvenda.delete(0, END)
        entry_prcvenda.insert(0, item_prcvenda_div2)
        
        del estoque[item_id]
        tree_estoque.delete(select_item)
        with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
                        j.dump(estoque, file, indent=2)
        
def cadastrar_produto():
    data_str = entry_validade.get()
   
    try:
        data_converçao = datetime.strptime(data_str, "%d/%m/%Y")
        
        if data_converçao < datetime.now():
            tkmsg.showerror("ERRO", "Este produto pode ja estar vencido!")
            return
    
    except ValueError:
            tkmsg.showerror("ERRO", "Formato de data inválido. Por favor, use o formato dd/mm/yyyy.")
            return
    
    if "" in (entry_nome_prod.get(), entry_categoria.get(), entry_validade.get(), entry_prclote.get(), entry_prcuni.get(), entry_prcvenda.get()):
        tkmsg.showerror("ERRO", "Preencha todos os campos")
        return
    
    if not entry_id_prod.get().isnumeric():
            tkmsg.showerror("ERRO", "Insira apenas números no ID")
            
    
    if entry_id_prod.get() in estoque:
        tkmsg.showerror("ERRO", "Este ID ja existe")
        return
   
    if not entry_qtd.get().isnumeric():
        tkmsg.showerror("ERRO", "Insira apenas números na quantidade")
        return
         
    if not entry_prclote.get().isnumeric():
            tkmsg.showerror("ERRO", "Insira apenas números no preço do lote")
            return
   
    if not entry_prcuni.get().isnumeric():
            tkmsg.showerror("ERRO", "Insira apenas números no preço do unitário")
            return
   
    if not entry_prcvenda.get().isnumeric():
            tkmsg.showerror("ERRO", "Insira apenas números no preço de venda")
            return
    validade = entry_validade.get().split("/")
    for i in validade:
        if not i.isnumeric():
            tkmsg.showerror("ERRO", "Insira apenas números como validade")    
            break
    
    estoque[entry_id_prod.get()] = {"Nome do Produto": entry_nome_prod.get(),
                                        "Categoria": entry_categoria.get(),
                                        "Validade": entry_validade.get(),
                                        "Quantidade": int(entry_qtd.get()),
                                        "Preço do Lote": float(entry_prclote.get()),
                                        "Preço do Unitario": float(entry_prcuni.get()),
                                        "Preço de Venda": float(entry_prcvenda.get())}
       
    tree_estoque.insert("", "end", values=(entry_id_prod.get(),
                                            entry_nome_prod.get(),
                                            entry_categoria.get(),
                                            entry_validade.get(), entry_qtd.get(), f"R$ {entry_prclote.get()}", f"R$ {entry_prcuni.get()}", f"R$ {entry_prcvenda.get()}"))
   
    with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
                j.dump(estoque, file, indent=2)
    
    entry_id_prod.config(state="normal")

def tab_cadastro():
    global entry_username2, entry_password2, entry_password3, gerentin, funcionario

    label_username2 = Label(login, text='nome de usuário:')
    label_username2.pack()
    entry_username2 = Entry(login, width=30)
    entry_username2.pack(pady=5)
    
    label_password2 = Label(login, text='Senha:')
    label_password2.pack()
    entry_password2 = Entry(login, show='*', width=30)
    entry_password2.pack(pady=5)
   
    label_confirm = Label(login, text='Confirmar senha')
    label_confirm.pack()
    entry_password3 = Entry(login, show='*', width=30)
    entry_password3.pack(pady=5)

    button_confirm = Button(login, text='Cadastrar', width=20, command=verficar_cadastro)
    button_confirm.pack(padx=10, pady=10)
 
    button_cancel2 = Button(login, text='Cancelar', width=20, command=lambda: [cleardois(), tab_login()])
    button_cancel2.pack(padx=10, pady=10)
 
def tab_login():
    global login, entry_password, entry_username
    
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
   
    button_login = Button(frame_buttons, text='login', width=10, command=lambda: [verificar_login(), botoes()])
    button_login.pack(side=LEFT, padx=10)
   
    button_cancel = Button(frame_buttons, text='cancelar', width=10, command=login.quit)
    button_cancel.pack(side=RIGHT, padx=10)
   
    button_createAccount = Button(frame_buttons, text='Criar Conta', width=20, command=lambda: [cleardois(), tab_cadastro()])
    button_createAccount.pack(side=RIGHT, padx=20)
 
def tab_estoque():
    global entry_id_prod, entry_nome_prod, entry_categoria, entry_validade, entry_qtd, entry_prclote, entry_prcuni, entry_prcvenda, tree_estoque
   
    label_id_prod= Label(root, text="ID")
    label_id_prod.place(x=10, y=0)
    entry_id_prod = Entry(root, width=30)
    entry_id_prod.place(x=15, y=25)
 
    label_nome_prod= Label(root, text="Nome do Produto")
    label_nome_prod.place(x=10, y=50)
    entry_nome_prod = Entry(root, width=30)
    entry_nome_prod.place(x=15, y=75)
 
    label_categoria = Label(root, text="Categoria:")
    label_categoria.place(x=10, y=100)
    entry_categoria = Entry(root, width=30)
    entry_categoria.place(x=15, y=125)
 
    label_validade = Label(root, text="Validade:")
    label_validade.place(x=10, y=150)
    entry_validade = Entry(root, width=30)
    entry_validade.place(x=15, y=175)
 
    label_qtd = Label(root, text="Quantidade:")
    label_qtd.place(x=10, y=200)
    entry_qtd = Entry(root, width=30)
    entry_qtd.place(x=15, y=225)
 
    label_prclote = Label(root, text="Preço do LOTE")
    label_prclote.place(x=10, y=250)
    entry_prclote = Entry(root, width=30)
    entry_prclote.place(x=15, y=275)
 
    label_prcuni = Label(root, text="Preço Unitário")
    label_prcuni.place(x=10, y=300)
    entry_prcuni = Entry(root, width=30)
    entry_prcuni.place(x=15, y=325)
 
    label_prcvenda = Label(root, text="Preço de Venda:")
    label_prcvenda.place(x=10, y=350)
    entry_prcvenda = Entry(root, width=30)
    entry_prcvenda.place(x=15, y=375)
 
    butao_confirmar = Button(root, text="Cadastrar", command=cadastrar_produto)
    butao_confirmar.place(x=60, y = 450)
 
    button_cancel = Button(root, text='VOLTAR', width=10, command=lambda: [clear(), botoes()])
    button_cancel.place(x=965, y = 10)
 
    botao_compra = Button(root, text='Editar produto', width=30, command=editar_produto)
    botao_compra.place(x=830, y=450)
 
    botaoremover = Button(root, text="Remover produto", width = 30, command=remocao_de_produtos)
    botaoremover.place(x = 600, y = 450)
 
    label_estoque = Label(root, text="ESTOQUE", font=("Arial", 20, "bold"))
    label_estoque.place(x=585, y=10)
 
    tree_estoque = ttk.Treeview(root, columns=("ID","Nome do Produto", "Categoria", "Validade","Quantidade", "Preço do Lote", "Preço do Unitário", "Preço de Venda"), show="headings", height=18 )
    tree_estoque.place(x=275, y=50)
   
    for i in ["ID", "Nome do Produto", "Categoria", "Validade","Quantidade", "Preço do Lote", "Preço do Unitário", "Preço de Venda"]:
        tree_estoque.heading(f"{i}", text=f"{i}")
 
    tree_estoque.column("ID", width=50, anchor="center")
    tree_estoque.column("Nome do Produto", width=150, anchor="center")
    tree_estoque.column("Categoria", width=100, anchor="center")
    tree_estoque.column("Validade", width=100, anchor="center")
    tree_estoque.column("Quantidade", width=75, anchor="center")
    tree_estoque.column("Preço do Lote", width=100, anchor="center")
    tree_estoque.column("Preço do Unitário", width=100, anchor="center")
    tree_estoque.column("Preço de Venda", width=100, anchor="center")
 
    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_estoque.yview)
    scrollbar.place(x=1050, y=49, height=388)
 
    tree_estoque.configure(yscrollcommand=scrollbar.set)

def tab_ordem_de_compra():
    global tree_ordemdecompra

    titulo = Label(root, text="ORDEM DE COMPRA", font=("Arial", 20, "bold"))
    titulo.pack(padx=10, pady=10)
   
    botaopacancela = Button(root, text="VOLTAR", command= lambda: [clear(), botoes()])
    botaopacancela.place(x=870, y = 15)
 
    tree_ordemdecompra = ttk.Treeview(root, columns=("ID", "Nome do Produto", "Categoria","Quantidade", "Motivo", "Status"), show="headings", height=18)
    tree_ordemdecompra.pack(padx=20, pady=20)
 
    for i in ["ID", "Nome do Produto", "Categoria","Quantidade", "Motivo", "Status"]:
        tree_ordemdecompra.heading(f"{i}", text=f"{i}")
   
    tree_ordemdecompra.column("ID", width=75, anchor="center")
    tree_ordemdecompra.column("Nome do Produto", width=200, anchor="center")
    tree_ordemdecompra.column("Categoria", width=150, anchor="center")
    tree_ordemdecompra.column("Quantidade", width=125, anchor="center")
    tree_ordemdecompra.column("Motivo", width=150, anchor="center")
    tree_ordemdecompra.column("Status", width=125, anchor="center")
 
    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_ordemdecompra.yview)
    scrollbar.place(x=950, y=75, height=390)
 
    tree_ordemdecompra.configure(yscrollcommand=scrollbar.set)
 
def botoes():
    if password == "123":
        butao_estoque = Button(root, text='GERENCIAR ESTOQUE', width=30, height=10, command=lambda: [clear(), tab_estoque(), informacoes_tree_estoque()])
        butao_estoque.place(x=100, y=220)
        
        butao_produtos = Button(root, text='ORDEM DE COMPRA', width=30, height=10, command=lambda: [clear(), tab_ordem_de_compra(), informacoes_tree_ordem_de_compra()])
        butao_produtos.place(x=450, y=220)
        
        butao_rastreamentos = Button(root, text='RASTREAMENTO DE VENDAS', width=30, height=10, command=lambda: [clear()])
        butao_rastreamentos.place(x=795, y=220)
    
    else:
        labelID = Label(root, text="ID do produto")
        labelID.place(x = 40, y=100)
        entryID = Entry(root, width=30)
        entryID.place(x= 40, y = 120)
 
        labelQTD = Label(root, text="Quantidade:")
        labelQTD.place(x = 40, y=160)
        entryQTD = Entry(root, width=30)
        entryQTD.place(x = 40, y =180)
 
        tree_funcionario = ttk.Treeview(root, columns=("ID","Nome do Produto", "Categoria", "Quantidade", "Preço"), show="headings", height=18 )
        tree_funcionario.place(x=275, y=50)
   
        for i in ["ID", "Nome do Produto", "Categoria", "Quantidade", "Preço"]:
            tree_funcionario.heading(f"{i}", text=f"{i}")
 
        tree_funcionario.column("ID", width=50, anchor="center")
        tree_funcionario.column("Nome do Produto", width=150, anchor="center")
        tree_funcionario.column("Categoria", width=100, anchor="center")
        tree_funcionario.column("Quantidade", width=75, anchor="center")
        tree_funcionario.column("Preço", width=100, anchor="center")
 
        scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_funcionario.yview)
        scrollbar.place(x=1050, y=49, height=388)
        
        tree_funcionario.configure(yscrollcommand=scrollbar.set)

def esquema_tela_inicial():                       # O ESQUEMA DE CONSEGUIR REALIZAR O CADASTRO SEM TER QUE ABRIR OUTRA JANELA
    global login

    login = Tk()
    login.title('Tela de Login')
    login.geometry('500x400')
    tab_login()

def main():
    global root

    root = Tk()
    root.geometry("1100x650")
    root.title("telamuitotopmesmochave")

    root.withdraw()
    esquema_tela_inicial()
    root.mainloop()

if __name__ == "__main__":
    carregar_usuarios()
    carregar_estoque()
    main()