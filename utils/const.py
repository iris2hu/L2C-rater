'''
get construction features from level 1 to 5
'''

# construction vocabulary 
questionMarks_1 = ['什么', '谁', '哪', '哪儿', '几', '多少', '多大', '什么时候']
questionMarks_2 = ['怎么样', '可以吗', '行吗', '好吗']
conjunction = {'先': -1, '再': 1, '因为': -2, '所以': 2, '如果': -3, '要是': -3, '既然': -3, '就': 3, '不但': -4, '而且': 4, '虽然': -5,
               '但是': 5, '即使': -6, '宁可': -6, '也': 6, '无论': -7, '都': 7, '不是': -8, '就是': 8}
c_level5 = ['既然', '即使', '无论', '不是', '就是', '宁可']
direction = ['上', '下', '来', '去', '上来', '上去', '下来', '下去', '进', '出', '进来', '进去', '出去', '出来', '过来', '过去', '回', '回来', '回去',
             '起', '起来']


def getLevelConstruction(words, sent, construction):
    '''
    words: <type> dict
    sent: <type> str
    construction: <type> dict
    '''
    pair1, pair2, c1, c2 = 0, 0, '', ''
    for key, value in words.items():
        if value['cont'] in conjunction.keys() and value['pos'] in ['c', 'd']:
            if c1:
                c2 = value['cont']
                pair2 = conjunction[c2]
                if pair1 + pair2 == 0:
                    if pair1 < 0:
                        c2 = 'CC_' + c1 + '……' + c2
                    elif pair1 > 0:
                        c2 = 'CC_' + c2 + '……' + c1
                    if c1 in c_level5 or c2 in c_level5:
                        construction[5].append(c2)
                    else:
                        construction[4].append(c2)
            else:
                c1 = value['cont']
                pair1 = conjunction[c1]
        parent_id = int(value['parent'])
        ## LEVEL 1
        if value['relate'] == 'HED' and value['pos'] == 'a':
            construction[1].append('形容词谓语句')
        elif value['cont'] in ['吗', '吧', '呢'] and key + 1 in words and words[key + 1]['cont'] in ['？', '?']:
            question_marks = questionMarks_1 + questionMarks_2
            match = map(sent.find, question_marks)
            if max(match) == -1:
                construction[1].append('一般疑问句')
        elif value['pos'] == 'd' and value['relate'] == 'ADV':
            if value['cont'] in ['很', '非常', '真', '太']:
                construction[1].append('程度副词')
            elif value['cont'] in ['不', '没'] and key - 1 in words and key + 1 in words and words[key - 1]['cont'] == \
                    words[key + 1]['cont'] and '？' in sent:
                construction[3].append('正反疑问句')
            elif value['cont'] == '不':
                construction[1].append('否定句_“不”')
            elif value['cont'] in ['没有', '没']:
                if words[parent_id]['pos'] in ['v', 'p']:
                    construction[3].append('否定句_“没/没有”')
                elif words[parent_id]['pos'] == 'a':
                    construction[3].append('比较句2')
            elif value['cont'] in ['也', '都']:
                construction[2].append('范围副词')
            elif value['cont'] == '最':
                construction[3].append('副词“最”')
            elif value['cont'] in ['还', '已经', '就', '才', '再', '又']:
                construction[4].append('时间副词')
            elif value['cont'] == '还是' and '？' in sent:
                construction[3].append('选择疑问句')
            elif value['cont'] in ['在', '正在', '正']:
                construction[3].append('事件正在进行的表达')
        ## Prepositional phrase
        elif value['pos'] == 'p' and value['relate'] == 'ADV':
            if value['cont'] == '在' and words[key + 1]['pos'] != 'v':
                construction[2].append('地点状语')
            elif value['cont'] in ['从', '向', '往']:
                construction[3].append('介词短语_方向')
            elif value['cont'] in ['跟', '和', '与']:
                if words[parent_id]['pos'] == 'v':
                    construction[3].append('介词短语_对象')
                elif '一样' in sent or '差不多' in sent:
                    construction[3].append('比较句3')
            elif value['cont'] in ['给', '对']:
                construction[3].append('介词短语_对象')
            elif value['cont'] == '比':
                if (words.__contains__(parent_id - 1) and words[parent_id - 1]['cont'] in ['还', '更']) or (
                        words.__contains__(parent_id + 1) and words[parent_id + 1]['pos'] != 'wp'):
                    construction[4].append('比较句1_四级')
                else:
                    construction[3].append('比较句1_三级')
            elif value['cont'] == '把':
                construction[5].append('把字句')
            elif value['cont'] == '被':
                construction[5].append('被动句_“被”')
        elif value['pos'] == 'nt' and value['relate'] == 'ADV':
            construction[2].append('时间状语')
        elif value['pos'] == 'nd':
            if value['relate'] == 'POB' and words[parent_id]['cont'] == '在' and words[parent_id]['relate'] == 'HED':
                construction[2].append('在字句')
            elif value['relate'] == 'ADV' and parent_id == key + 1 and words[parent_id][
                'pos'] == 'v' and key + 2 in words and words[key + 2]['cont'] == '着':
                construction[3].append('存现句2')
            else:
                construction[2].append('方位词(组)')
        elif value['relate'] == 'HED' and value['cont'] in ['是', '有'] and key - 1 in words and words[key - 1][
            'pos'] == 'nd':
            construction[2].append('存现句1')
        elif value['cont'] == '离' and value['relate'] == 'HED':
            construction[2].append('距离表达')
        elif value['cont'] == '要' and value['relate'] == 'ADV':  # 要
            construction[2].append('意愿表达')
        elif value['cont'] == '想' and value['relate'] == 'HED' and words[key + 1]['pos'] in ['v', 'p']:  # 想
            construction[2].append('意愿表达')
        elif value['cont'] == '的' and key - 1 in words and words[key - 1]['pos'] in ['a', 'r', 'n']:
            construction[2].append('的字结构')
        elif value['cont'] in ['一', '了'] and key - 1 in words and key + 1 in words and words[key - 1]['cont'] == \
                words[key + 1]['cont'] and words[key - 1]['pos'] == 'v' and words[key + 1]['pos'] == 'v':
            construction[2].append('动词重叠2')
        elif value['relate'] == 'COO' and value['pos'] == 'v' and parent_id == key - 1 and value['cont'] == \
                words[parent_id]['cont']:
            construction[2].append('动词重叠1')
        elif value['pos'] == 'q':
            if value['relate'] == 'CMP':
                construction[4].append('时量/动量补语')
            elif value['relate'] == 'ATT':
                construction[2].append('常用量词')
        ## LEVEL 3
        elif value['cont'] in ['了', '着']:
            construction[3].append('助词_“了/着”')  ####四级：该*了，（就/快）要*了，能/会/可以*了，不*了，V了就/再V
        elif value['relate'] == 'IOB':
            construction[3].append('双宾语句')
        elif value['relate'] == 'COO' and value['pos'] == 'v' and value['cont'] != words[parent_id]['cont'] and \
                words[parent_id]['pos'] == 'v':
            temp_poslist = []
            for num in range(min(key, parent_id), max(key, parent_id)):
                temp_poslist.append(words[num]['pos'])
            if 'wp' not in temp_poslist:
                construction[3].append('连动句')
        elif value['cont'] in ['怎么', '怎样', '如何'] and '？' in sent:
            construction[3].append('特殊疑问句2')  # 询问方式
        elif value['cont'] in ['能', '会', '可以', '愿意'] and value['relate'] == 'ADV':
            construction[3].append('能愿动词')
        elif value['pos'] == '' and value['cont'] == '过':
            construction[4].append('助词_“过”')
        elif value['relate'] == 'DBL':
            construction[4].append('兼语句')
        elif value['pos'] == 'v' and value['relate'] == 'VOB' and words[parent_id]['cont'] == '是' and words[parent_id][
            'relate'] == 'HED' and key + 1 in words and words[key + 1]['cont'] == '的' and key + 2 in words and \
                words[key + 2]['cont'] == '。':
            construction[4].append('是……的')
        elif value['relate'] == 'CMP':
            if value['cont'] in direction:
                construction[5].append('趋向补语')
            elif value['pos'] in ['a', 'v', 'i']:
                construction[5].append('结果/程度补语')
            elif value['pos'] == 'p':
                construction[5].append('地点补语')
            elif value['pos'] == 'm' or value['cont'] == '小时':
                construction[4].append('时量/动量补语')
        elif value['relate'] == 'FOB' and '被' not in sent:
            construction[5].append('被动句_无标记')
    match = map(sent.find, questionMarks_1)
    if max(match) > -1 and '？' in sent:
        construction[2].append('特殊疑问句1')  # 疑问代词
    match = map(sent.find, questionMarks_2)
    if max(match) > -1 and '？' in sent:
        construction[3].append('特殊疑问句3')  # 询问意见
    if '怎么了？' in sent:
        construction[4].append('特殊疑问句4')  # 询问情况

    return construction
