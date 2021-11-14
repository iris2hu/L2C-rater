from math import sqrt
import numpy as np
from utils.hsk import *
from utils.clausal import *
from utils.coll import *
from utils.bidep import *
from utils.const import *


def get_lexical_indices(text_wordlist, text_level_dict):
    lexical_indices = {}
    sophistication2 = (text_level_dict[5] + text_level_dict[6] + text_level_dict[7]) / sqrt(len(text_wordlist))
    lexical_indices['LEXICAL_RTTR'] = len(set(text_wordlist)) / sqrt(len(text_wordlist))
    lexical_indices['LEXICAL_SOP2'] = sophistication2
    return lexical_indices


def get_clausal_indices(sent_length_list, clause_length_list, T_unit_length_list, max_depth_list):
    clausal_indices = {}
    # length based
    clausal_indices['MLS'] = np.mean(sent_length_list)
    clausal_indices['MLC'] = np.mean(clause_length_list)
    clausal_indices['MLTU'] = np.mean(T_unit_length_list)
    # unit based
    clausal_indices['NCPS'] = len(clause_length_list) / len(sent_length_list)
    clausal_indices['NTPS'] = len(T_unit_length_list) / len(sent_length_list)
    # tree based
    clausal_indices['MEAN_TREE_DEPTH'] = np.mean(max_depth_list)
    clausal_indices['MAX_TREE_DEPTH'] = max(max_depth_list)
    return clausal_indices


def get_coll_indices(collocation_list):
    coll_indices = {}
    coll_num = len(collocation_list)
    sqrt_coll_num = sqrt(coll_num)

    # coll_RTTR
    set_colls = set(collocation_list)
    coll_indices['COLL_RTTR'] = len(set_colls) / sqrt_coll_num

    # unique_RTTR
    unique_colls = [coll for coll in collocation_list if isUniqueColl(coll)]
    set_unique_colls = set(unique_colls)
    coll_indices['UNIQUE_RTTR'] = len(set_unique_colls) / (sqrt(len(unique_colls)) + 1)

    # general_RTTR
    general_colls = [coll for coll in collocation_list if coll not in set_unique_colls]
    set_general_colls = set(general_colls)
    general_coll_diversity = len(set_general_colls) / sqrt(len(general_colls))
    coll_indices['GENERAL_RTTR'] = general_coll_diversity

    # unique_RATIO
    # coll_indices['UNIQUE_RATIO2'] = len(unique_colls) / coll_num
    coll_indices['UNIQUE_RATIO2'] = len(unique_colls) / sqrt_coll_num

    # lowfreq_RATIO
    lowfreq_collls = [coll for coll in collocation_list if isLowFreqColl(coll)]
    # coll_indices['LOWFREQ_RATIO1'] = len(lowfreq_collls) / coll_num
    coll_indices['LOWFREQ_RATIO2'] = len(lowfreq_collls) / sqrt_coll_num

    # coll indices based on different types
    coll_types = ['VO', 'SP', 'AN', 'AP', 'CN*', 'PP*', 'PV*', 'PC*']
    coll_type_dict = {k: [] for k in coll_types}

    for coll in collocation_list:
        typ = coll_dict[coll.split('\t')[-1]]
        coll_type_dict[typ].append(coll)

    for ct, v in coll_type_dict.items():
        coll_indices[ct + '_RATIO'] = len(v) / len(collocation_list)
        coll_indices[ct + '_RTTR'] = 0
        if v:
            coll_indices[ct + '_RTTR'] = len(set(v)) / sqrt(len(v))

    return coll_indices


def get_ngram_indices(text_bigrams, text_trigrams):
    '''
    param: 
     - text_bigrams: <type> list
     - text_trigrams: <type> dict
    return :
     - ngram_indices: <type> dict
       * bi_rttr, bi_sop2
       * tri_rttr, tri_sop2
       * each type of dep: rttr, ratio
    '''
    ngram_indices = {}
    trigram_list = []
    for trigrams in text_trigrams.values():
        trigram_list.extend(trigrams)

    # diversity
    ngram_indices['BIGRAM_RTTR'] = len(set(text_bigrams)) / sqrt(len(text_bigrams))
    ngram_indices['DEP_RTTR'] = len(set(trigram_list)) / sqrt(len(trigram_list))

    # sophistication
    sophis_bi = [b for b in text_bigrams if is_sophis_bigram(b)]
    sophis_tri = [t for t in trigram_list if is_sophis_trigram(t)]
    # bi_sop1 = len(sophis_bi) / len(text_bigrams)
    ngram_indices['BIGRAM_SOP2'] = len(sophis_bi) / sqrt(len(text_bigrams))
    # tri_sop1 = len(sophis_tri) / len(trigram_list)
    ngram_indices['DEP_SOP2'] = len(sophis_tri) / sqrt(len(trigram_list))

    # rttr and ratio for each dep label
    deplabels = ["HED", "COO", "SBV", "ADV", "ATT", "VOB", "FOB", "POB", "IOB", "DBL", "RAD", "CMP", "LAD"]
    for label in deplabels:
        ngram_indices[label + '_RTTR'] = 0
        ngram_indices[label + '_RATIO'] = 0
        if label in text_trigrams:
            trigrams = text_trigrams[label]
            ngram_indices[label + '_RTTR'] = len(set(trigrams)) / sqrt(len(trigrams))
            ngram_indices[label + '_RATIO'] = len(trigrams) / len(trigram_list)

    return ngram_indices


