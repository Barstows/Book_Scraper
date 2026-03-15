"""
Ponto de entrada do scraper.
Execute: python main.py
"""

import json
import logging
import argparse
from pathlib import Path
from src.scraper import run

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Web Scraper — books.toscrape.com"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Número máximo de páginas de listagem a percorrer (padrão: todas).",
    )
    parser.add_argument(
        "--max-products",
        type=int,
        default=None,
        help="Número máximo de produtos a extrair (padrão: todos).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/products.json",
        help="Caminho do arquivo JSON de saída (padrão: output/products.json).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    products = run(max_pages=args.max_pages, max_products=args.max_products)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Scraping concluído! {len(products)} produto(s) salvo(s) em '{output_path}'.")


if __name__ == "__main__":
    main()
