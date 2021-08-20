'''
    collcation features
'''

notHV = ['的', '吗', '吧', '呢', '啊', '呀', '之', '等']
prepositions = ['把', '被', '对', '给', '跟', '将', '为', '向', '由', '与', '和', '同']


def getColl(words):
    collocation = []
    for key, value in words.items():
        parent_id = int(value['parent'])
        if parent_id == -1:
            continue
        parent_cont = words[parent_id]['cont']

        if value['pos'] in ['wp', 'ws'] or words[parent_id]['pos'] in ['wp', 'ws']:
            continue

        # P_X_DN
        if value['relate'] == 'POB' and value['pos'] == 'nd':
            if key > parent_id + 1 and words[parent_id]['pos'] == 'p' and parent_cont in ['在', '到', '从', '自', '自从', '向',
                                                                                          '往', '除了', '于', '沿着', '至',
                                                                                          '由', '顺着', '朝', '朝着', '沿',
                                                                                          '向着']:
                coll_p_dn = parent_cont + '\t' + 'X' + '\t' + value['cont'] + '\t' + 'P_X_DN'
                collocation.append(coll_p_dn)
        if value['relate'] == 'POB' and value['cont'] in ['时', '时候']:
            if key > parent_id + 1 and words[parent_id]['pos'] == 'p' and parent_cont in ['在', '当', '每当', '从', '自从',
                                                                                          '自', '到']:
                coll_p_dn = parent_cont + '\t' + 'X' + '\t' + value['cont'] + '\t' + 'P_X_DN'
                collocation.append(coll_p_dn)

        # P_X_U
        if value['relate'] == 'RAD' and value['pos'] == 'u' and value['cont'] not in notHV:
            if key > parent_id + 1 and words[parent_id]['pos'] == 'p':
                coll_p_u = parent_cont + '\t' + 'X' + '\t' + value['cont'] + '\t' + 'P_X_U'
                collocation.append(coll_p_u)

        # CN
        if value['relate'] == 'ATT' and value['pos'] == 'q':
            if words[parent_id]['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
                coll_q_n = value['cont'] + '\t' + parent_cont + '\t' + 'Q_N'
                collocation.append(coll_q_n)
        # AN
        if value['relate'] == 'ATT' and value['pos'] == 'a':
            if words[parent_id]['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
                if key == parent_id - 1:
                    coll_a_n = value['cont'] + '\t' + parent_cont + '\t' + 'A_N'
                    collocation.append(coll_a_n)
                elif key == parent_id - 2 and words[parent_id - 1]['cont'] == '的':
                    coll_a_de_n = value['cont'] + '\t' + '的' + '\t' + parent_cont + '\t' + 'A_DE_N'
                    collocation.append(coll_a_de_n)
                elif words[key + 1]['cont'] == '的':
                    coll_a_de_x_n = value['cont'] + '\t' + '的' + '\t' + 'X' + '\t' + parent_cont + '\t' + 'A_DE_X_N'
                    collocation.append(coll_a_de_x_n)
                elif words[parent_id - 1]['cont'] == '的':
                    coll_a_x_de_n = value['cont'] + '\t' + 'X' + '\t' + '的' + '\t' + parent_cont + '\t' + 'A_X_DE_N'
                    collocation.append(coll_a_x_de_n)
                else:
                    coll_a_x_n = value['cont'] + '\t' + 'X' + '\t' + parent_cont + '\t' + 'A_X_N'
                    collocation.append(coll_a_x_n)

        # VO
        if value['relate'] in ['VOB', 'FOB', 'IOB'] and value['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
            if words.__contains__(parent_id + 1) and words[parent_id + 1]['relate'] in ['RAD', 'CMP'] and \
                    words[parent_id + 1]['cont'] not in notHV:
                if words.__contains__(parent_id + 2) and words[parent_id + 2]['relate'] in ['RAD', 'CMP'] and \
                        words[parent_id + 2]['cont'] not in notHV:
                    coll_v_2hv_o = parent_cont + '\t' + words[parent_id + 1]['cont'] + '\t' + words[parent_id + 2][
                        'cont'] + '\t' + value['cont'] + '\t' + 'V_2HV_O'
                    collocation.append(coll_v_2hv_o)
                else:
                    coll_v_hv_o = parent_cont + '\t' + words[parent_id + 1]['cont'] + '\t' + value[
                        'cont'] + '\t' + 'V_HV_O'
                    collocation.append(coll_v_hv_o)
            else:
                coll_v_o = parent_cont + '\t' + value['cont'] + '\t' + 'V_O'
                collocation.append(coll_v_o)

        # SP
        if value['relate'] == 'SBV' and value['pos'] not in ['r', 'nh', 'nl']:
            if words.__contains__(parent_id + 1) and words[parent_id + 1]['relate'] in ['RAD', 'CMP'] and \
                    words[parent_id + 1]['cont'] not in notHV:
                if words.__contains__(parent_id + 2) and words[parent_id + 2]['relate'] in ['RAD', 'CMP'] and \
                        words[parent_id + 2]['cont'] not in notHV:
                    coll_s_v_2hv = value['cont'] + '\t' + parent_cont + '\t' + words[parent_id + 1]['cont'] + '\t' + \
                                   words[parent_id + 2]['cont'] + '\t' + 'S_V_2HV'
                    collocation.append(coll_s_v_2hv)
                else:
                    coll_s_v_hv = value['cont'] + '\t' + parent_cont + '\t' + words[parent_id + 1][
                        'cont'] + '\t' + 'S_V_HV'
                    collocation.append(coll_s_v_hv)
            elif words[parent_id - 1]['cont'] not in [':', '：']:
                coll_s_v = value['cont'] + '\t' + parent_cont + '\t' + 'S_V'
                collocation.append(coll_s_v)

        # AP
        if value['relate'] == 'ADV' and value['pos'] in ['a', 'd', 'v']:
            if key == parent_id - 1:
                if words[parent_id]['pos'] == 'a':
                    coll_d_a = value['cont'] + '\t' + parent_cont + '\t' + 'D_A'
                    collocation.append(coll_d_a)
                elif words[parent_id]['pos'] == 'v':
                    coll_d_v = value['cont'] + '\t' + parent_cont + '\t' + 'D_V'
                    collocation.append(coll_d_v)
            elif key < parent_id and words[key + 1]['cont'] == '地':
                coll_d_di_v = value['cont'] + '\t' + '地' + '\t' + parent_cont + '\t' + 'D_DI_V'
                collocation.append(coll_d_di_v)
            elif key < parent_id:
                if words[parent_id]['pos'] == 'a':
                    coll_d_x_a = value['cont'] + '\t' + 'X' + '\t' + parent_cont + '\t' + 'D_X_A'
                    collocation.append(coll_d_x_a)
                elif words[parent_id]['pos'] == 'v':
                    coll_d_x_v = value['cont'] + '\t' + 'X' + '\t' + parent_cont + '\t' + 'D_X_V'
                    collocation.append(coll_d_x_v)

        # PV
        if value['pos'] == 'p' and value['cont'] in prepositions:
            if value['relate'] == 'ADV' and words[parent_id]['pos'] == 'v' and key < parent_id:
                if words.__contains__(parent_id + 1) and words.__contains__(parent_id + 2) and words[parent_id + 1][
                    'relate'] in ['RAD', 'CMP'] and words[parent_id + 1]['cont'] not in notHV and words[parent_id + 2][
                    'relate'] in ['RAD', 'CMP'] and words[parent_id + 2]['cont'] not in notHV:
                    coll_p_v_2hv = value['cont'] + '\t' + 'X' + '\t' + parent_cont + '\t' + words[parent_id + 1][
                        'cont'] + '\t' + words[parent_id + 2]['cont'] + '\t' + 'P_X_V_2HV'
                    collocation.append(coll_p_v_2hv)
                elif words.__contains__(parent_id + 1) and words[parent_id + 1]['relate'] in ['RAD', 'CMP'] and \
                        words[parent_id + 1]['cont'] not in notHV:
                    coll_p_v_hv = value['cont'] + '\t' + 'X' + '\t' + parent_cont + '\t' + words[parent_id + 1][
                        'cont'] + '\t' + 'P_X_V_HV'
                    collocation.append(coll_p_v_hv)
                else:
                    coll_p_v = value['cont'] + '\t' + 'X' + '\t' + parent_cont + '\t' + 'P_X_V'
                    collocation.append(coll_p_v)
        # PC
        if value['relate'] == 'CMP':
            if key == parent_id + 1:
                if words.__contains__(key + 1):
                    if words[key + 1]['cont'] in ['了', '得', '过']:
                        coll_v_c_u = parent_cont + '\t' + value['cont'] + '\t' + words[key + 1]['cont'] + '\t' + 'V_C_U'
                        collocation.append(coll_v_c_u)
                    else:
                        coll_v_c = parent_cont + '\t' + value['cont'] + '\t' + 'V_C'
                        collocation.append(coll_v_c)
            elif key == parent_id + 2:
                if words[key - 1]['cont'] in ['了', '得', '过']:
                    coll_v_u_c = parent_cont + '\t' + words[key - 1]['cont'] + '\t' + value['cont'] + '\t' + 'V_U_C'
                    collocation.append(coll_v_u_c)
                elif words[key - 1]['relate'] == 'ADV':
                    coll_v_d_c = parent_cont + '\t' + words[key - 1]['cont'] + '\t' + value['cont'] + '\t' + 'V_D_C'
                    collocation.append(coll_v_d_c)
                elif words[key - 1]['relate'] == 'ATT':
                    if words[key - 1]['pos'] == 'm':
                        coll_v_m_c = parent_cont + '\t' + 'm' + '\t' + value['cont'] + '\t' + 'V_M_C'
                        collocation.append(coll_v_m_c)
                    else:
                        coll_v_a_c = parent_cont + '\t' + 'A' + '\t' + value['cont'] + '\t' + 'V_A_C'
                        collocation.append(coll_v_a_c)
            elif key > parent_id + 2:
                if words[parent_id + 1]['cont'] in ['了', '得', '过']:
                    if key == parent_id + 3:
                        if words[key - 1]['relate'] == 'ATT':
                            if words[key - 1]['pos'] == 'm':
                                coll_v_u_m_c = parent_cont + '\t' + words[key - 2]['cont'] + '\t' + 'm' + '\t' + value[
                                    'cont'] + '\t' + 'V_U_M_C'
                                collocation.append(coll_v_u_m_c)
                            else:
                                coll_v_u_a_c = parent_cont + '\t' + words[key - 2]['cont'] + '\t' + words[key - 1][
                                    'cont'] + '\t' + value['cont'] + '\t' + 'V_U_A_C'
                                collocation.append(coll_v_u_a_c)
                        elif words[key - 1]['relate'] == 'ADV':
                            if value['pos'] != 'v':
                                coll_v_u_d_c = parent_cont + '\t' + words[key - 2]['cont'] + '\t' + words[key - 1][
                                    'cont'] + '\t' + value['cont'] + '\t' + 'V_U_D_C'
                                collocation.append(coll_v_u_d_c)
                            elif words[key + 1]['pos'] == 'wp':
                                coll_v_u_d_c = parent_cont + '\t' + words[key - 2]['cont'] + '\t' + words[key - 1][
                                    'cont'] + '\t' + value['cont'] + '\t' + 'V_U_D_C'
                                collocation.append(coll_v_u_d_c)
                        else:
                            coll_v_u_x_c = parent_cont + '\t' + words[key - 2]['cont'] + '\t' + 'X' + '\t' + value[
                                'cont'] + '\t' + 'V_U_X_C'
                            collocation.append(coll_v_u_x_c)
                    else:
                        coll_v_u_x_c = parent_cont + '\t' + words[parent_id + 1]['cont'] + '\t' + 'X' + '\t' + value[
                            'cont'] + '\t' + 'V_U_X_C'
                        collocation.append(coll_v_u_x_c)
                else:
                    coll_v_x_c = parent_cont + '\t' + 'X' + '\t' + value['cont'] + '\t' + 'V_X_C'
                    collocation.append(coll_v_x_c)

    return collocation


coll_dict = {"V_O": "VO", "V_HV_O": "VO", "V_2HV_O": "VO", "D_V": "AP",
             "S_V_HV": "SP", "P_X_DN": "PP*", "V_C": "PC*",
             "S_V": "SP", "D_A": "AP", "Q_N": "CN*", "V_D_C": "PC*", "P_X_U": "PP*",
             "P_X_V": "PV*", "A_N": "AN", "A_X_DE_N": "AN", "D_X_A": "AP", "P_X_V_HV": "PV*",
             "D_X_V": "AP", "V_U_C": "PC*", "A_DE_N": "AN", "V_X_C": "PC*",
             "V_C_U": "PC*", "D_DI_V": "AP", "V_U_X_C": "PC*", "V_M_C": "PC*", "V_U_A_C": "PC*",
             "A_X_N": "AN", "V_U_D_C": "PC*", "V_U_M_C": "PC*", "A_DE_X_N": "AN",
             "P_X_V_2HV": "PV*", "S_V_2HV": "SP", "V_A_C": "PC*"}


def isUniqueColl(coll):
    typ = coll_dict[coll.split('\t')[-1]]
    if typ in ['PC*', 'PV*', 'CN*', 'PP*']:
        return True
    else:
        return False


lowfreq_colls = {line.strip(): 0 for line in open('./dict/low_freq_coll.txt', encoding='utf-8')}


def isLowFreqColl(coll):
    if coll in lowfreq_colls:
        return True
    return False
