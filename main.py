class MarkmapRender():
    def __init__(self):
        pass

    def render(self, source):
        doc = '''<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="IE=edge" http-equiv="X-UA-Compatible"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <script src="https://unpkg.com/d3@7" type="text/javascript"></script>
    <script src="https://unpkg.com/markmap-lib@0.15.3" type="text/javascript"></script>
    <script src="https://unpkg.com/markmap-view@0.15.3" type="text/javascript"></script>
    <style type="text/css">div.mkdocs-markmap {
        width: 100%;
        min-height: 1em;
        border: 1px solid grey;
    }

    .mkdocs-markmap > svg {
        width: 100%;
        height: 100%;
        display: block;
    }
    </style>
</head>
<body>
<div class="mkdocs-markmap">
    <markmap-data class="language-markmap" hidden="true">
'''+ source+'''
    </markmap-data>
</div>
<script type="text/javascript">(function initializeMarkmap() {
    const transformer = new markmap.Transformer();
    const assets = transformer.getAssets();
    const loading = Promise.all([
        assets.styles && markmap.loadCSS(assets.styles),
        assets.scripts && markmap.loadJS(assets.scripts),
    ]);

    function parseData(content) {
        const { root, frontmatter } = transformer.transform(content);
        let options = markmap.deriveOptions(frontmatter?.markmap);
        options = Object.assign({
            fitRatio: 0.85,
        }, options);
        return { root, options };
    }

    function resetMarkmap(m, el) {
        const { minX, maxX, minY, maxY } = m.state;
        const height = el.clientWidth * (maxX - minX) / (maxY - minY);
        el.style.height = height + "px";
        m.fit();
    }

    function renderMarkmap(el) {
        let svg = el.querySelector('svg');
        if (svg) return;
        const content = el.textContent;
        el.innerHTML = '<svg>';
        svg = el.firstChild;
        const { root, options } = parseData(content);
        const m = markmap.Markmap.create(svg, options, root);
        resetMarkmap(m, el);
        transformer.hooks.retransform.tap(() => {
            const { root, options } = parseData(content);
            m.setData(root, options);
            resetMarkmap(m, el);
        });
    }

    function updateMarkmaps(node) {
        for (const el of node.querySelectorAll('.mkdocs-markmap')) {
            renderMarkmap(el);
        }
    }

    loading.then(() => {
        const observer = new MutationObserver((mutationList) => {
            for (const mutation of mutationList) {
                if (mutation.type === 'childList') {
                    for (const node of mutation.addedNodes) {
                        updateMarkmaps(node);
                    }
                }
            }
        });

        observer.observe(document.body, { childList: true });

        updateMarkmaps(document);
    });
})();
</script>
</body>
</html>'''
        return doc

if __name__ == '__main__':
    source = '''---
markmap:
  colorFreezeLevel: 2
---

# markmap

## Links

- [Website](https://markmap.js.org/)
- [GitHub](https://github.com/gera2ld/markmap)

## Related Projects

- [coc-markmap](https://github.com/gera2ld/coc-markmap) for Neovim
- [markmap-vscode](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode) for VSCode
- [eaf-markmap](https://github.com/emacs-eaf/eaf-markmap) for Emacs

## Features

Note that if blocks and lists appear at the same level, the lists will be ignored.

### Lists

- **strong** ~~del~~ *italic* ==highlight==
- `inline code`
- [x] checkbox
- Katex: $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$ <!-- markmap: fold -->
  - [More Katex Examples](#?d=gist:af76a4c245b302206b16aec503dbe07b:katex.md)
- Now we can wrap very very very very long text based on `maxWidth` option

### Blocks

```js
console('hello, JavaScript')
```

| Products | Price |
|-|-|
| Apple | 4 |
| Banana | 2 |

![](/favicon.png)'''
    render = MarkmapRender()
    with open("test.html", "w") as f:
        f.write(render.render(source))
