"""
Web Scraper - books.toscrape.com
Coleta nome, preço, URL, avaliação e disponibilidade de livros.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import time

logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url: str, retries: int = 3, delay: float = 1.0) -> BeautifulSoup:
    """Faz a requisição HTTP e retorna um objeto BeautifulSoup."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.warning(f"Tentativa {attempt}/{retries} falhou para {url}: {e}")
            if attempt < retries:
                time.sleep(delay)
    raise ConnectionError(f"Não foi possível acessar: {url}")


def get_all_product_urls(max_pages: int | None = None) -> list[str]:
    """
    Percorre todas as páginas de listagem e coleta as URLs de cada produto.

    Args:
        max_pages: Limite de páginas a percorrer. None = todas.

    Returns:
        Lista de URLs absolutas dos produtos.
    """
    product_urls = []
    current_url = BASE_URL
    page_number = 1

    logger.info("Iniciando coleta de URLs dos produtos...")

    while current_url:
        if max_pages and page_number > max_pages:
            break

        logger.info(f"Paginação — página {page_number}: {current_url}")
        soup = get_soup(current_url)

        # Coleta URLs dos produtos na página atual
        articles = soup.select("article.product_pod")
        for article in articles:
            relative_url = article.select_one("h3 > a")["href"]
            # As páginas internas usam paths relativos com "../"
            absolute_url = urljoin(current_url, relative_url)
            product_urls.append(absolute_url)

        # Verifica se existe próxima página
        next_btn = soup.select_one("li.next > a")
        if next_btn:
            current_url = urljoin(current_url, next_btn["href"])
            page_number += 1
            time.sleep(0.5)  # Pausa respeitosa entre requisições
        else:
            current_url = None

    logger.info(f"Total de URLs coletadas: {len(product_urls)}")
    return product_urls


def scrape_product(url: str) -> dict:
    """
    Acessa a página de um produto e extrai suas informações.

    Args:
        url: URL absoluta do produto.

    Returns:
        Dicionário com os dados extraídos.
    """
    soup = get_soup(url)

    name = soup.select_one("div.product_main > h1").get_text(strip=True)
    price = soup.select_one("p.price_color").get_text(strip=True)
    availability = soup.select_one("p.availability").get_text(strip=True)

    # Avaliação em estrelas (atributo da classe CSS: "star-rating Three")
    rating_word = soup.select_one("p.star-rating")["class"][1]
    rating = RATING_MAP.get(rating_word, 0)

    return {
        "name": name,
        "price": price,
        "rating_stars": rating,
        "availability": availability,
        "url": url,
    }


def run(max_pages: int | None = None, max_products: int | None = None) -> list[dict]:
    """
    Executa o scraper completo.

    Args:
        max_pages: Limite de páginas de listagem (None = todas as 50).
        max_products: Limite de produtos a extrair (None = todos).

    Returns:
        Lista de dicionários com os dados dos produtos.
    """
    product_urls = get_all_product_urls(max_pages=max_pages)

    if max_products:
        product_urls = product_urls[:max_products]

    products = []
    total = len(product_urls)

    logger.info(f"Extraindo dados de {total} produto(s)...")

    for index, url in enumerate(product_urls, start=1):
        try:
            logger.info(f"[{index}/{total}] {url}")
            product = scrape_product(url)
            products.append(product)
            time.sleep(0.3)  # Pausa respeitosa entre requisições
        except Exception as e:
            logger.error(f"Erro ao processar {url}: {e}")

    return products
