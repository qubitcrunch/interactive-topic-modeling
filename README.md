# Interactive Topic Modeling
This repository contains the code for anchor word-based interactive topic modeling. Here we lay out the steps for running anchor words on the New York Times dataset.

## The New York times dataset
The dataset contains articles from the New York Times World section spanning 10 years (2009 - 2018). The articles are in the `data/docs` directory. There is a `.jsonl` file for each year. Each line corresponds to an article and is a `.json` object that contains the following fields.

* date
* text
* author
* pageUrl

### Installing R and packages
To process the data you will need R and some packages. To install R go here https://www.r-project.org. After R is installed make sure that you can successfully start it from a terminal and then run

```
R -e 'install.packages(c("RJSONIO","tm","stringr"),repos="http://cran.us.r-project.org")'
```

to install the required packages. 

### Processing data
The following will remove numbers, stops words, perform stemming, extract the vocabulary and convert the data in the sparse uci format. The output will be saved in a directory e.g. `data_uci`.

```
mkdir data_uci
Rscript json_to_uci.R nytimes data/docs data_uci
```

## Computing anchor words

### Installing the requirements
To compute anchor words you will need python 2.7.x. The requirements can be installed with `pip`.

```pip install -r requirements.txt```

The following 

```
python main_anchor_words.py -h
```
will show the different arguments.


Running   

```
mkdir output
python main_anchor_words.py --settings_file=settings --uci_file=data_uci/nytimes.txt --full_vocab_file=data_uci/vocab.nytimes.txt --cut_off=10 --stopwords_file=stopwords.txt --num_anchors=500 --recovery=False --out_file=output/output --save_trunc=True
```

will output 
* the anchor words (`output.anchors`)
* the anchor word matrix (`output.Q_anchors`)
* the truncated document-term (`output.M.trunc.mat`) and vocabulary (`output.vocab.trunc`)

in the `output` directory.

