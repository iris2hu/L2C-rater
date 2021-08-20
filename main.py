import argparse
import time
import logging
import numpy as np
import pandas as pd
import scipy.stats
import xgboost as xgb
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from mord import LogisticAT, OrdinalRidge
from sklearn.metrics import mean_squared_error, confusion_matrix
from utils.text import *
from utils.text_repre import *
from linguistic import getLinguisticIndices
from stepwise_selection import *
from my_kappa_calculator import quadratic_weighted_kappa as qwk

# set logger
logging.basicConfig(filename='hsk.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# set argparse
parser = argparse.ArgumentParser()
parser.add_argument("-mp", "--modelpath", dest="model_path", type=str, metavar='<str>', default='./ltp_models',
                    help="the model directory")
parser.add_argument("-dp", "--datapath", dest="data_path", type=str, metavar='<str>', default='./data',
                    help="the input directory")
parser.add_argument("-m", "--feature_mode", dest="feature_mode", type=str, metavar='<str>', default='l',
                    help="feature mode (t|l|b)(default=l)")

parser.add_argument("-t", "--feature_type", dest="feature_type", type=str, metavar='<str>', default='c',
                    help="feature type (c|w|cw|wp|cwp) (default=c)")

parser.add_argument("--max_depth", dest="max_depth", type=int, metavar='<int>', default=40,
                    help="max_depth of random forest regressior")

parser.add_argument("--maxd_xgb", dest="maxd_xgb", type=int, metavar='<int>', default=3,
                    help="max_depth of XGBRegressor")
parser.add_argument("-lr", dest="learning_rate", type=float, metavar='<float>', default=0.05,
                    help="learning_rate of XGBRegressor")
parser.add_argument("--min_cw", dest="min_child_weight", type=int, metavar='<int>', default=5,
                    help="min_child_weight of XGBRegressor")
parser.add_argument("--n_estimators", dest="n_estimators", type=int, metavar='<int>', default=300,
                    help="n_estimators of XGBRegressor")
parser.add_argument("-gm", dest="gamma", type=int, metavar='<int>', default=5,
                    help="gamma of XBClassifier")

parser.add_argument("--olr_penalty", dest="olr_penalty", type=int, metavar='<float>', default=1.,
                    help="regular parameter for OLR. Zero value means no regularization")
parser.add_argument("--rdg_penalty", dest="rdg_penalty", type=int, metavar='<float>', default=1.,
                    help="regular parameter for Ridge")

parser.add_argument("--ngram_max", dest="max_n", type=int, metavar='<int>', default=1,
                    help="upper bound of ngram range")
parser.add_argument("--ngram_min", dest="min_n", type=int, metavar='<int>', default=1,
                    help="lower bound of ngram range")
parser.add_argument("--df_threshold", dest="min_df", type=int, metavar='<int>', default=10,
                    help="document frequency when building vocabulary")
args = parser.parse_args()

model_path = args.model_path
data_path = args.data_path
feature_mode = args.feature_mode
feature_type = args.feature_type
max_depth = args.max_depth
maxd_xgb = args.maxd_xgb
n_estimators = args.n_estimators
lr = args.learning_rate
min_child_weight = args.min_child_weight
gamma = args.gamma
olr_penalty = args.olr_penalty
rdg_penalty = args.rdg_penalty
max_n = args.max_n
min_n = args.min_n
min_df = args.min_df

logger.info("feature_mode: " + str(feature_mode))
logger.info("feature_type: " + str(feature_type))
logger.info("n-grams range: [ %s, %s]" % (str(min_n), str(max_n)))
logger.info("term frequency threshold: " + str(min_df))

t1 = time.time()

# Generating Linguistics Features 
index_data = {}
corpus = []
df_data = pd.read_csv(data_path + '/essay_revised.csv')

# shuffle
# df_data = shuffle(df_data)
# df_data = df_data.reset_index(drop=True)

segmentor, postagger, parser = load_ltpmodel(model_path)

for index, row in df_data.iterrows():
    essay_id, essay_text, essay_score = row['essay_ID'], row['ESSAY'], row['SCORE']
    text_dict = text_process(essay_text, segmentor, postagger, parser)
    # build corpus for "text|both" feature setting using the text_dict, the parsing results from ltp
    if feature_mode in ['t', 'b']:
        corpus_line = get_text_feature_from_ltp_results(essay_text, text_dict, feature=feature_type)
        corpus.append(corpus_line)
    indices = getLinguisticIndices(text_dict)
    indices['essay_ID'] = essay_id
    indices['SCORE'] = essay_score
    index_data[index] = indices

release_ltpmodel(segmentor, postagger, parser)

df_ling = pd.DataFrame.from_dict(index_data, orient='index')

for column_name in df_ling.columns:
    if column_name not in ['SCORE', 'essay_ID']:
        x = df_ling[column_name].values.reshape(-1, 1)
        min_max_scaler = MinMaxScaler()
        df_ling[column_name] = min_max_scaler.fit_transform(x)

df_ling = df_ling.fillna(0)
df_ling.to_csv(data_path + '/essay_linguistic_indices.csv', index=False)

ling_name = list(df_ling.columns)
ling_name.remove('essay_ID')

# Get effective linguistic feature stepwise regression
logger.info('>>>>>>>>> STEPWISE REGRESSION <<<<<<<<<')
features_automatic = stepwiseSelection(df_ling.filter(items=ling_name), 'SCORE', verbose=False)
logger.info(f'Linguistics Features Selected:\n{features_automatic}')

if feature_mode == 't':  # text mode
    # Get text representation
    X = get_text_matrix(corpus, ngram_min=min_n, ngram_max=max_n, df_threshold=min_df)
    Y = np.array([score2ord[score] for score in df_data['SCORE']])
    
elif feature_mode == 'l':  # ling mode
    # Get linguistic Feature Vec
    X = np.array(df_ling.filter(items=features_automatic))
    Y = np.array([score2ord[score] for score in df_ling['SCORE']])

else:  # both mode
    # Get text representation
    txt_vec = get_text_matrix(corpus, ngram_min=min_n, ngram_max=max_n, 
                               df_threshold=min_df, sparse=True)
    # Get linguistic Feature Vec
    lng_vec = np.array(df_ling.filter(items=features_automatic))
    X = np.concatenate((txt_vec, lng_vec), axis=1)
    Y = np.array([score2ord[score] for score in df_ling['SCORE']])


# Set models and their parameters
# Note that OrdinalRidge and Ridge Regression are identical
models = {
          'LinearRegression': LinearRegression(),
          'Ridge': Ridge(alpha=rdg_penalty),
          'RandomForestRegressor': RandomForestRegressor(max_depth=max_depth, random_state=0),
          'XGBRegressor': xgb.XGBRegressor(max_depth=maxd_xgb,
                                           learning_rate=lr,
                                           n_estimators=n_estimators,
                                           min_child_weight=min_child_weight,
                                           subsample=0.7,
                                           colsample_bytree=0.7,
                                           reg_alpha=0,
                                           reg_lambda=0,
                                           silent=True,
                                           objective='reg:gamma',
                                           missing=None,
                                           seed=123,
                                           gamma=gamma),
          'LogisticRegression': LogisticRegression(max_iter=1000),
          'OrderedLR_LogisticAT': LogisticAT(alpha=olr_penalty)
          # 'OrdinalRidge': OrdinalRidge(alpha=olr_penalty)
          }

# train/dev/test split
# Rewrite following codes according to your data
X_tr_val = X[:90]
Y_tr_val = Y[:90]
X_test = X[90:]
Y_test = Y[90:]

X_lst = np.array_split(X_tr_val, 5)
Y_lst = np.array_split(Y_tr_val, 5)

logger.info('>>>>>>>>>> Cross Validation <<<<<<<<<')

# split train_valid to train/valid/test and CV
for i in range(5):
    X_frame = list()
    Y_frame = list()
    for j in range(5):
        if j != i:
            X_frame.append(X_lst[j])
            Y_frame.append(Y_lst[j])
    X_train = np.concatenate(X_frame, axis=0)
    Y_train = np.concatenate(Y_frame, axis=0)
    X_valid = X_lst[i]
    Y_valid = Y_lst[i]

    # write shape of train/dev/test in log
    logger.info('\n########## Fold {} ##########'.format(i+1))
    logger.info(f'tr: {X_train.shape} dev: {X_valid.shape} ts: {X_test.shape}')
    logger.info(f'tr: {Y_train.shape} dev: {Y_valid.shape} ts: {Y_test.shape}')

    for name, lm in models.items():
        logger.info('\n=========== {} ============'.format(name))
        lm.fit(X_train, Y_train)

        # predict
        Y_train_pred = lm.predict(X_train)
        Y_valid_pred = lm.predict(X_valid)
        Y_test_pred = lm.predict(X_test)

        # Modified too small values to the lower bound 0
        # Modified too large values to the upper bound 11
        Y_train_pred[np.where(Y_train_pred < 0)] = 0
        Y_train_pred[np.where(Y_train_pred > 11)] = 11
        Y_valid_pred[np.where(Y_valid_pred < 0)] = 0
        Y_valid_pred[np.where(Y_valid_pred > 11)] = 11
        Y_test_pred[np.where(Y_test_pred < 0)] = 0
        Y_test_pred[np.where(Y_test_pred > 11)] = 11

        # transform predicted values to integer
        Y_train_pred_int = np.rint(Y_train_pred).astype('int32')
        Y_valid_pred_int = np.rint(Y_valid_pred).astype('int32')
        Y_test_pred_int = np.rint(Y_test_pred).astype('int32')

        # output
        logger.info(f'[TRAIN QWK] {qwk(Y_train, Y_train_pred_int, 0, 11)}')
        logger.info(f'[VALID QWK] {qwk(Y_valid, Y_valid_pred_int, 0, 11)}')
        logger.info(f'[TEST QWK]  {qwk(Y_test, Y_test_pred_int,  0, 11)}')

        train_rmse = np.sqrt(mean_squared_error(Y_train, Y_train_pred_int))
        valid_rmse = np.sqrt(mean_squared_error(Y_valid, Y_valid_pred_int))
        test_rmse = np.sqrt(mean_squared_error(Y_test, Y_test_pred_int))
        logger.info(f'[TRAIN RMSE] {train_rmse}')
        logger.info(f'[VALID RMSE] {valid_rmse}')
        logger.info(f'[TEST RMSE] {test_rmse}')

        train_pears = scipy.stats.pearsonr(Y_train, Y_train_pred_int)
        valid_pears = scipy.stats.pearsonr(Y_valid, Y_valid_pred_int)
        test_pears = scipy.stats.pearsonr(Y_test, Y_test_pred_int)
        logger.info(f'[TRAIN PEARS] {train_pears[0]}')
        logger.info(f'[VALID PEARS] {valid_pears[0]}')
        logger.info(f'[TEST PEARS] {test_pears[0]}')

t2 = time.time()
logger.info('\nMain Program Runs for %s s' % str(t2-t1))
logger.info('===============================================================\n')
