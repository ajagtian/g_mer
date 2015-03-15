#!/usr/bin/python3 -tt

import ast
import sys

def	get_tag_sents(filename):
		tag_sents = []
		f = open(filename, 'rU', errors = 'ignore')
		lines = f.readlines()
		f.close()
		i = 1
		l = len(lines)
		progress = 0
		print ('reading corpus')
		for line in lines:
			if ((i/l)*100 - progress) >= 3:
				progress = (i/l)*100
				print('progress ... '+str(progress))
			
			tag_sents.append(ast.literal_eval(line))
			i += 1
		
		return tag_sents

		



def	parse(tag_sents, training_dir):
		print ('extracting classes')
		f_to_to = open(training_dir+'/to-too', 'w')
		f_i_i = open(training_dir+'/i-i', 'w')
		f_th_th = open(training_dir+'/th-th', 'w')
		f_lo_lo= open(training_dir+'/lo-lo', 'w')
		f_yo_yo = open(training_dir+'/yo-yo', 'w')
		# P_POS, PP_POS, PPP_POS, N_POS, NN_POS, NNN_POS, 
		p = 1
		ll = len(tag_sents)
		progress = 0
		for tag_sent in tag_sents:
			if ((p/ll)*100 - progress) >= 2:
				progress = (p/ll)*100
				print('progress ... '+str(progress))
			p += 1
			l = len(tag_sent)
			for i in range(len(tag_sent)):
				feature_vector = {'CL':'','P_POS':'P_BS', 'PP_POS':'PP_BS', 'PPP_POS':'PPP_BS', 'N_POS':'N_ES', 'NN_POS':'NN_ES', 'NNN_POS':'NNN_ES', 'W_S':'0', 'PREV':'BOS', 'NEXT':'', 'P_SF':'P_SF', 'PP_SF':'PP_SF', 'N_SF':'', 'NN_SF':'', 'P_W_S':'0', 'N_W_S':'0', 'P_POS_PP_POS':'', 'N_POS_NN_POS':''}
				tag_word = tag_sent[i]
				if tag_word[0][0].isupper():
					feature_vector['W_S'] = str(1)
				word = tag_word[0].lower()
				pos = tag_word[1]
				if word in ['its', 'your', 'their', 'loose', 'lose', 'to', 'too', "it's", "you're", "they're"]:
					feature_vector['CL'] = word
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
						
				
				
					context_string = feature_vector['CL'] + ' '
					for feature in feature_vector.keys():
						if feature != 'CL' and feature_vector[feature] != '':
							context_string += feature+':'+feature_vector[feature]+' '
					if word in ["its","it's"]:
						f = f_i_i
					if word in ["they're","their"]:
						f = f_th_th
					if word in ["too","to"]:
						f = f_to_to
					if word in ["loose", "lose"]:
						f = f_lo_lo
					if word in ["your","you're"]:
						f = f_yo_yo
					f.write(context_string+'\n')




				elif word == 'it' and i+1 < l and tag_sent[i+1][0] in ["is", "'s", 'was']:
					word = "it's"
					
					feature_vector['CL'] = word
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
			
					context_string = feature_vector['CL'] + ' '
					for feature in feature_vector.keys():
						if feature != 'CL' and feature_vector[feature] != '':
							context_string += feature+':'+feature_vector[feature]+' '
					if word in ["its","it's"]:
						f = f_i_i
					if word in ["they're","their"]:
						f = f_th_th
					if word in ["too","to"]:
						f = f_to_to
					if word in ["loose", "lose"]:
						f = f_lo_lo
					if word in ["your","you're"]:
						f = f_yo_yo
					f.write(context_string+'\n')
	

			
				elif word in ['you', 'they'] and i+1 < l and tag_sent[i+1][0] in ["'re", "are", "were"]:
					word = word+"'re"
						
					feature_vector['CL'] = word
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
					
					
					context_string = feature_vector['CL'] + ' '
					for feature in feature_vector.keys():
						if feature != 'CL' and feature_vector[feature] != '':
							context_string += feature+':'+feature_vector[feature]+' '
					if word in ["its","it's"]:
						f = f_i_i
					if word in ["they're","their"]:
						f = f_th_th
					if word in ["too","to"]:
						f = f_to_to
					if word in ["loose", "lose"]:
						f = f_lo_lo
					if word in ["your","you're"]:
						f = f_yo_yo
					f.write(context_string+'\n')
					
				
					


	
def	main():
		args = sys.argv[1:]
		if len(args) != 2:	
			print('usage: ./tokenize.py pos_tagged_corpus training_dir')
			sys.exit(0)


		tag_sents = get_tag_sents(args[0])
		parse(tag_sents, args[1])






if __name__ == '__main__':
	main()
