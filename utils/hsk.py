import re
import pickle as p

# load vocabulary data
with open('./dict/vocab_info.data', 'rb') as f:
    vocab_data = p.load(f)

hsk_ambiguous = vocab_data['hsk_ambiguous']
hsk_5000 = vocab_data['hsk_5000']
hsk_all = vocab_data['hsk_all']
chars = vocab_data['chars']
jzcz = vocab_data['jzcz']


def diambiguate_level(word, pos, posseg, loc):
    if word == '得':
        if pos == 'u':
            return 'hsk2'
        else:
            return 'hsk4'  # v, d

    if word == '等':
        if pos == 'v':
            return 'hsk2'
        else:
            return 'hsk4'  # u

    if word == '地':
        if pos == 'u':
            return 'hsk3'
        else:
            return 'hsk3_减字'  # 天地

    if word == '过':
        if pos == 'u':
            return 'hsk2'
        else:
            return 'hsk3'  # v

    if word == '还':
        if pos == 'd':
            return 'hsk2'
        else:
            return 'hsk3'  # v

    if word == '喂':
        w1, p1 = posseg[loc + 1].split('/')
        if w1 in [',', '，', '？', '?', '……', '。'] or p1 == 'w':
            return 'hsk1'
        else:
            return 'hsk6'

    if word == '长':
        if pos == 'a':
            return 'hsk2'
        else:
            return 'hsk3'  # v

    if word == '只':
        if pos == 'q':
            return 'hsk2'
        else:
            return 'hsk3'  # d

    if word == '种':
        if pos == 'q':
            return 'hsk3'
        else:
            return 'hsk6_减字'  # v


def isWordChinese(word):
    for char in word:
        if char < '\u4e00' or char > '\u9fff':
            return False
    return True


def returnHSKlevel(word, pos, wplist, loc):
    if word in hsk_5000:
        return hsk_5000[word]
    elif word in hsk_ambiguous:
        return diambiguate_level(word, pos, wplist, loc)


def isJianzici(word):
    for l, words in hsk_all.items():
        for w in words:
            if word in w:
                return 'hsk' + str(l) + '_减字*'  # 默认'None'


def isChongzuci(word):
    char_levels = [0] * len(word)

    for i, c in enumerate(word):
        for l, charlist in chars.items():
            if c in charlist:
                char_levels[i] = l

    if min(char_levels) > 0:
        chongzu_level = max(char_levels)
        all_levels = [str(i) for i in char_levels]
        return 'hsk' + str(max(char_levels)) + '_重组*'


def level_analyze(sent, wordlist, wplist, current_level=0):
    level_dict = {k: 0 for k in range(1, 8)}

    for i, word in enumerate(wordlist):

        level = '默认_超纲'
        wp = wplist[i]
        if '//w' in wp:
            continue
        pos = wp.split('/')[1]

        if len(wordlist) == 1 and pos == 'nr':
            pos = 'n'

        if pos in ['w', 'nr', 'ns', 'Ng'] or not isWordChinese(word):
            continue

        if re.search('[a-zA-Z1-9]', word):
            word = re.sub('[a-zA-Z1-9]', '', word)

        if word in hsk_5000:
            level = hsk_5000[word]
        elif word in hsk_ambiguous:
            level = diambiguate_level(word, pos, wplist, i)
        elif word in jzcz:
            level = jzcz[word]

        if level == '默认_超纲':
            if len(word) < 3:
                t1 = isJianzici(word)
                if t1:
                    level = t1
                else:
                    t2 = isChongzuci(word)
                    if t2:
                        level = t2
            else:
                t2 = isChongzuci(word)
                if t2:
                    level = t2

        # word = word + '(' + level + ')' # for log
        if 'hsk' in level and '_' in level:
            word = word + '(' + level.split('_')[1] + ')'

        if level.startswith('hsk'):
            init_level = int(level[3])
            level_dict[init_level] += 1

        if '超纲' in level:
            level_dict[7] += 1

    return level_dict
