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
            if self.itens[nome].quantidade >= quantidade:
                self.itens[nome].quantidade -= quantidade
                if self.itens[nome].quantidade == 0:
                    del self.itens[nome]
            else:
                st.warning("Quantidade insuficiente para remover.")
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

def carregar_estoque_session():
    if "estoque" not in st.session_state:
        st.session_state.estoque = Estoque()

def menu():
    st.title("Sistema de Organização de Estoque")

    carregar_estoque_session()  # Carrega o estoque na sessão

    estoque = st.session_state.estoque

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

    # Remover Item
    st.header("Remover Item")
    nome_remover = st.text_input("Nome do Item para Remover:")
    quantidade_remover = st.number_input("Quantidade a Remover", min_value=1, step=1)
    if st.button("Remover Item"):
        if nome_remover and quantidade_remover > 0:
            estoque.remover_item(nome_remover, quantidade_remover)
            st.success(f"Quantidade de '{nome_remover}' removida com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente!")

    # Listar Itens
    st.header("Itens no Estoque")
    if st.button("Listar Itens"):
        estoque.listar_itens()

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