def get_dep_distance(depdist):
    dist_indices = {}
    sum_dist, num_dist = 0, 0

    deplabels = ["COO", "SBV", "ADV", "ATT", "VOB", "FOB", "POB", "IOB", "DBL", "RAD", "CMP", "LAD"]
    for label in deplabels:
        dist_indices[label + '_DIST'] = 0
        if label in depdist:
            distances = depdist[label]
            dist_indices[label + '_DIST'] = np.mean(distances)
            sum_dist += sum(distances)
            num_dist += len(distances)

    dist_indices['MEAN_DIST'] = sum_dist / num_dist

    return dist_indices


def get_construction_indices(constructions, text_length, const_num):
    '''
    ratio and density indices from level 1 to 5
    '''
    const_indices = {'CONST_DENSITY': const_num / text_length}

    for i in range(1, 6):
        level_const = constructions[i]
        const_indices['CONST' + str(i) + '_RATIO'] = len(level_const) / const_num
        const_indices['CONST' + str(i) + '_DENSITY'] = len(level_const) / text_length

    # combine level 1&2 to low, level 4&5 to high, level 3 by default the mid
    const_indices['CONST_LOW_RATIO'] = const_indices['CONST1_RATIO'] + const_indices['CONST2_RATIO']
    const_indices['CONST_HIGH_RATIO'] = const_indices['CONST4_RATIO'] + const_indices['CONST5_RATIO']
    const_indices['CONST_LOW_DENSITY'] = const_indices['CONST1_DENSITY'] + const_indices['CONST2_DENSITY']
    const_indices['CONST_HIGH_DENSITY'] = const_indices['CONST4_DENSITY'] + const_indices['CONST5_DENSITY']

    return const_indices


def getLinguisticIndices(text_dict):
    ''' lexical
        clausal
        collocation based
        bigram and dependency based
        construction based
    '''

    indices = {}

    # for lexical
    text_wordlist, text_level_dict = [], {k: 0 for k in range(1, 8)}

    # for clausal: length based
    sent_length_list, clause_length_list, T_unit_length_list = [], [], []

    # for clausal: tree based
    max_depth_list = []

    # for collocation
    collocation_list = []

    # for bigram and dependency triples
    text_bigrams, text_trigrams, text_depdists = [], {}, {}

    # text constructions
    text_constructions = {i: [] for i in range(1, 6)}

    # get linguistic features for one text
    for sent_id, info in text_dict.items():

        sent, wordlist, wplist = info['sent'], info['wordlist'], info['wplist']
        worddict = info['worddict']

        # lexical features
        level_dict = level_analyze(sent, wordlist, wplist)
        wordlist = [w for w in wordlist if isWordChinese(w)]  # 去除标点数字英文等
        text_wordlist.extend(wordlist)
        for level, wl in level_dict.items():
            text_level_dict[level] += wl

        # clausal units
        if not re.search('[，。？！；……]', sent):
            continue
        sent_length, clause_lengths, T_unit_lengths = clausal_index(sent, worddict)
        sent_length_list.append(sent_length)
        clause_length_list.extend(clause_lengths)
        T_unit_length_list.extend(T_unit_lengths)
        max_depth = getTreePath(worddict)
        max_depth_list.append(max_depth)

        # collocations
        collocations = getColl(worddict)
        collocation_list.extend(collocations)

        # bigrams and dependency trigrams
        bigrams = get_bigrams(wplist)
        text_bigrams.extend(bigrams)
        text_trigrams, text_depdists = get_dep_trigrams(worddict, text_trigrams, text_depdists)

        # constructions
        text_constructions = getLevelConstruction(worddict, sent, text_constructions)

        ############### linguistic feature extraction done ###############

    # update length indices
    text_length = sum(sent_length_list)
    indices['CHAR_NUM'] = text_length
    indices['WORD_NUM'] = len(text_wordlist)

    # update lexical indices
    if len(text_wordlist):
        lexical_indices = get_lexical_indices(text_wordlist, text_level_dict)
        indices.update(lexical_indices)

    # udpate clausal indices
    if sent_length_list:
        clausal_indices = get_clausal_indices(sent_length_list, clause_length_list, T_unit_length_list, max_depth_list)
        indices.update(clausal_indices)

    # update collocation based indices
    if collocation_list:
        coll_indices = get_coll_indices(collocation_list)
        indices.update(coll_indices)

    # update bigram and dependency based indices
    if text_bigrams:
        ngram_indices = get_ngram_indices(text_bigrams, text_trigrams)
        dist_indices = get_dep_distance(text_depdists)
        indices.update(ngram_indices)
        indices.update(dist_indices)

    const_num = sum([len(v) for v in text_constructions.values()])
    if const_num:
        const_indices = get_construction_indices(text_constructions, text_length, const_num)
        indices.update(const_indices)

    return indices
