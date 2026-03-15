# Web Scraper — books.toscrape.com

Script Python para coleta de dados de produtos em um e-commerce público, utilizando `requests` e `BeautifulSoup`.

---

## Site escolhido

**[books.toscrape.com](https://books.toscrape.com/)** — site criado especificamente para prática de web scraping, com listagem de livros, paginação (50 páginas) e página individual para cada produto.

---

## Dados coletados por produto

| Campo | Descrição |
|---|---|
| `name` | Nome do livro |
| `price` | Preço (ex: `£51.77`) |
| `rating_stars` | Avaliação em estrelas (1–5) |
| `availability` | Disponibilidade em estoque |
| `url` | URL da página do produto |

**Exemplo de saída:**

```json
[
  {
    "name": "A Light in the Attic",
    "price": "£51.77",
    "rating_stars": 3,
    "availability": "In stock",
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
  }
]
```

---

## Instalação

**Pré-requisitos:** Python 3.10+

```bash
# Clone o repositório (ou extraia o arquivo .zip)
cd web-scraper

# (Opcional) Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## Execução

```bash
# Coleta TODOS os produtos (50 páginas, ~1000 livros — leva alguns minutos)
python main.py

# Limita a 2 páginas de listagem (~40 produtos — rápido para teste)
python main.py --max-pages 2

# Limita a 10 produtos no total
python main.py --max-products 10

# Define um arquivo de saída personalizado
python main.py --max-pages 3 --output meus_produtos.json
```

O resultado é salvo em `output/products.json` por padrão.

---

## Estrutura do projeto

```
web-scraper/
├── src/
│   └── scraper.py      # Lógica principal: paginação, coleta de URLs e extração
├── output/             # Arquivos JSON gerados
├── main.py             # Ponto de entrada e CLI
├── requirements.txt    # Dependências
└── README.md
```

---

## Abordagem

O script segue três etapas bem definidas:

1. **Paginação** — `get_all_product_urls()` percorre todas as páginas de listagem seguindo o botão "next", coletando a URL relativa de cada produto e convertendo para URL absoluta.

2. **Extração** — `scrape_product()` acessa cada página individual e faz o parse dos campos desejados via seletores CSS.

3. **Saída** — `main.py` orquestra a execução, recebe argumentos via CLI e persiste o resultado em JSON formatado.
