import streamlit as st
import json
import os

class Item:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.nome} - Quantidade: {self.quantidade}, Preço: R${self.preco:.2f}"

    def to_dict(self):
        return {"nome": self.nome, "quantidade": self.quantidade, "preco": self.preco}

    @staticmethod
    def from_dict(data):
        return Item(data["nome"], data["quantidade"], data["preco"])

class Estoque:
    def __init__(self, arquivo_estoque="estoque.json"):
        self.itens = {}
        self.arquivo_estoque = arquivo_estoque
        self.carregar_estoque()

    def adicionar_item(self, nome, quantidade, preco):
        if nome in self.itens:
            self.itens[nome].quantidade += quantidade
        else:
            self.itens[nome] = Item(nome, quantidade, preco)

    def remover_item(self, nome, quantidade):
        if nome in self.itens:
            item = self.itens[nome]
            if item.quantidade >= quantidade:
                item.quantidade -= quantidade
                if item.quantidade == 0:
                    del self.itens[nome]
                st.success(f"Item '{nome}' removido com sucesso!")
            else:
                st.warning(f"Quantidade insuficiente para remover. Só há {item.quantidade} unidades de '{nome}' no estoque.")
        else:
            st.warning("Item não encontrado.")

    def listar_itens(self):
        if not self.itens:
            st.warning("Estoque vazio.")
        else:
            for item in self.itens.values():
                st.write(item)

    def valor_total_estoque(self):
        total = sum(item.quantidade * item.preco for item in self.itens.values())
        return total

    def salvar_estoque(self):
        with open(self.arquivo_estoque, "w") as f:
            json.dump({nome: item.to_dict() for nome, item in self.itens.items()}, f, indent=4)

    def carregar_estoque(self):
        if os.path.exists(self.arquivo_estoque):
            with open(self.arquivo_estoque, "r") as f:
                dados = json.load(f)
                for nome, item_data in dados.items():
                    self.itens[nome] = Item.from_dict(item_data)

    def organizar_alfabeticamente(self):
        self.itens = dict(sorted(self.itens.items()))

    def organizar_por_quantidade(self):
        self.itens = dict(sorted(self.itens.items(), key=lambda item: item[1].quantidade))

def carregar_estoque_session():
    if "estoque" not in st.session_state:
        st.session_state.estoque = Estoque()

def menu():
    st.title("Sistema de Organização de Estoque")

    carregar_estoque_session()  # Carrega o estoque na sessão

    estoque = st.session_state.estoque

    # Lateral - Menu de opções
    with st.sidebar:
        st.header("Menu")
        opcao = st.radio("Escolha uma opção:", ("Adicionar Itens", "Remover Itens", "Listar Itens", "Organizar Itens", "Valor Total"))

    # Opções dependendo da escolha do menu lateral
    if opcao == "Adicionar Itens":
        # Adicionar Item
        st.header("Adicionar Item")
        nome = st.text_input("Nome do Item:")
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        preco = st.number_input("Preço (R$)", min_value=0.01, format="%.2f")

        if st.button("Adicionar Item"):
            if nome and quantidade > 0 and preco > 0:
                estoque.adicionar_item(nome, quantidade, preco)
                st.success(f"Item '{nome}' adicionado com sucesso!")
            else:
                st.error("Preencha todos os campos corretamente!")

    elif opcao == "Remover Itens":
        # Remover Item
        st.header("Remover Item")
        nome_remover = st.text_input("Nome do Item para Remover:")
        quantidade_remover = st.number_input("Quantidade a Remover", min_value=1, step=1)
        if st.button("Remover Item"):
            if nome_remover and quantidade_remover > 0:
                estoque.remover_item(nome_remover, quantidade_remover)
            else:
                st.error("Preencha todos os campos corretamente!")

    elif opcao == "Listar Itens":
        # Listar Itens
        st.header("Itens no Estoque")
        if st.button("Listar Itens"):
            estoque.listar_itens()

    elif opcao == "Organizar Itens":
        # Organizar Itens
        st.header("Organizar Itens")
        organizar_opcao = st.radio("Como deseja organizar?", ("Por ordem alfabética", "Por quantidade"))
        if organizar_opcao == "Por ordem alfabética":
            if st.button("Organizar"):
                estoque.organizar_alfabeticamente()
                st.success("Itens organizados em ordem alfabética!")
        elif organizar_opcao == "Por quantidade":
            if st.button("Organizar"):
                estoque.organizar_por_quantidade()
                st.success("Itens organizados por quantidade!")

    elif opcao == "Valor Total":
        # Valor Total do Estoque
        st.header("Valor Total do Estoque")
        if st.button("Calcular Valor Total"):
            total = estoque.valor_total_estoque()
            st.write(f"O valor total do estoque é: R${total:.2f}")

    # Salvar o Estoque no Arquivo
    if st.button("Salvar Estoque"):
        estoque.salvar_estoque()
        st.success("Estoque salvo com sucesso!")

if __name__ == "__main__":
    menu()
