import pytest
from models.loja import Loja

def test_media_calcula_corretamente():
    loja = Loja("Livraria da Vila", "São Paulo")
    loja.avaliar_loja("Ana", 5.0)
    loja.avaliar_loja("Maria", 4.0)
    assert loja.media_avaliacoes == 4.5

def test_adicionar_item_invalido():
    loja = Loja("Saraiva", "Curitiba")
    with pytest.raises(ValueError):
        loja.adicionar_catalogo("Isso não é um item do catálogo")

def test_verificar_exibir_catalogo_vazio(capsys):
    loja = Loja("Sebo Visconde", "São José dos Pinhais")
    loja.exibir_catalogo
    saida = capsys.readouterr().out
    assert "Catálogo de Sebo Visconde" in saida