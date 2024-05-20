from tika import parser

parsed_pdf = parser.from_file("data/nela-gt-2021/docx_data_sample/Lab2.docx")

print(type(parsed_pdf))
print(parsed_pdf.keys())

print(parsed_pdf['metadata'].keys())