from tkinter import *
from tkinter import ttk
from datetime import datetime
import tkinter.messagebox as tkmsg #Importa o tkinter.messagebox como tkmsg
import json as j
import os
 
usuarios = {}
estoque = {}
historico = {}
carrinho = {}
valor = 0
cont = 1

def deteste():
     root.withdraw()
     
def cleardois():
    for i in login.winfo_children():
        i.destroy()
 
def clear():
    for i in root.winfo_children():
        i.destroy()

def voltar():
    yesno = tkmsg.askyesno("Confirmação","Você tem certeza que deseja voltar ao menu principal? Informações não salvas ou produtos com edições não salvas serão perdidos.")

    if yesno:
        clear()
        botoes()

def alertas():
    baixa_quantidade = []
    vencido = []

    for i in estoque:

        if estoque[i]["Quantidade"] < 30:
            baixa_quantidade.append(i)
        
        data_str = estoque[i]["Validade"]
        data_converçao = datetime.strptime(data_str, "%d/%m/%Y")
        
        if data_converçao < datetime.now():
            vencido.append(i)
    
    if len(baixa_quantidade) > 0:
        baixa_quantidade.sort()
        tkmsg.showinfo("Produtos Acabando", f"ID: {",".join(baixa_quantidade)}\nVerifique a pagina de alertas para mais informações")
    
    if len(vencido) > 0:
        vencido.sort()
        tkmsg.showinfo("Produtos Vencidos", f"ID: {",".join(vencido)}\nVerifique a pagina de alertas para mais informações")

