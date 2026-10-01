from models.loja import Loja
from models.item_catalogo.itemCatalogo import ItemCatalogo
from models.item_catalogo.livro import Livro
from models.item_catalogo.discos import Disco
from models.item_catalogo.revista import Revista
from models.item_catalogo.avaliacoes import Avaliacoes

loja1 = Loja("Sebo Releituras", "Curitiba")
loja2 = Loja("Livraria Cultura", "São Paulo")

loja1.avaliar_loja("Maria", 4.5)
loja1.avaliar_loja("Ana", 4.0)
loja2.avaliar_loja("Carla", 3.8)
loja2.avaliar_loja("Simone", 4.8)

loja2.alterar_status()

livro1 = Livro("O Caminho dos Reis", "Brandon Sanderson", 2019, "Fantasia", 200.00, "Lutinhas, espadas legais e o Kaladin sofrendo")
disco1 = Disco("Forever Now", "Switchfoot", 2026, "Alt-rock", "Vinil", 124.00)
revista1 = Revista("Capricho", "Abril", 2015, "Entretenimento", "Mensal", 30.00)

loja1.adicionar_catalogo(revista1)
loja1.adicionar_catalogo(disco1)
loja2.adicionar_catalogo(livro1)

livro1.avaliar_livro("Analice", 5.0)
livro1.avaliar_livro("Maria", 4.5)
disco1.avaliar_disco("João", 4.5)
disco1.avaliar_disco("José", 4.9)
revista1.avaliar_revista("Josefina", 3.7)
revista1.avaliar_revista("Maria do Bairro", 4.2)

Loja.listar_lojas()
loja1.exibir_catalogo
loja2.exibir_catalogo