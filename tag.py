#!/usr/bin/python3 -tt

import nltk
import sys

def	tag_brown_corpus(corpus_type):
		if corpus_type == 'brown':
			sents = nltk.corpus.brown.sents()	
		if corpus_type == 'gutenberg':
			sents = nltk.corpus.gutenberg.sents()
		i = 1
		l = len(sents)
		f = open(corpus_type+'.tags', 'w')
		print('getting tagged data')
		for sent in sents:
			print('progress ... '+str((i/l)*100) + '%')
			f.write(str(nltk.tag.pos_tag(sent))+'\n')
			i += 1

		

def	get_tag_sents(sents) :
		tag_sents = []
		i = 1
		progress = 0
		l = len(sents)
		for sent in sents:
			if ((i/l) * 100) - progress >= 1:
				progress = (i/l)*100
				print ('... progress '+str(progress)+' %')
			tag_sents.append(nltk.tag.pos_tag(sent))
			i += 1


		return tag_sents



def	main():
		args = sys.argv[1:]
		if len(args) != 1:
			print('usage: ./tag.py corpus-name(brown|gutenberg)')
			sys.exit(0)

		tag_brown_corpus(args[0])


if __name__ == '__main__':
	main()