def alterar_status():
    select_item = tree_alertas.selection()

    if select_item:
        valores = tree_alertas.item(select_item, "values")
        item_id = valores[0]  
        item_nome = valores[1]
        item_categoria = valores[2]
        item_quantidade = valores[3]
        item_motivo = valores[4]
        item_status = valores[5]

        if item_status == "Pendente":
            item_status = "Em Andamento"
        
        elif item_status == "Em Andamento":
            tree_alertas.delete(select_item)
            return     
        
        tree_alertas.item(select_item, values=(valores[0], item_nome, item_categoria, item_quantidade, item_motivo, item_status))
    elif not select_item:
        tkmsg.showerror("ERRO", "Selecione um produto para usar esta função")

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
    
    dels = []
    if os.path.exists("supermercado_estoque.json"):
    
        try:
            with open("supermercado_estoque.json", "r", encoding="utf-8") as arquivo:
                estoque = j.load(arquivo)
                for i in estoque:
                    if estoque[i]["Quantidade"] <= 0:
                        dels.append(i)
                for k in dels:
                    del estoque[k]
                     
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
def informacoes_tree_alertas():
     for i in estoque:
       
        if estoque[i]["Quantidade"] < 30:
            tree_alertas.insert("", "end",values=(i, 
                                                        estoque[i]["Nome do Produto"], 
                                                        estoque[i]["Categoria"],
                                                        estoque[i]["Quantidade"],
                                                        "Quantidade em estoque",
                                                        "Pendente"
                                                        ))
        
        data_str = estoque[i]["Validade"]
        data_converçao = datetime.strptime(data_str, "%d/%m/%Y")
        
        if data_converçao < datetime.now():
              tree_alertas.insert("", "end",values=(i, 
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
        usuarios[entry_username2.get()] = {"Senha": entry_password3.get(), "Cargo": cargo_var.get()}
        with open("supermercado_usuarios.json" , "w", encoding="utf-8") as file:
            j.dump(usuarios, file, indent=2)
        tkmsg.showinfo("SUCESSO", "Cadastro feito com sucesso!")
   

    else:
        tkmsg.showerror("ERRO", "As senhas devem ser iguais")

def verificar_login():
    global username, password, loginTRUEouFALSE

    username = entry_username.get()
    password = entry_password.get()
    loginTRUEouFALSE = False
 
    for i in usuarios:

        if i == username:

            if usuarios[username]["Senha"] == password:
                root.deiconify()
                login.destroy()
                loginTRUEouFALSE = True
                break
    else:
        tkmsg.showinfo("ERRO", "Login inválido")


        
def remocao_de_produtos(tree):
        selected_item = tree.selection()
        if not selected_item:
            tkmsg.showerror("ERRO", "Selecione um produto para usar esta função")
        else:
            item_id = tree.item(selected_item, "values")[0]
            str(item_id)
            del estoque[item_id]
            tree.delete(selected_item)
            with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
                        j.dump(estoque, file, indent=2)

def transferir_produtos():
    try:

        int(entry_QTD.get())
        if int(entry_QTD.get()) > estoque[entry_ID.get()]["Quantidade"]:
            tkmsg.showerror("ERRO", "O estoque não possui esta quantidades de items")
            return
        
        else:
            remover = estoque[entry_ID.get()]["Quantidade"] - int(entry_QTD.get())
            estoque[entry_ID.get()]["Quantidade"] = remover

            tree_estoque.item(select_item, values=(entry_ID.get(),
                                                    estoque[entry_ID.get()]["Nome do Produto"], 
                                                    estoque[entry_ID.get()]["Categoria"],
                                                    estoque[entry_ID.get()]["Validade"], 
                                                    remover,
                                                    estoque[entry_ID.get()]["Preço do Lote"],
                                                    estoque[entry_ID.get()]["Preço do Unitario"],
                                                    estoque[entry_ID.get()]["Preço de Venda"]))
                
                
            with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
                                    j.dump(estoque, file, indent=2)
            transferir.destroy()

    except ValueError:
         tkmsg.showerror("ERRO", "Insira apenas número inteiros na quantidade")
         return

def editar_produto():       #Função para realizar a compra de produtos novos
    select_item = tree_estoque.selection()
    botao_cadastrar.config(text="Finalizar Edição")
    
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
    elif not select_item:
        tkmsg.showerror("ERRO", "Selecione um produto para usar esta função")
        
def cadastrar_produto():
    data_str = entry_validade.get()
    botao_cadastrar.config(text="Cadastrar Produto")
   
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
            return
    
    if entry_id_prod.get() in estoque:
        tkmsg.showerror("ERRO", "Este ID ja existe")
        return
   
    if not entry_qtd.get().isnumeric():
        tkmsg.showerror("ERRO", "Insira apenas números na quantidade")
        return
    
    if int(entry_qtd.get()) == 0:
        tkmsg.showerror("ERRO", "Não insira quantidade como 0")
        return
    
    try:
        float(entry_prclote.get())
    
    except ValueError:        
        tkmsg.showerror("ERRO", "Insira apenas números no preço do lote")
        return
    
    try:
        float(entry_prcuni.get())

    except ValueError:
        tkmsg.showerror("ERRO", "Insira apenas números no preço do unitário")
        return

    try:
        float(entry_prcvenda.get())
    
    except ValueError:
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
                                            entry_validade.get(), 
                                            int(entry_qtd.get()), 
                                            f"R$ {float(entry_prclote.get())}", 
                                            f"R$ {float(entry_prcuni.get())}", 
                                            f"R$ {float(entry_prcvenda.get())}"))

    with open("supermercado_estoque.json" , "w", encoding="utf-8") as file:
                        j.dump(estoque, file, indent=2)

    entry_nome_prod.delete(0, END)
    entry_categoria.delete(0, END)
    entry_validade.delete(0, END)
    entry_qtd.delete(0, END)
    entry_prclote.delete(0, END)
    entry_prcuni.delete(0, END)
    entry_prcvenda.delete(0, END)
    entry_id_prod.config(state="normal")
    entry_id_prod.delete(0, END)

def retirar_produto():
    global select_item

    select_item = tree_estoque.selection()

    if select_item:
        tab_transferir_produtos()    
        valores = tree_estoque.item(select_item, "values")
        item_id = valores[0]  
        item_nome = valores[1]

        entry_ID.insert(0, item_id)
        entry_ID.config(state="disabled")

        entry_NOME.insert(0, item_nome)
        entry_NOME.config(state="disabled")

    if not select_item:
        tkmsg.showerror("ERRO", "Selecione um produto para usar esta função")
     
