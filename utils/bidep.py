'''
bigram and dep trigram features
'''


def get_bigrams(wplist):
    bigrams = []
    for i, wp in enumerate(wplist):
        if i < len(wplist) - 1:
            wpl = wp.split('/')
            if len(wpl) != 2:
                continue
            word, pos = wpl[0], wpl[1]
            if pos != 'wp':
                wp_next = wplist[i + 1]
                if 'wp' not in wp_next:
                    bi = word + '_' + wp_next.split('/')[0]
                    bigrams.append(bi)
    return bigrams


def get_dep_trigrams(worddict, trigrams, depdist):
    '''
    trigrams: type <dict> 
    depdist: type <dict>
    '''
    for k, v in worddict.items():
        word = v['cont']
        relation = v['relate']
        if relation == 'WP':
            continue
        parent_id = v['parent']
        if parent_id == -1:
            parent = 'ROOT'
        else:
            parent = worddict[parent_id]['cont']
            distance = abs(parent_id - k)
            if relation in depdist:
                depdist[relation].append(distance)
            else:
                depdist[relation] = [distance]

        tri = word + '_' + relation + '_' + parent
        if relation in trigrams:
            trigrams[relation].append(tri)
        else:
            trigrams[relation] = [tri]

    return trigrams, depdist


bigram_freq = {line.strip().split('\t')[0]: int(line.strip().split('\t')[1]) for line in 
            open('./dict/bigram_freq.txt', encoding='utf-8')}
dep_freq = {line.strip().split('\t')[0]: int(line.strip().split('\t')[1]) for line in
            open('./dict/dep_trigram_freq.txt', encoding='utf-8')}


def is_sophis_bigram(bigram, freq_threshold=10):
    if bigram in bigram_freq and bigram_freq[bigram] < freq_threshold:
        return True
    return False


def is_sophis_trigram(trigram, freq_threshold=10):
    if trigram in dep_freq and dep_freq[trigram] < freq_threshold:
        return True
    return False
