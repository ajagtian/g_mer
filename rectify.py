#!/usr/bin/python3 -tt

import nltk
import sys
import percepclassify
import tag

def	rectify(tag_sents, g_hash):
		print ('extracting classes')
		# P_POS, PP_POS, PPP_POS, N_POS, NN_POS, NNN_POS, 
		p = 1
		ll = len(tag_sents)
		progress = 0
		out_sents = []
		for tag_sent in tag_sents:
			out_sent = []
			if ((p/ll)*100 - progress) >= 2:
				progress = (p/ll)*100
				print('progress ... '+str(progress))
			p += 1
			l = len(tag_sent)
			for i in range(len(tag_sent)):
				feature_vector = {'P_POS':'P_BS', 'PP_POS':'PP_BS', 'PPP_POS':'PPP_BS', 'N_POS':'N_ES', 'NN_POS':'NN_ES', 'NNN_POS':'NNN_ES', 'W_S':'0', 'PREV':'BOS', 'NEXT':'', 'P_SF':'P_SF', 'PP_SF':'PP_SF', 'N_SF':'', 'NN_SF':'', 'P_W_S':'0', 'N_W_S':'0', 'P_POS_PP_POS':'', 'N_POS_NN_POS':''}
				tag_word = tag_sent[i]
				clazz = tag_word[0]
				if tag_word[0][0].isupper():
					feature_vector['W_S'] = str(1)
				word = tag_word[0].lower()
				if word in ["'s", "'re"]:
					continue
				pos = tag_word[1]
				if word in ['its', 'your', 'their', 'loose', 'lose', 'to', 'too', "it's", "you're", "they're"]:
					if i-1 >= 0:
						feature_vector['P_POS'] = tag_sent[i-1][1]
						prev = tag_sent[i-1][0]
						if prev[0].isupper():
							feature_vector['P_W_S'] = '1'
						feature_vector['PREV'] = prev.lower()
						feature_vector['P_SF'] = prev[-3:].lower()
					if i-2 >= 0:
						feature_vector['PP_POS'] = tag_sent[i-2][1]
						feature_vector['PP_SF'] = tag_sent[i-2][0].lower()[-3:]
						feature_vector['P_POS_PP_POS'] = feature_vector['P_POS']+'_'+feature_vector['PP_POS']
					if i-3 >= 0:
						feature_vector['PPP_POS'] = tag_sent[i-3][1]
					if i+1 < l:
						feature_vector['N_POS'] = tag_sent[i+1][1]
						next = tag_sent[i+1][0]
						feature_vector['N_SF'] = next[-3:].lower()
						feature_vector['NEXT'] = next.lower()
						if next[0].isupper():
							feature_vector['N_W_S'] = '1'
					if i+2 < l:
						feature_vector['NN_POS'] = tag_sent[i+2][1]
						feature_vector['NN_SF'] = tag_sent[i+2][0].lower()[-3:]
						feature_vector['N_POS_NN_POS'] = feature_vector['N_POS']+'_'+feature_vector['NN_POS']
						
					if i+3 < l:
						feature_vector['NNN_POS'] = tag_sent[i+3][1]
						
				
				
					context_string = ''
					for feature in feature_vector.keys():
						if feature_vector[feature] != '':
							context_string += feature+':'+feature_vector[feature]+' '
					if word in ["its","it's"]:
						clazz = percepclassify.classify(context_string, g_hash['i-i'])
					if word in ["loose","lose"]:
						clazz = percepclassify.classify(context_string, g_hash['lo-lo'])
					if word in ["their","they're"]:
						clazz = percepclassify.classify(context_string, g_hash['th-th'])
					if word in ["to","too"]:
						clazz = percepclassify.classify(context_string, g_hash['to-too'])
					if word in ["your","you're"]:
						clazz = percepclassify.classify(context_string, g_hash['yo-yo'])
					if feature_vector['W_S'] == '1':
						clazz = clazz[0].upper() + clazz[1:]
					




				if word == 'it' and i+1 < l and tag_sent[i+1][0] == "'s":
					word = "it's"
					
					if i-1 >= 0:
						feature_vector['P_POS'] = tag_sent[i-1][1]
						prev = tag_sent[i-1][0]
						feature_vector['PREV'] = prev.lower()
						feature_vector['P_SF'] = prev[-3:].lower()
						if prev[0].isupper():
							feature_vector['P_W_S'] = '1'
					
					if i-2 >= 0:
						feature_vector['PP_POS'] = tag_sent[i-2][1]
						feature_vector['PP_SF'] = tag_sent[i-2][0].lower()[-3:]
						feature_vector['P_POS_PP_POS'] = feature_vector['P_POS']+'_'+feature_vector['PP_POS']
					if i-3 >= 0:
						feature_vector['PPP_POS'] = tag_sent[i-3][1]
					if i+2 < l:
						feature_vector['N_POS'] = tag_sent[i+2][1]
						next = tag_sent[i+2][0]
						feature_vector['NEXT'] = next.lower()
						feature_vector['N_SF'] = next[-3:].lower()
						if next[0].isupper():
							feature_vector['N_W_S'] = '1'

					if i+3 < l:
						feature_vector['NN_POS'] = tag_sent[i+3][1]
						feature_vector['NN_SF'] = tag_sent[i+3][0].lower()[-3:]
						feature_vector['N_POS_NN_POS'] = feature_vector['N_POS']+'_'+feature_vector['NN_POS']

					if i+4 < l:
						feature_vector['NNN_POS'] = tag_sent[i+4][1]
			
					context_string = ''
					for feature in feature_vector.keys():
						if feature_vector[feature] != '':
							context_string += feature+':'+feature_vector[feature]+' '
					clazz = percepclassify.classify(context_string, g_hash['i-i'])
					if feature_vector['W_S'] == '1':
						clazz = clazz[0].upper()+clazz[1:]
	

				print('marker')	
				print(word in ['you', 'they'] and i+1 < l and tag_sent[i+1][0] == "'re")
				if word in ['you', 'they'] and i+1 < l and tag_sent[i+1][0] == "'re":
					print('marker_in')
					word = word+"'re"
						
					if i-1 >= 0:
						feature_vector['P_POS'] = tag_sent[i-1][1]
						prev = tag_sent[i-1][0]
						feature_vector['PREV'] = prev.lower()
						feature_vector['P_SF'] = prev[-3:].lower()
						if prev[0].isupper():
							feature_vector['P_W_S'] = '1'
	
					if i-2 >= 0:
						feature_vector['PP_POS'] = tag_sent[i-2][1]
						feature_vector['PP_SF'] = tag_sent[i-2][0].lower()[-3:]
						feature_vector['P_POS_PP_POS'] = feature_vector['P_POS']+'_'+feature_vector['PP_POS']

					if i-3 >= 0:
						feature_vector['PPP_POS'] = tag_sent[i-3][1]
					if i+2 < l:
						feature_vector['N_POS'] = tag_sent[i+2][1]
						next = tag_sent[i+2][0]		
						feature_vector['NEXT'] = next.lower()
						feature_vector['N_SF'] = next[-3:].lower()
						if next[0].isupper():
							feature_vector['N_W_S'] = '1'
					if i+3 < l:
						feature_vector['NN_POS'] = tag_sent[i+3][1]
						feature_vector['NN_SF'] = tag_sent[i+3][0].lower()[-3:]
						feature_vector['N_POS_NN_POS'] = feature_vector['N_POS']+'_'+feature_vector['NN_POS']

					if i+4 < l:
						feature_vector['NNN_POS'] = tag_sent[i+4][1]
					
					
					context_string = ''
					for feature in feature_vector.keys():
						if feature_vector[feature] != '':
							context_string += feature+':'+feature_vector[feature]+' '
					if word == "you're":
						clazz = percepclassify.classify(context_string, g_hash['yo-yo'])
					if word == "they're":
						clazz = percepclassify.classify(context_string, g_hash['th-th'])
						print('class')
						print(clazz)
					if feature_vector['W_S'] == '1':
						clazz = clazz[0].upper() + clazz[1:]
				
					
				out_sent.append(clazz)
			out_sents.append(out_sent)
		return out_sents



	