def inserir_produto():
    global valor

    if entryID.get() in estoque:

        if int(entryQTD.get()) > estoque[entryID.get()]["Quantidade"]:
            tkmsg.showwarning("AVISO!", "Este produto não possui estoque! Verifique com o repositor.")

        carrinho[entryID.get()] = {"Nome do Produto": estoque[entryID.get()]["Nome do Produto"],
                                   "Categoria": estoque[entryID.get()]["Categoria"],
                                   "Quantidade": entryQTD.get(),
                                   "Preço Unitario": estoque[entryID.get()]["Preço de Venda"],
                                   "Preço": estoque[entryID.get()]["Preço de Venda"]*float(entryQTD.get())} 
         
        tree_funcionario.insert("", END, values=(entryID.get(),
                                                 estoque[entryID.get()]["Nome do Produto"], 
                                                 estoque[entryID.get()]["Categoria"],
                                                 entryQTD.get(),
                                                 estoque[entryID.get()]["Preço de Venda"],
                                                 estoque[entryID.get()]["Preço de Venda"]*float(entryQTD.get())))
        
        valor += estoque[entryID.get()]["Preço de Venda"]*float(entryQTD.get())
        label_preçototal.config(text=f"Preço Total: R${valor}")

    elif not entryID.get().isnumeric():
        tkmsg.showerror("ERRO", "Insira apenas números como ID.")

    else:
         tkmsg.showerror("ERRO", "Não existe produto com este ID.")      

def finalizar_compra():
    global valor
    for i in carrinho:
        notinha = tkmsg.showinfo("COMPRA FINALIZADA", f"Produtos comprados:\nProduto: {carrinho[i]["Nome do Produto"]}, Quantidade: {carrinho[i]["Quantidade"]}, Preço: {carrinho[i]["Preço"]}\nForma de Pagamento:{pagamento_var.get()}\nPreço Total: {valor}")

def tab_historico():
    global tree_historico

    labeldohistoricofx = Label(root, text="HISTÓRICO DE VENDAS", background='green', fg="white", font=("Arial",14), width=100)
    labeldohistoricofx.place(x=0, y=20)

    tree_historico = ttk.Treeview(root, columns=("ID","Nome do Produto", "Categoria", "Validade","Quantidade", "Preço do Lote", "Preço do Unitário", "Preço de Venda"), show="headings", height=24 )
    tree_historico.place(x=50, y=90)
   
    for i in ["ID", "Nome do Produto", "Categoria", "Validade","Quantidade", "Preço do Lote", "Preço do Unitário", "Preço de Venda"]:
        tree_historico.heading(f"{i}", text=f"{i}")
 
    tree_historico.column("ID", width=75, anchor="center")
    tree_historico.column("Nome do Produto", width=175, anchor="center")
    tree_historico.column("Categoria", width=125, anchor="center")
    tree_historico.column("Validade", width=125, anchor="center")
    tree_historico.column("Quantidade", width=100, anchor="center")
    tree_historico.column("Preço do Lote", width=125, anchor="center")
    tree_historico.column("Preço do Unitário", width=125, anchor="center")
    tree_historico.column("Preço de Venda", width=125, anchor="center")
 
    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_historico.yview)
    scrollbar.place(x=1030, y=90, height=500)
 
    tree_historico.configure(yscrollcommand=scrollbar.set)

    botaopacancela = Button(root, text="VOLTAR", command= lambda: [clear(), botoes()], width=25)
    botaopacancela.place(x=50, y=600)       

def tab_cadastro():
    global entry_username2, entry_password2, entry_password3, cargo_var
 
    label_username2 = Label(root, text='nome de usuário:')
    label_username2.pack()
    entry_username2 = Entry(root, width=30)
    entry_username2.pack(pady=5)
   
    label_password2 = Label(root, text='Senha:')
    label_password2.pack()
    entry_password2 = Entry(root, show='*', width=30)
    entry_password2.pack(pady=5)
   
    label_confirm = Label(root, text='Confirmar senha')
    label_confirm.pack()
    entry_password3 = Entry(root, show='*', width=30)
    entry_password3.pack(pady=5)
   
    framebuttttton = Frame(root)
    framebuttttton.pack(pady=10)
    
    button_cadastrar = Button(root, text='Cadastrar', width=20, command=verficar_cadastro)
    button_cadastrar.pack(padx=10, pady=10)
 
    botao_cancelar = Button(root, text='Cancelar', width=20, command=lambda: [clear(), botoes()])
    botao_cancelar.pack(padx=10, pady=10)
 
    cargo_var = StringVar()
    cargo_var.set(None)

    radio1 = Radiobutton(framebuttttton, text='Caixa', variable=cargo_var, value="Caixa")
    radio1.pack()
 
    radio2 = Radiobutton(framebuttttton, text="Gerente", variable=cargo_var, value="Gerente")
    radio2.pack()

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
   
    botao_cancelars = Button(frame_buttons, text='cancelar', width=10, command=login.quit)
    botao_cancelars.pack(side=RIGHT, padx=10)
 
