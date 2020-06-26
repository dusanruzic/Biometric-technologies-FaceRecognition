from mailmerge import MailMerge

template = "template.docx"
document = MailMerge(template)
print(document.get_merge_fields())
document.merge(PrezimeIme = "Душан Ружић", Datum = "07.11.2019", Iznos = "250.00", Zgrada = "Београдског батаљона 38", CenaUkupno = "500", Dugovanje = "300")

document.write('test-output.docx')
