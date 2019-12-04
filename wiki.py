import wikipediaapi

def print_sections(sections, level=0, endlevel=10):
	text = "";
	section_no = 0
	for s in sections:
		# print("%s: %s" % ("*" * (level + 1), s.title))
		section_no = section_no + 1
		if section_no <= endlevel:
			text = text + s.text + print_sections(s.sections, level + 1)
	return text

def findwiki(given_input):
	wiki = wikipediaapi.Wikipedia('en')

	page  = wiki.page(given_input)
	if page.exists()==False:
		print("Wikipedia page doesn't exists for ",given_input," keyword")
		exit(1)
	return page.summary + print_sections(page.sections), page.fullurl