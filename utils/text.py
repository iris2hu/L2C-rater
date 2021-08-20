import os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser


def load_ltpmodel(model_path):
    cws_model_path = os.path.join(model_path, 'cws.model')  # word segmentation model
    pos_model_path = os.path.join(model_path, 'pos.model')  # pos tagging model
    par_model_path = os.path.join(model_path, 'parser.model')  # parsing model

    segmentor = Segmentor()
    segmentor.load(cws_model_path)
    postagger = Postagger()
    postagger.load(pos_model_path)
    parser = Parser()
    parser.load(par_model_path)
    return segmentor, postagger, parser


def release_ltpmodel(segmentor, postagger, parser):
    segmentor.release()
    postagger.release()
    parser.release()


def parse(sent, segmentor, postagger, parser, withWordPOS=False):
    ''' 
        word segment
        pos tagging
        dependency parsing
        return: word_dict type: dict
    '''
    d = {}
    wordlist = segmentor.segment(sent)
    postags = postagger.postag(wordlist)

    arcs = parser.parse(wordlist, postags)
    for i, arc in enumerate(arcs):
        token, pos = wordlist[i], postags[i]
        parent = arc.head - 1  # 原为从1开始编号，现从0开始编号
        relate = arc.relation
        d[i] = {'cont': token, 'pos': pos, 'parent': parent, 'relate': relate}

    if withWordPOS:
        wplist = []
        for w, p in zip(wordlist, postags):
            wplist.append(w + '/' + p)
        wordlist = [w for w in wordlist]
        return wordlist, wplist, d

    return d


def text_process(text, segmentor, postagger, parser):
    sent_id, text_dict = 0, {}

    # sentence split
    paras = text.split('\n')
    # print('loaded %s text paragraphs' % len(paras))

    # para split
    for para in paras:
        para = para.strip()
        if len(para) < 3:
            continue
        sents = SentenceSplitter.split(para)
        for sent in sents:
            if len(sent) < 3:
                continue

            sent_id += 1

            wordlist, wplist, worddict = parse(sent, segmentor, postagger, parser, withWordPOS=True)
            text_dict[sent_id] = {'wordlist': wordlist, 'wplist': wplist, 'worddict': worddict, 'sent': sent}

    return text_dict
