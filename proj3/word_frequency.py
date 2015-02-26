def process_text(filename):
	"""Makes histogram of text"""
	d = dict()
	fp = open(filename, 'r')
	for line in fp:
		for word in line.split():

			while not (word == '' or word[0].isalpha() or word[0].isdigit()):
				word = word[1:]
			while not (word == '' or word[-1].isalpha() or word[-1].isdigit()):
				word = word[0:-1]
			word = word.lower()
			if word != '':
				d[word] = d.get(word, 0) + 1
	return d

def inverse_dict(d):
	"""Reverse keys and values of dictionary"""
	inverse = dict()
	for key in d:
		val = d[key]
		if val not in inverse:
			inverse[val] = [key]
		else:
			inverse[val].append(key)
	return inverse

def subtract_common(freq, freq_word):
	"""subtrace most common 100 words from inversed dictionary"""
	common_freq = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 
	'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'
	'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
	'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
	'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
	'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
	'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
	'than', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
	'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
	'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
	'are', 'is', 'have', 'has', 'were', 'was', 'been', 'had']
	top10_freq = []
	for number in freq:
		if freq_word[number][0] not in common_freq:
			top10_freq.append(number)
		if len(top10_freq) == 10:
			break
	top10_freq.sort()
	top10_freq.reverse()
	return top10_freq


stat = process_text('les_miserables.txt')
freq_word = inverse_dict(stat)
freq = freq_word.keys()
freq.sort()
freq.reverse()
top10_freq = subtract_common(freq, freq_word)
for number in top10_freq:
	print (freq_word[number][0], number)