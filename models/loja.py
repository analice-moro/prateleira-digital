from models.item_catalogo.avaliacoes import Avaliacoes
from models.item_catalogo.itemCatalogo import ItemCatalogo

class Loja:
    lojas = []
    STATUS_VALIDOS = ("Pendente", "Ativo", "Inativo")

    def __init__(self, nome_loja, cidade):
        self.nome_loja = nome_loja
        self.cidade = cidade
        self._status = "Pendente"
        self._avaliacoes = []
        self._catalogo = []
        Loja.lojas.append(self)

    @classmethod
    def listar_lojas(cls):
        for loja in cls.lojas:
            print(f"Loja: {loja.nome_loja.ljust(25)} | Endereço: {loja.cidade.ljust(20)} | Avaliações: {loja.media_avaliacoes} | Status: {loja.status}")

    @property
    def status(self):
        return self._status

    def definir_status(self, novo_status):
        if novo_status not in Loja.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {novo_status}")
        self._status = novo_status

    @property
    def media_avaliacoes(self):
        if not self._avaliacoes:
            return 0.0
        notas_somadas = sum(avaliacao._nota for avaliacao in self._avaliacoes)
        quantidade_avaliacoes = len(self._avaliacoes)
        media = round(notas_somadas / quantidade_avaliacoes, 1)
        return media

    @property
    def exibir_catalogo(self):
        print(f"Catálogo de {self.nome_loja}\n")
        for item in self._catalogo:
            if hasattr(item, '_autor'):
                mensagem_livro = f"| Título: {item._titulo} \n| Autor(a): {item._autor} \n| Gênero: {item._genero} \n| Ano de Lançamento: {item._ano_lancamento} \n| Sinopse: {item._sinopse} \n| Avaliações: {item.media_avaliacoes} \n| Preço: R${item._preco} \n"
                print(mensagem_livro)
            elif hasattr(item, '_artista'):
                mensagem_disco = f"| Título: {item._titulo} \n| Artista: {item._artista} \n| Gênero: {item._genero} \n| Ano de Lançamento: {item._ano_lancamento} \n| Formato da mídia: {item._formato_midia} \n| Avaliações: {item.media_avaliacoes} \n| Preço: R${item._preco} \n"
                print(mensagem_disco)
            else:
                mensagem_revista = f"| Título: {item._titulo} \n| Editora: {item._editora} \n| Gênero: {item._genero} \n| Ano de Lançamento: {item._ano_lancamento} \n| Periodicidade: {item._periodicidade} \n| Avaliações: {item.media_avaliacoes} \n| Preço: R${item._preco} \n"
                print(mensagem_revista)

    def avaliar_loja(self, cliente, nota):
        avaliacao = Avaliacoes(cliente, nota)
        self._avaliacoes.append(avaliacao)

    def adicionar_catalogo(self, item):
        if isinstance(item, ItemCatalogo):
            self._catalogo.append(item)
        else:
            raise ValueError("O item não pode ser None")