from random import choice

def process_text(filename):
	"""Makes map from prefix to suffix"""
	d = dict()
	fp = open(filename, 'r')
	prev_word = ''
	quote = ['\'', '\"']
	for line in fp:
		for word in line.split():
			while word != '' and word[0] in quote:
				word = word[1:]
			while word != '' and word[-1] in quote:
				word = word[:-1]
			if word != '':
				d[prev_word] = d.get(prev_word, [])
				d[prev_word].append(word)
				prev_word = word
	return d

def generate_sentence(words_map):
	"""Generate sentence with Markov text synthesis"""
	sentence = ''
	end_of_sentence = ['.', '!', '?']
	first = choice(words_map.keys())
	while not first.isupper():
		first = choice(words_map.keys())
	sentence += first
	next = choice(words_map[first])
	sentence += ' ' + next
	while next[-1] not in end_of_sentence:
		next = choice(words_map[next])
		sentence += ' ' + next
	return sentence


words_map = process_text('les_miserables.txt')
print generate_sentence(words_map)

