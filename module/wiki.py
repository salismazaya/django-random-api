import wikipedia as wk
wk.set_lang("id")

def wikipedia(query):
	data = wk.search(query)
	if len(data) == 0:
		return {"sucess": False}
		
	data = wk.page(data[0])
	rv = {
		"title": data.title,
		"content": data.content,
		"success": True,
	}
	
	return rv