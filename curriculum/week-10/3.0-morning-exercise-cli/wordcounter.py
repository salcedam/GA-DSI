def counter(txt):
	words=txt.split()
	return_dict={}
	for word in words:
		return_dict[word]=words.count(word)
	return_list=[]
	for word in return_dict.keys().sort():
		return_list.append(word,return_dict[word])
	for x in return_list:
		print x