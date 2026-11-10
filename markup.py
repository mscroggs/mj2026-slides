import re

def nonogram(m):
    rows = [i.split() for i in m[1].split('rows="')[1].split('"')[0].split("|")]
    row_texts = [" ".join(f"{j}" for j in i) for i in rows]
    nrows = len(rows)
    row_clue_len = max(len(i) for i in row_texts)

    cols = [i.split() for i in m[1].split('cols="')[1].split('"')[0].split("|")]
    col_texts = [" ".join(f"{j}" for j in i) for i in cols]
    ncols = len(cols)
    col_clue_len = max(len(i.split()) for i in col_texts)

    if 'filled="' in m[1]:
        filled = [tuple(int(j) for j in i.split(",")) for i in m[1].split('filled="')[1].split('"')[0].split()]
    else:
        filled = []
    if 'unfilled="' in m[1]:
        if (raw := m[1].split('unfilled="')[1].split('"')[0]) != "remainder":
            unfilled = [tuple(int(j) for j in i.split(",")) for i in raw.split()]
        else:
            unfilled = [(i, j) for j in range(nrows) for i in range(ncols) if (i, j) not in filled]
    else:
        unfilled = []

    if 'color="' in m[1]:
        color = m[1].split('color="')[1].split('"')[0]
    else:
        color = "#000000"

    svg = f"<svg viewBox='0 0 {20 + 100 * ncols + 65 * row_clue_len} {20 + 100*nrows + 100 * col_clue_len}' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'"
    if 'style="' in m[1]:
        svg += ' style="' + m[1].split('style="')[1].split('"')[0] + '"'
    else:
        svg += ' class="default-style"'
    svg += ">\n"
    for i, j in filled:
        svg += f"<rect x='{10 + 65 * row_clue_len + 100 * i}' y='{10 + 100 * col_clue_len + 100 * j}' width='100' height='100' />\n"
    for i, j in unfilled:
        x = 60 + 65 * row_clue_len + 100 * i
        y = 60 + 100 * col_clue_len + 100 * j
        svg += f"<line x1='{x+15}' y1='{y+15}' x2='{x-15}' y2='{y-15}' stroke-linecap='round' stroke-width='3.0' stroke='#CCCCCC' />\n"
        svg += f"<line x1='{x+15}' y1='{y-15}' x2='{x-15}' y2='{y+15}' stroke-linecap='round' stroke-width='3.0' stroke='#CCCCCC' />\n"

    for i in range(ncols + 1):
        x = 10 + 65 * row_clue_len + 100 * i
        svg += f"<line x1='{x}' y1='10' x2='{x}' y2='{10 + 100 * col_clue_len}' stroke-linecap='round' stroke-width='3.0' stroke='#CCCCCC' />\n"
        svg += f"<line x1='{x}' y1='{10 + 100 * col_clue_len}' x2='{x}' y2='{10 + 100 * col_clue_len + 100 * nrows}' stroke-linecap='round' stroke-width='3.0' stroke='{color}' />\n"
    for i, clue in enumerate(col_texts):
        for j, c in enumerate(clue.split()[::-1]):
            svg += f"<text x='{60 + 65 * row_clue_len + 100 * i}' y='{100 * (col_clue_len - j)}' fill='{color}' font-size='25' style=\"text-anchor:middle;dominant-baseline:text-bottom;font-size:80px;font-family:martianmono\">{c}</text>\n"

    for i in range(nrows + 1):
        y = 10 + 100 * col_clue_len + 100 * i
        svg += f"<line x1='10' y1='{y}' x2='{10 + 65 * row_clue_len}' y2='{y}' stroke-linecap='round' stroke-width='3.0' stroke='#CCCCCC' />\n"
        svg += f"<line x1='{10 + 65 * row_clue_len}' y1='{y}' x2='{10 + 65 * row_clue_len + 100 * ncols}' y2='{y}' stroke-linecap='round' stroke-width='3.0' stroke='{color}' />\n"
    for i, clue in enumerate(row_texts):
        svg += f"<text x='{65 * row_clue_len}' y='{60 + 100 * col_clue_len + 100 * i}' fill='{color}' font-size='25' style=\"text-anchor:end;dominant-baseline:central;font-size:80px;font-family:martianmono\">{clue}</text>\n"


    svg += "</svg>\n"
    return svg

def to_html(page):

    while "</for>" in page:
        pre, post = page.split("</for>", 1)
        pre, inner = pre.rsplit("<for ", 1)
        info, inner = inner.split(">", 1)
        v, i, r = info.split(" ", 2)
        inner = inner.split("{{")
        assert i == "in"
        page = pre
        for value in eval(r):
            page += inner[0]
            for part in inner[1:]:
                a, b = part.split("}}")
                page += str(eval(a.replace(v, str(value))))
                page += b
        page += post

    page = page.replace("<title>", "<div class='title'>")
    page = page.replace("</title>", "</div>")

    page = page.replace("<author>", "<div class='author'>")
    page = page.replace("</author>", "</div>")
    for a in ["left", "right", "centre"]:
        page = page.replace(f"<block align {a}>", f"<div class='block{a}'>")
    page = page.replace("</block>", "</div>")
    page = page.replace("<spacing>", "<div style='height:10vh'></div>")
    page = page.replace("<spacing small>", "<div style='height:1vh'></div>")
    page = page.replace("<mscroggs.co.uk>", "<span style='font-family:comfortaaregular;font-weight:normal'><span style='color:#2EA3D0'>mscroggs</span><span style='color:FFA366'>.co.uk</span></span>")
    page = page.replace("<icon twitter>", "<span class='icon twitter'>a</span>")
    page = page.replace("<icon website>", "<span class='icon website'>d</span>")
    page = page.replace("<icon mastodon>", "<span class='icon mastodon'>n</span>")
    page = page.replace("<icon bluesky>", "<span class='icon bluesky'>t</span>")
    page = re.sub(r"\<nonogram ([^\>]+)\>", nonogram, page)
    return page
