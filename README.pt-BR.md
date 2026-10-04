[English](README.md) · **Português (Brasil)**

# serp-overlap

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`serp-overlap` é uma ferramenta de linha de comando gratuita e de código aberto que compara as URLs orgânicas do top 10 de duas ou mais buscas e mostra quantas páginas o Google serve para as duas. Duas palavras-chave que dividem muitas URLs costumam ser atendidas pelo mesmo tipo de página, então podem ir para uma página só. Lê arquivos JSON locais.

## Sumário

- [O que a ferramenta verifica](#o-que-a-ferramenta-verifica)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Perguntas frequentes](#perguntas-frequentes)
- [Limitações](#limitações)
- [Como contribuir](#como-contribuir)
- [Autor](#autor)
- [Licença](#licença)

## O que a ferramenta verifica

Para cada par de buscas, conta as URLs em comum no top 10, depois de tirar protocolo, `www`, query string, fragmento e barra final. O limiar é convenção minha, sem fonte externa, e pode ser mudado com `--minimo`:

- 4 ou mais em comum: mesmo grupo, uma página atende as duas.
- 2 ou 3: fronteira, decidir pela intenção e pelo tipo de página dominante.
- 0 ou 1: grupos separados.

## Requisitos

Python 3.9 ou superior. Só biblioteca padrão.

## Instalação

```bash
git clone https://github.com/LucasFerrazSEO/serp-overlap.git
cd serp-overlap
```

## Uso

Cada entrada é um arquivo JSON, lista de URLs ou formato do Serper (`{"organic": [{"link": "..."}]}`). O nome do arquivo vira o rótulo da busca.

```bash
python serp_overlap.py examples/busca-a.json examples/busca-b.json examples/busca-c.json
```

Busca opcional, só quando você define a sua própria chave do Serper no ambiente (nenhuma chave é guardada ou distribuída):

```bash
export SERPER_API_KEY="sua chave"
python serp_overlap.py --fetch "primeira busca" "segunda busca"
```

O código de saída é 2 em erro de leitura ou de busca. Os arquivos de `examples/` são inventados.

## Perguntas frequentes

**É gratuita mesmo?**
Sim, a ferramenta é MIT. A API do Serper tem termos e preços próprios, pagos por quem usa.

**Por que só o top 10?**
É um recorte simples e repetível. As posições mais fundas mudam muito entre leituras.

## Limitações

A SERP varia por dia, local e dispositivo, então uma leitura é um retrato, não um valor estável. O limiar é uma convenção que eu uso, não regra do Google. A sobreposição não diz se uma página deve existir, só o que o Google serve hoje.

## Como contribuir

Relatos de erro e sugestões são bem-vindos pelas [Issues do GitHub](https://github.com/LucasFerrazSEO/serp-overlap/issues).

## Autor

[Lucas Ferraz](https://lucasferraz.com) é especialista em SEO, criação de sites e Generative Engine Optimization e fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT. Veja [LICENSE](LICENSE).
