**English** · [Português (Brasil)](README.pt-BR.md)

# serp-overlap

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`serp-overlap` is a free, open source command-line tool that compares the organic top 10 URLs of two or more searches and tells you how many pages Google serves for both. Two keywords that share many URLs are usually answered by the same kind of page, so they can go to one page. It reads local JSON files and prints the report in Brazilian Portuguese.

## Contents

- [What it checks](#what-it-checks)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## What it checks

For every pair of searches it counts the URLs in common in the top 10, after removing protocol, `www`, query string, fragment and trailing slash. The threshold is my own convention, with no external source, and you can change it with `--minimo`:

- 4 or more in common: same group, one page serves both.
- 2 or 3: borderline, decide by intent and by the dominant page type.
- 0 or 1: separate groups.

## Requirements

Python 3.9 or newer. Standard library only.

## Installation

```bash
git clone https://github.com/LucasFerrazSEO/serp-overlap.git
cd serp-overlap
```

## Usage

Each input is a JSON file, either a list of URLs or the Serper format (`{"organic": [{"link": "..."}]}`). The file name becomes the label of the search.

```bash
python serp_overlap.py examples/busca-a.json examples/busca-b.json examples/busca-c.json
```

Real output on the invented files in `examples/`:

```
busca-a x busca-b: 5/10 em comum -> MESMO GRUPO (uma página só atende as duas)
  = site1.example.com/pagina
  ...
busca-a x busca-c: 0/10 em comum -> GRUPOS SEPARADOS (páginas diferentes)
```

Optional fetch, only when you set your own Serper key in the environment (no key is stored or shipped):

```bash
export SERPER_API_KEY="your key"
python serp_overlap.py --fetch "first search" "second search"
```

The exit code is 2 on a read or fetch error.

## FAQ

**Is it really free?**
Yes, the tool is MIT. The Serper API has its own terms and prices, paid by whoever uses it.

**Why the top 10 only?**
It is a simple, repeatable cut. Deeper positions change a lot between reads.

## Limitations

A SERP varies by day, location and device, so one read is a snapshot, not a stable value. The threshold is a convention that I use, not a rule from Google. Overlap says nothing about whether a page should exist, only about what Google serves today.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/serp-overlap/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
