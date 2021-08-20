import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


def stepwiseSelection(data, tag, 
                       initial_list=list(), 
                       threshold_in=0.05, 
                       threshold_out=0.10,
                       verbose=True):
    '''
    data: <Pandas.DataFrame> contaning indep/dep variables
    tag: <String> name of target
    initial_list: <List> independent variables that must be included
    threshold_in: <float> partial F-test threshold for entering a variable
    threshold_in: <float> partial F-test threshold for eliminating a variable
    verbose: <Boolean> show stepwise details of entering and eliminating
    >>> NOTE that {threshold_in < threshold_out} must be satisfied!
    '''

    ab_dic = dict()
    ab_mark = ['~', '+', '-', ':', '*', '/']
    for col in data.columns:
        for mark in ab_mark:
            if mark in col:
                ab_dic[col.replace(mark, '')] = col
                data.rename(columns={col: col.replace(mark, '')}, inplace=True)
    
    included = initial_list
    formula = f'{tag}~1'  # set a constant model as initial reduced_model
    best_r2_dif = .0

    while True:  # end loop when no variable gets in/out

        excluded = list(set(data.columns) - set(included))
        excluded.remove(tag)
        changed = False
        
        full_model = ols(formula=formula, data=data).fit()
        last_adj_r2 = full_model.rsquared_adj

        # forward step
        for new_feature in excluded:

            # Note here the test_model has more variable than full_model
            test_model = ols(formula=formula+f'+{new_feature}', data=data).fit()

            # find feature whose contribution to adj_r2 largest
            if test_model.rsquared_adj - last_adj_r2 > best_r2_dif:
                best_r2_dif = test_model.rsquared_adj - last_adj_r2
                last_adj_r2 = test_model.rsquared_adj
                best_feature = new_feature
        
        # Partial F-test
        # Note that in anova_lm models with few variables are put forward
        full_model_pro = ols(formula=formula+f'+{best_feature}', data=data).fit()
        anova_tbl = sm.stats.anova_lm(full_model, full_model_pro)
        criterion = anova_tbl['Pr(>F)'][1]

        if criterion <= threshold_in:
            included.append(best_feature)
            formula += f'+{best_feature}'
            full_model = full_model_pro
            changed = True
            best_r2_dif = .0
            if verbose:
                print('Add  {:25} with f_pvalue {:.6}'.format(best_feature, criterion))

        # backward step
        for old_feature in included:
            test_model = ols(formula=formula.replace(f'+{old_feature}', ''), data=data).fit()

            # Note here the test_model has less variable than full_model
            anova_tbl = sm.stats.anova_lm(test_model, full_model)
            criterion = anova_tbl['Pr(>F)'][1]
            if criterion >= threshold_out:
                included.remove(old_feature)
                formula = formula.replace(f'+{old_feature}', '')
                changed = True
                best_r2_dif = .0
                if verbose:
                    print('Drop {:25} with f_pvalue {:.6}'.format(old_feature, criterion))
        
        if not changed:
            break     

    return [ab_dic[x] if x in ab_dic.keys() else x for x in included]
