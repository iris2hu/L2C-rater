# L2C-rater (Automated Essay Scoring Method for Chinese Second Language Writing)

An automatic essay scoring method for Chinese L2 writing based on linear models, tree-structure models and logistic regression models, especially Ordinal Logistic Regression(OLR), combining 90 linguistic features and Tf-Idf textual representations.

### Enviroment
<h6>Python 3.6+<h6>

### Main Package
<h6>numpy 1.19.5</h6>
<h6>pandas 1.1.5</h6>
<h6>scipy 1.5.2</h6>
<h6>sci-kit-learn 0.24.1<h6>
<h6>pyltp 0.1.9.1</h6>
<h6>xgboost 1.3.3</h6>
<h6>mord 0.6</h6>

### Set Up ###

* Configure the environment
* Prepare data
* Run main.py

### Dataset ###

We conduct 5-fold cross validation on HSK Dynamic Composition Corpus to evaluate our system. This dataset (this code can be run with part of the data in [here](https://github.com/iris2hu/L2C-rater/tree/main/data)) is publicly available [here](http://hsk.blcu.edu.cn/).

### Options

You can see the list of available options by running:

```bash
python main.py -h
```

For ```feature_mode```, ```t``` means using **<em>text representation</em>** only when training the model, ```l``` means using **<em>linguistics features</em>** only, and ```b``` means using both the above features.

For ```feature_type```, ```c``` means segmenting the essay to **<em>character</em>** level when generating <em>text representation</em>, ```w``` means segmenting the essay to **<em>word</em>** level, ```cw``` means using both the above, ```wp``` means segmenting the essay to **<em>word</em>** level and tagging their **<em>part-of-speech(POS)</em>**, and ```cwp``` means using both ```c``` and ```wp```.

### Example ###

The following command  trains the best model among all automated models. Note that you will not get a convincing result with data provided [here](https://github.com/iris2hu/L2C-rater/tree/main/data), because the amount of data is not large enough.

```bash
python main.py -m b -t wp
```

### Publication ###

Wang Y., Hu R. (2021) A Prompt-Independent and Interpretable Automated Essay Scoring Method for Chinese Second Language Writing. In: Li S. et al. (eds) Chinese Computational Linguistics. CCL 2021. Lecture Notes in Computer Science, vol 12869. Springer, Cham. https://doi.org/10.1007/978-3-030-84186-7_30
