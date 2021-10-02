import pdfminer.high_level
import pdfminer.layout
import pyexcel

incomecodes = {  '0010': 'Оплата по окладу (часы)'
                   , '0206': 'ОплатаЗаРаботуВых(Окл+ИВ)'
                   , '0207': 'ДоплатаЗаРаботуВых(Ок+ИВ)'
                   , '1010': 'ИСН'
                   , '1024': 'Индексирующая выплата'
                   , '1274': 'Оперативная премия'
                   }
outcomecodes = {'/322': 'НДФЛ 13%'}

def from_pdf(file, incomecodes, outcomecodes):
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

    for page_layout in pdfminer.high_level.extract_pages(file):
        textcontainers = [x for x in page_layout if isinstance(x, pdfminer.layout.LTTextContainer)]

        # поиск и конвертация даты
        for i, container in enumerate(textcontainers):
            for textline in container:
                if textline.get_text().strip() == 'Расчетный период':
                    title = textcontainers[i].get_text().strip()
                    value = textcontainers[i+1].get_text().strip()
                    date="{}.{}".format(value.split(" ")[1], months[value.split(" ")[0]])

        values = {}
        # плюсы (оклад, премии и т.д.)
        for i, container in enumerate(textcontainers):
            for textline in container:
                if textline.get_text()[0:4] in incomecodes.keys():
                    j = i
                    while len(textcontainers[j].get_text().split(",")) < 2: j += 1
                    if j < i+3 and len(textcontainers[j+1].get_text().split(",")) == 2: j += 1
                    code = textline.get_text()[0:4]
                    value = float((textcontainers[j].get_text().strip().replace(',','.').replace(' ','')))
                    values.update(**{code: value})

        # минусы (налоги)
        for i, container in enumerate(textcontainers):
            for textline in container:
                if textline.get_text()[0:4] in outcomecodes.keys():
                    j = i
                    while len(textcontainers[j].get_text().split(",")) < 2: j += 1
                    if j < i+3 and len(textcontainers[j+1].get_text().split(",")) == 2: j += 1
                    code = textline.get_text()[0:4]
                    value = (-1) * float((textcontainers[j].get_text().strip().replace(',','.').replace(' ','')))
                    values.update(**{code: value})
    return (date, values)


def to_ods(file, incomecodes, outcomecodes, date, values):
    sheet = pyexcel.get_sheet(file_name=file)

    colnames = ['2021.01', '2021.02', '2021.03', '2021.04', '2021.05', '2021.06'
        , '2021.07', '2021.08', '2021.09', '2021.10', '2021.11', '2021.12'
        , '2022.01', '2022.02', '2022.03', '2022.04', '2022.05', '2022.06'
        , '2022.07', '2022.08', '2022.09', '2022.10', '2022.11', '2022.12'
                ]

    sheet[0, 1] = 'названия'
    for i, colname in enumerate(colnames):
        sheet[0, i + 2] = colname
    sheet[1, 0] = 'Итого'
    sheet[1, 1] = ':'
    for i, rowcode in enumerate({**incomecodes, **outcomecodes}.keys()):
        allrows = list(sheet.column_at(0))
        if rowcode not in allrows:
            sheet[len(allrows), 0] = str(rowcode)
            sheet[len(allrows), 1] = str({**incomecodes, **outcomecodes}[rowcode])

    sheet.name_columns_by_row(0)
    sheet.name_rows_by_column(0)

    # print(sheet.rownames)
    for key in values.keys():
        sheet[key, date] = values[key]

    sheet.save_as(file)

if __name__  == '__main__':
    file = "2021.01.pdf"
    date, values = from_pdf(file, incomecodes, outcomecodes)
    file='/mnt/autofs/public/test.ods'
    to_ods(file, incomecodes, outcomecodes, date, values)