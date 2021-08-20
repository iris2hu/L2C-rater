'''
clausal features
'''


def CHNlen(seq):
    '''
    seq: a sequence of chars
    return: the number of Chinese chars
    '''
    seq = [c for c in seq if c >= '\u4e00' and c <= '\u9fff']
    return len(seq)


def merge_T_units(candidates):
    results = []

    for i, c in enumerate(candidates):
        is_T, tsr = c[0], c[1]
        if is_T:
            results.append(tsr)
        elif results:
            # 跟前面
            results[-1] = results[-1] + tsr
        elif i < len(candidates) - 1:
            # 前面没有，跟后面
            candidates[i + 1] = [candidates[i + 1][0], tsr + candidates[i + 1][1]]

    return results


def clausal_index(sent_cont, word_dict):
    '''
    return : length of a sentence, [length of clauses], [length of T-Units]
    '''

    sent_str, clause_str = '', ''
    clause_lengths = []
    candidate_T_units = []
    tmp_info = []

    for k, v in word_dict.items():
        word, pos = v['cont'], v['pos']

        if pos in ['wp', 'ws']:
            if word in ['，', ',', '；', ';', '。', '？', '?', '！', '!']:
                if clause_str:
                    clause_lengths.append(CHNlen(clause_str))

                    # T-unit detection
                    is_Tunit = False
                    for info in tmp_info:
                        if info['relate'] in ['HED']:
                            is_Tunit = True
                        elif info['relate'] == 'COO':
                            parent_id = int(info['parent'])
                            if word_dict[parent_id]['relate'] == 'HED':
                                is_Tunit = True
                            elif word_dict[parent_id]['relate'] == 'COO':
                                grandfather_id = int(word_dict[parent_id]['parent'])
                                if word_dict[grandfather_id]['relate'] == 'HED':
                                    is_Tunit = True
                            if info['pos'] in ['v', 'a', 'p']:
                                is_Tunit = True

                    candidate_T_units.append([is_Tunit, clause_str])
                    tmp_info, clause_str = [], ''

        else:
            clause_str += word
            sent_str += word
            tmp_info.append(v)

    current_T_units = merge_T_units(candidate_T_units)
    T_unit_lengths = [CHNlen(unit) for unit in current_T_units]

    return CHNlen(sent_str), clause_lengths, T_unit_lengths


def getTreePath(word_dict):
    '''
        return max_depth, average_depth
    '''
    paths = []
    temp_parents = []
    for k, v in word_dict.items():
        if k in temp_parents:
            continue
        current_id = k
        parent_id = current_id
        current_path = [current_id]
        while parent_id != -1:
            parent_id = word_dict[parent_id]['parent']
            temp_parents.append(parent_id)
            current_path.append(parent_id)
        paths.append(current_path)
    sort_path = sorted(paths, key=len, reverse=True)
    max_depth = len(sort_path[0])
    # average_depth = sum([len(p) for p in paths]) / len(paths)
    return max_depth
