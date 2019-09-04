import pandas as pd
import numpy as np
#import boto
#import boto3
import nltk
from nltk.tag import StanfordNERTagger
import time
from multiprocessing import Pool
import sys
from tqdm import tqdm

# depend on user path
# cloud path
# st = StanfordNERTagger('/home/ec2-user/GKGPreprocessing/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
#                        '/home/ec2-user/GKGPreprocessing/stanford-ner-2018-10-16/stanford-ner-3.9.2.jar',
#                        encoding='utf-8')
# Local path
st = StanfordNERTagger('/Users/fanliang/Downloads/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/Users/fanliang/Downloads/stanford-ner-2018-10-16/stanford-ner-3.9.2.jar',
                       encoding='utf-8')
def getDecision(input_list):
    for item in input_list:
        if item[1] == 'ORGANIZATION':
            return "Yes"
            break   
    return "No"

def ner_result(input_str):
    new_str = [w.capitalize() for w in input_str.split(' ')]
    classified_text = st.tag(new_str)
    return getDecision(classified_text)

def main(start_num,end_num,file_num):
	# The following command is cloud version
	# file_path = 's3://gkgpreprocessing/'
	# file_name = 'df_{}.csv'.format(file_num)
	# output_file = 'df_{}_{}_{}.csv'.format(file_num,start_num,end_num)
	# new_df = pd.read_csv(file_path + file_name ,index_col='Unnamed: 0')

	# Local version
	# Since in our project, the file are orgnized in a sequence of numbers
	# For the test version, we treat the file number as the file name
	output_file = 'test{}_{}.csv'.format(start_num,end_num)
	new_df = pd.read_csv(file_num, index_col='Unnamed: 0')

	parsed_df = new_df.loc[start_num:end_num].copy()
	original_name = list(parsed_df['original_name'])
	cleaned_name = list(parsed_df['cleaned_name'])

	#s = time.time()
	p = Pool()
	result = p.map(ner_result,cleaned_name)
	p.close()
	p.join()
	

	for i in range(len(result)):
		temp_decision = result[i]
		if temp_decision == 'Yes':
			with open (output_file,'a') as f:
				f.write('{},{}\n'.format(original_name[i],cleaned_name[i]))
				f.close()
		else:
			pass

if __name__ == '__main__':

	file_name = sys.argv[1]
	# cloud file_name version
	# file_name = int(file_name)

	start_end_file = sys.argv[2]

	with open (start_end_file,'r') as f:
		whole_str = f.read()
		line_list = whole_str.split('\n')[:-1]
		f.close()

	for line in tqdm(line_list):
		start = line.split(',')[0]
		end = line.split(',')[1]
		main(int(start),int(end),file_name)


