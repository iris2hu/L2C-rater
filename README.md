# Automated Essay Scoring Method for Chinese Second Language Writing

An automatic essay scoring method for Chinese L2 writing based on linear models, tree-structure models and logistic regression models, especially Ordinal Logistic Regression(OLR), combining 90 linguistic features and Tf-Idf textual representations.

An online demo of L2C-rater can be seen at [https://l2c.shenshen.wiki/](https://l2c.shenshen.wiki/).

### Enviroment
* Python 3.6+

### Packages
* numpy 1.19.5
* pandas 1.1.5
* scipy 1.5.2
* sci-kit-learn 0.24.1
* pyltp 0.1.9.1
* xgboost 1.3.3
* mord 0.6

### Set Up ###

* Configure the environment
* Prepare the data
* Run main.py

### Dataset ###

We conduct 5-fold cross validation on [HSK Dynamic Composition Corpus 2.0](http://hsk.blcu.edu.cn/) to evaluate our system. Currently, the code can be run with the provided [samples](https://github.com/iris2hu/L2C-rater/tree/main/data).

### Options

You can see the list of available options by running:

```bash
python main.py -h
```

For ```feature_mode```, ```t``` means using **<em>text representations</em>** only when training the model, ```l``` means using **<em>linguistics features</em>** only, and ```b``` means using both the above features.

For ```feature_type```, ```c``` means using **<em>character</em>** level features when generating <em>text representations</em>, ```w``` means the **<em>word</em>** level, ```cw``` means using both ```c``` and ```w```, ```wp``` means using **<em>word</em>** and **<em>part-of-speech(POS)</em>** features, and ```cwp``` means using both ```c``` and ```wp```.

### Example ###

The following command  trains the best model among all models. Note that you will not get a convincing result with only the [samples](https://github.com/iris2hu/L2C-rater/tree/main/data).

```bash
python main.py -m b -t wp
```

### Publication ###

Please cite our work when using the codes:

Wang Y., Hu R. (2021) A Prompt-Independent and Interpretable Automated Essay Scoring Method for Chinese Second Language Writing. In: Li S. et al. (eds) Chinese Computational Linguistics. CCL 2021. Lecture Notes in Computer Science, vol 12869. Springer, Cham. https://doi.org/10.1007/978-3-030-84186-7_30

```
@inproceedings{wang2021prompt,
  title={A Prompt-Independent and Interpretable Automated Essay Scoring Method for Chinese Second Language Writing},
  author={Wang, Yupei and Hu, Renfen},
  booktitle={China National Conference on Chinese Computational Linguistics},
  pages={450--470},
  year={2021},
  organization={Springer}
}
```

More modules of L2C-rater coming soon!
