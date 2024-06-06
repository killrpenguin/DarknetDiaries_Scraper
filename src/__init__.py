from importlib.resources import files
xml_data = files('src').joinpath('dn_page.xml').read_text()
