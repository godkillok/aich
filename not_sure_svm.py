import pandas as pd, numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import svm
import logging
import scipy
from sklearn.metrics import classification_report
from scipy.sparse import csr_matrix
from scipy.sparse import csr_matrix, vstack, hstack
#12813123
column = "passage"
column1="query"

train = pd.read_csv('../input_1/train.csv')
valid = pd.read_csv('../input_1/validation.csv')
test = pd.read_csv('../input_1/test.csv')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

print(train._info_axis)
print(train.shape)

test_id = test["query_id"].copy()
y=np.where(train["answer"]=='无法确定',0,1)

vec = TfidfVectorizer(ngram_range=(1,2),min_df=10, max_df=0.9,use_idf=1,smooth_idf=1, sublinear_tf=1,max_features=20000)
# fit_trams=(train[column]).copy()
# fit_trams.append((valid[column]).copy())
keys=['query_in_char',
'query_in_word',
'query_in_char_set',
'query_in_word_set',
'passage_len',
'ques_mark']
vec.fit_transform(train[column])
trn_term_doc =vec.transform(train[column])

for k in keys:
    bb=train[k].values
    bb=bb.reshape(bb.size,1)
    query_in_char=scipy.sparse.csr_matrix(bb)
    trn_term_doc=hstack((trn_term_doc, query_in_char))


# trn_term_doc=csr_matrix.todense(trn_term_doc)
# trn_term_doc
valid_term_doc = vec.transform(valid[column])
# valid_term_doc=csr_matrix.todense(valid_term_doc)
# for
# fid0=open('baseline.csv','w')
#'query_id','passage','query','alternatives','answer'
for k in keys:
    bb=valid[k].values
    bb=bb.reshape(bb.size,1)
    query_in_char=scipy.sparse.csr_matrix(bb)
    valid_term_doc=hstack((valid_term_doc, query_in_char))

lin_clf = svm.LinearSVC(class_weight='balanced',penalty='l2')
lin_clf.fit(trn_term_doc,y)
y_valid=np.where(valid["answer"]=='无法确定',0,1)
preds = lin_clf.predict(valid_term_doc)
print(classification_report(y_valid, preds))

preds = lin_clf.predict(trn_term_doc)
print(classification_report(y, preds))

#
# preds = lin_clf.predict(test_term_doc)
#
# i=0
# fid0.write("id,class"+"\n")
# for item in preds:
#     fid0.write(str(i)+","+str(item+1)+"\n")
#     i=i+1
# fid0.close()
co=0
for i,j,k,l in zip(preds,y_valid,valid[column],valid['query']):
    if i==0 and j==1:
        co+=1
        if co<50:
            print('{}---{}'.format(k,l))