def tab_estoque():
    global entry_id_prod, entry_nome_prod, entry_categoria, entry_validade, entry_qtd, entry_prclote, entry_prcuni, entry_prcvenda, tree_estoque, botao_cadastrar
   
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
 
    label_prclote = Label(root, text="Preço do Lote")
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
 
    botao_cadastrar = Button(root, text="Cadastrar", command=cadastrar_produto)
    botao_cadastrar.place(x=60, y = 450)
 
    botao_voltar = Button(root, text='VOLTAR', width=10, command=voltar)
    botao_voltar.place(x=965, y = 10)
 
    botao_editar = Button(root, text='Editar produto', width=30, command=editar_produto)
    botao_editar.place(x=830, y=450)
 
    botaoremover = Button(root, text="Remover produto", width = 30, command=lambda: [remocao_de_produtos(tree_estoque)])
    botaoremover.place(x = 600, y = 450)

    butaoderetransferirproduto = Button(root, text="Transferir produto", width=30, command=lambda: [retirar_produto()])
    butaoderetransferirproduto.place(x=370, y = 450)
 
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

def tab_alertas():
    global tree_alertas

    titulo = Label(root, text="ALERTAS", font=("Arial", 20, "bold"))
    titulo.pack(padx=10, pady=10)
   
    botaopacancela = Button(root, text="VOLTAR", command= lambda: [clear(), botoes()])
    botaopacancela.place(x=870, y = 15)

    botao_status = Button(root, text='Alterar Status', width=30, command=alterar_status)
    botao_status.place(x=725, y=475)
 
    tree_alertas = ttk.Treeview(root, columns=("ID", "Nome do Produto", "Categoria","Quantidade", "Motivo", "Status"), show="headings", height=18)
    tree_alertas.pack(padx=20, pady=20)
 
    for i in ["ID", "Nome do Produto", "Categoria","Quantidade", "Motivo", "Status"]:
        tree_alertas.heading(f"{i}", text=f"{i}")
   
    tree_alertas.column("ID", width=75, anchor="center")
    tree_alertas.column("Nome do Produto", width=200, anchor="center")
    tree_alertas.column("Categoria", width=150, anchor="center")
    tree_alertas.column("Quantidade", width=125, anchor="center")
    tree_alertas.column("Motivo", width=150, anchor="center")
    tree_alertas.column("Status", width=125, anchor="center")
 
    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_alertas.yview)
    scrollbar.place(x=950, y=75, height=390)
 
    tree_alertas.configure(yscrollcommand=scrollbar.set)

def tab_transferir_produtos():
     global entry_ID, entry_NOME, entry_QTD, entry_MTV, transferir

     transferir  = Toplevel(root)
     transferir.geometry("600x600")
     transferir.title("Transeferencia de Produtos")

     label_IDprod = Label(transferir, text="ID:")
     label_IDprod.pack(padx=10, pady=10)
     entry_ID = Entry(transferir, width=30)
     entry_ID.pack(padx=10, pady=10)
 
     label_NOME = Label(transferir, text="Nome:")
     label_NOME.pack(padx=10, pady=5)
     entry_NOME = Entry(transferir, width=30)
     entry_NOME.pack(padx=10, pady=5)

     label_QTD = Label(transferir, text="Quantidade:")        #QTD é "Quantidade"
     label_QTD.pack(padx=10, pady=5)
     entry_QTD = Entry(transferir, width=30)
     entry_QTD.pack(padx=10, pady=5)
 
     label_MTV = Label(transferir, text="MOTIVO:")         #MTV é "Motivo"
     label_MTV.pack(padx=10, pady=5)
     entry_MTV = Entry(transferir, width=30)
     entry_MTV.pack(padx=10, pady=5)
 
     buttonpaconfirma = Button(transferir, text='CONFIRMAR', width=15, command=transferir_produtos)
     buttonpaconfirma.pack(padx=10, pady=10)
 
     buttoncancel = Button(transferir, text='CANCELAR', width=15, command=transferir.destroy)
     buttoncancel.pack(padx=10, pady=10)