def	get_sents(filename):
		f = open(filename, 'rU', errors = 'ignore')
		lines = f.readlines()
		f.close()
		sents = []
		for line in lines:
			sents.append(nltk.tokenize.word_tokenize(line))
		print('sents')
		print(sents)
		return sents


def	get_tagged_sents(sents):
		print(tag.get_tag_sents(sents))
		return tag.get_tag_sents(sents)



def	main():
		args = sys.argv[1:]
		if len(args) != 3:
			print('uasge: ./rectify.py model_dir test_file out_file')
			sys.exit(0)

		i_i_g_hash = percepclassify.get_g_hash_from_file(args[0]+'/i-i.model')
		lo_lo_g_hash = percepclassify.get_g_hash_from_file(args[0]+'/lo-lo.model')
		th_th_g_hash = percepclassify.get_g_hash_from_file(args[0]+'/th-th.model')
		to_too_g_hash = percepclassify.get_g_hash_from_file(args[0]+'/to-too.model')
		yo_yo_g_hash = percepclassify.get_g_hash_from_file(args[0]+'/yo-yo.model')
	
		g_hash = {'i-i':i_i_g_hash, 'lo-lo':lo_lo_g_hash, 'th-th':th_th_g_hash, 'to-too':to_too_g_hash, 'yo-yo':yo_yo_g_hash}

		print('tokenizing')
		sents = get_sents(args[1])
		print("taggin'")
		tag_sents = get_tagged_sents(sents)
		print("rectifyin'")
		out_lines = rectify(tag_sents, g_hash)

		print(out_lines)
	
			





if __name__ == '__main__':
	main()
