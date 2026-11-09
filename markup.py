import re

def nonogram(m):
    rows = [i.split() for i in m[1].split('rows="')[1].split('"')[0].split("|")]
    cols = [i.split() for i in m[1].split('cols="')[1].split('"')[0].split("|")]
    print(rows, cols)
    return "LOLOL"

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