def tab_caixa():
    global entryID, entryQTD, pagamento_var, tree_funcionario, label_preçototal

    labeldafaixa = Label(root, text="Supermercado top", background='green', fg="white", font=("Arial",14), width=100)
    labeldafaixa.place(x=0, y=20)
       
    labelID = Label(root, text="ID do produto")
    labelID.place(x = 40, y=75)
    entryID = Entry(root, width=30)
    entryID.place(x= 40, y = 100)
 
    labelQTD = Label(root, text="Quantidade:")
    labelQTD.place(x = 40, y=130)
    entryQTD = Entry(root, width=30)
    entryQTD.place(x = 40, y =150)

    label_preçototal = Label(root, text=f"Preço Total: {valor}", font=("Arial", 20, "bold"))
    label_preçototal.place(x=725, y=475)

    buttonCONFIRM = Button(root, text="CONFIRMAR", command=inserir_produto)
    buttonCONFIRM.place(x=90, y=225)

    pagamento_var = StringVar()
    pagamento_var.set(None)

    PIX = Radiobutton(root, text='PIX', variable=pagamento_var, value="Pix")
    PIX.place(x=755, y=525)

    CARTAO = Radiobutton(root, text="Cartão de Crédito", variable=pagamento_var, value="Cartao de Credito")
    CARTAO.place(x=755, y=550)

    CARTAODEBITO = Radiobutton(root, text="Cartão de Débito", variable=pagamento_var, value="Cartao de Debito")
    CARTAODEBITO.place(x=755, y=575)
        
    DINHEIRO = Radiobutton(root, text='Dinheiro', variable=pagamento_var,  value="Dinheiro")
    DINHEIRO.place(x=755, y=600)

    button_finalizarcompra = Button(root, text="FINALIZAR COMPRA", command=finalizar_compra)
    button_finalizarcompra.place(x=900, y=615)

    tree_funcionario = ttk.Treeview(root, columns=("ID","Nome do Produto", "Categoria", "Quantidade", "Preço do Unitário", "Valor"), show="headings", height=18)
    tree_funcionario.place(x=275, y=75)

    for i in ["ID", "Nome do Produto", "Categoria", "Quantidade", "Preço do Unitário", "Valor"]:
        tree_funcionario.heading(f"{i}", text=f"{i}")

    tree_funcionario.column("ID", width=75, anchor="center")
    tree_funcionario.column("Nome do Produto", width=150, anchor="center")
    tree_funcionario.column("Categoria", width=120, anchor="center")
    tree_funcionario.column("Quantidade", width=100, anchor="center")
    tree_funcionario.column("Preço do Unitário", width=120, anchor="center")
    tree_funcionario.column("Valor", width=120, anchor="center")

    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree_funcionario.yview)
    scrollbar.place(x=945, y=75, height=389)
       
    tree_funcionario.configure(yscrollcommand=scrollbar.set)

def botoes():
    global entryID, entryQTD, pagamento_var, tree_funcionario, label_preçototal, cont
    if loginTRUEouFALSE:    
        if username in usuarios:
        
            if usuarios[username]["Cargo"] == "Gerente":
                butao_estoque = Button(root, text='GERENCIAR ESTOQUE', font=("Arial", 10, "bold"), width=30, height=10, command=lambda: [clear(), tab_estoque(), informacoes_tree_estoque()])
                butao_estoque.place(x=100, y=220)
                
                botao_alerta = Button(root, text='ALERTAS',  font=("Arial", 10, "bold"), width=30, height=10, command=lambda: [clear(), tab_alertas(), informacoes_tree_alertas()])
                botao_alerta.place(x=450, y=220)
                
                botato_historico = Button(root, text='HISTORICO',  font=("Arial", 10, "bold"), width=30, height=10, command=lambda: [clear(), tab_historico()])
                botato_historico.place(x=795, y=220)

                button_createAccount = Button(root, text='Criar Conta', width=20, command=lambda: [clear(), tab_cadastro()])
                button_createAccount.place(x=900, y=600)

                botaodevoltar = Button(root, text="Voltar ao inicio", command=lambda: [deteste(), start(), clear()], width=20)
                botaodevoltar.place(x=750, y=600)
                if cont == 1:
                    alertas()
                    cont = 0
            
            elif usuarios[username]["Cargo"] == "Caixa":
                tab_caixa()    
     
def start():                       # O ESQUEMA DE CONSEGUIR REALIZAR O CADASTRO SEM TER QUE ABRIR OUTRA JANELA
    global login, cont

    cont = 1
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
    start()
    root.mainloop()

if __name__ == "__main__":
    carregar_usuarios()
    carregar_estoque()
    main()