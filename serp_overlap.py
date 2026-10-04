#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""serp-overlap: compara as URLs organicas do top 10 de duas ou mais buscas.

Entrada (um por busca): arquivo JSON com uma lista de URLs ou com o formato do Serper
({"organic": [{"link": ...}]}). O nome do arquivo (sem extensao) vira o rotulo da busca.

    python serp_overlap.py busca-a.json busca-b.json
    python serp_overlap.py a.json b.json c.json --minimo 4

Opcional, so se existir a variavel de ambiente SERPER_API_KEY (conta propria no Serper):
    python serp_overlap.py --fetch "termo a" "termo b"

Limiar (convencao do autor, sem fonte externa): 4 ou mais URLs em comum = mesmo grupo,
2 ou 3 = fronteira, 0 ou 1 = grupos separados. Biblioteca padrao apenas, Python 3.9+.
"""
import argparse
import itertools
import json
import os
import re
import sys
import urllib.request


def normalizar(u):
    u = re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower())
    return u.split("#", 1)[0].split("?", 1)[0].rstrip("/")


def urls_do_json(dado):
    if isinstance(dado, dict):
        itens = dado.get("organic", [])
    else:
        itens = dado
    saida = []
    for i in itens[:10]:
        link = i.get("link") if isinstance(i, dict) else i
        if isinstance(link, str) and link.strip():
            saida.append(normalizar(link))
    return saida


def ler_arquivo(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            return urls_do_json(json.load(f))
    except (OSError, ValueError) as e:
        print(f"ERRO {caminho}: {e}", file=sys.stderr)
        sys.exit(2)


def buscar(termo):
    chave = os.environ.get("SERPER_API_KEY")
    if not chave:
        print("ERRO: --fetch exige a variável de ambiente SERPER_API_KEY", file=sys.stderr)
        sys.exit(2)
    req = urllib.request.Request(
        "https://google.serper.dev/search",
        data=json.dumps({"q": termo, "gl": "br", "hl": "pt-br", "num": 10}).encode("utf-8"),
        headers={"X-API-KEY": chave, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return urls_do_json(json.loads(r.read().decode("utf-8")))
    except (OSError, ValueError) as e:
        print(f"ERRO ao buscar '{termo}': {e}", file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("entradas", nargs="+", help="arquivos JSON (ou termos, com --fetch)")
    ap.add_argument("--fetch", action="store_true", help="busca os termos no Serper (SERPER_API_KEY)")
    ap.add_argument("--minimo", type=int, default=4, help="URLs em comum para 'mesmo grupo' (padrão 4)")
    a = ap.parse_args()
    if len(a.entradas) < 2:
        ap.error("informe pelo menos duas entradas")
    lidos = {}
    for e in a.entradas:
        rotulo = e if a.fetch else os.path.splitext(os.path.basename(e))[0]
        lidos[rotulo] = buscar(e) if a.fetch else ler_arquivo(e)
        print(f"{rotulo}: {len(lidos[rotulo])} URLs orgânicas")
    for x, y in itertools.combinations(lidos, 2):
        comuns = [u for u in lidos[x] if u in set(lidos[y])]
        n = len(comuns)
        if n >= a.minimo:
            v = "MESMO GRUPO (uma página só atende as duas)"
        elif n >= 2:
            v = "FRONTEIRA (decidir pela intenção e pelo tipo de página dominante)"
        else:
            v = "GRUPOS SEPARADOS (páginas diferentes)"
        print(f"\n{x} x {y}: {n}/10 em comum -> {v}")
        for u in comuns:
            print(f"  = {u}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    main()
