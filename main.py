import pdfminer.high_level
import pdfminer.layout


file = "2021.01.pdf"

incomecodes = ['0010', '0206', '0207', '1010', '1024', '1274']
outcomecodes = ['/322']

for page_layout in pdfminer.high_level.extract_pages(file):
    textcontainers = [x for x in page_layout if isinstance(x, pdfminer.layout.LTTextContainer)]

    # плюсы (оклад, премии и т.д.)
    for i, container in enumerate(textcontainers):
        for textline in container:
            if textline.get_text()[0:4] in incomecodes:
                j = i
                while len(textcontainers[j].get_text().split(",")) < 2: j += 1
                if j < i+3 and len(textcontainers[j+1].get_text().split(",")) == 2: j += 1
                title = textcontainers[i].get_text().strip()[5:]
                value = textcontainers[j].get_text().strip()
                print("{} - {}".format(title, value))

    # минусы (налоги)
    for i, container in enumerate(textcontainers):
        for textline in container:
            if textline.get_text()[0:4] in outcomecodes:
                j = i
                while len(textcontainers[j].get_text().split(",")) < 2: j += 1
                if j < i+3 and len(textcontainers[j+1].get_text().split(",")) == 2: j += 1
                title = textcontainers[i].get_text().strip()[5:]
                value = textcontainers[j].get_text().strip()
                print("{} - {}".format(title, value))