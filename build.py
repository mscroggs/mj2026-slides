import os
import json
from markup import to_html


def make_slide(page, settings):
    return to_html(page), settings


if os.path.isdir("build"):
    os.system("rm -r build")

os.system("mkdir build")
os.system("cp -r _static build/_static")
os.system("cp -r test.html build/")

slides = []
i = 0
while os.path.isfile(f"slides/{i}.html"):
    settings = {"style": "default", "enter_slide": "false", "exit_slide": "false"}
    page = ""
    with open(f"slides/{i}.html") as f:
        for line in f:
            if line[0] == "!":
                key, value = line[1:].split("=", 1)
                settings[key.strip()] = value.strip()
            elif line.strip() == "<newslide>":
                slides.append(make_slide(page, settings))
                page = ""
            else:
                page += line
        slides.append(make_slide(page, settings))
    i += 1

with open("_template.html") as f:
    t = f.read()

enter_fs = []
exit_fs = []
slide_divs = ""
js = ""
for i, (slide, options) in enumerate(slides):
    enter_fs.append(options['enter_slide'])
    exit_fs.append(options['exit_slide'])
    slide_divs += f"<div class='slide {options['style']}' id='slide{i}' style='display:"
    if i == 0:
        slide_divs += "block"
    else:
        slide_divs += "none"
    slide_divs += "'>"
    while "<script>" in slide:
        a, b = slide.split("<script>", 1)
        b, c = b.split("</script>", 1)
        js += to_html(b) + "\n"
        slide = a + "\n" + c
    slide_divs += slide
    slide_divs += "</div>"

js += "enter_fs = [" + ",".join(enter_fs) + "];\n"
js += "exit_fs = [" + ",".join(exit_fs) + "];\n"

with open("_template.js") as f:
    js += f.read()
js = js.replace("{nslides}", f"{len(slides)}")

t = t.replace("{slide}", slide_divs)
t = t.replace("{js}", js)

with open("build/index.html", "w") as f:
    f.write(t)
