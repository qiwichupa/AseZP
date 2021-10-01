import pdfminer.high_level
import pdfminer.layout
import pyexcel

file = "2021.01.pdf"

months = { 'январь':    '01',
          'февраль':   '02',
          'март':      '03',
          'апрель':    '04',
          'май':       '05',
          'июнь':      '06',
          'июль':      '07',
          'август':    '08',
          'сентябрь':  '09',
          'октябрь':   '10',
          'ноябрь':    '11',
          'декабрь':   '12'
          }
incomecodes = ['0010', '0206', '0207', '1010', '1024', '1274']
outcomecodes = ['/322']

for page_layout in pdfminer.high_level.extract_pages(file):
    textcontainers = [x for x in page_layout if isinstance(x, pdfminer.layout.LTTextContainer)]

    # поиск и конвертация даты
    for i, container in enumerate(textcontainers):
        for textline in container:
            if textline.get_text().strip() == 'Расчетный период':
                title = textcontainers[i].get_text().strip()
                value = textcontainers[i+1].get_text().strip()
                date="{}.{}".format(value.split(" ")[1], months[value.split(" ")[0]])
                print("{} - {}".format(title, date))

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



file='/mnt/autofs/public/test.ods'
sheet  = pyexcel.get_sheet(file_name=file)

colnames = [  '2021.01', '2021.02', '2021.03', '2021.04', '2021.05', '2021.06'
          , '2021.07', '2021.08', '2021.09', '2021.10', '2021.11', '2021.12'
          , '2022.01', '2022.02', '2022.03', '2022.04', '2022.05', '2022.06'
          , '2022.07', '2022.08', '2022.09', '2022.10', '2022.11', '2022.12'
         ]
for i, colname in enumerate(colnames):
    sheet[0, i+1] = colname

sheet.save_as(file)