from models.item_catalogo.itemCatalogo import ItemCatalogo
from models.item_catalogo.livro import Livro

def test_livro_e_item_catalogo():
    livro = Livro("Orgulho e Preconceito", "Jane Austen", 1813, "Romance", 53.00, "Romance famosinho", None)
    assert isinstance(livro, ItemCatalogo)
    assert livro._titulo == "Orgulho e Preconceito"
    assert livro._autor == "Jane Austen"