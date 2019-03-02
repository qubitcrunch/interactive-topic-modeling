# Interactive Topic Modeling

## The New York times dataset
The dataset contains articles from the New York Times World section spanning 10 years (2009 - 2018). The articles are in the `data/docs` directory. There is a `.jsonl` file for each year. Each line corresponds to an article and is a `.json` object that contains the following fields.

* date
* text
* author
* pageUrl

### Installing R and packages
To process the data you will need R and some packages. To install R go here https://www.r-project.org. After R is installed run and you can successfully start it from a terminal run

```R -e 'install.packages(c("RJSONIO","tm","stringr"),repos="http://cran.us.r-project.org")'
```

to install the required packages. 

### Processing data
The following will remove numbers, stops words, perform stemming, extract the vocabulary and convert the data in the sparse uci format in `data_uci`.

```
mkdir data_uci
Rscript json_to_uci.R nytimes data/docs data_uci
```

### Other useful commands

```Rscript ```

```Rscript ```

## Computing anchor words

### Installing the requirements
To compute anchor words you will need python 2.7.x. The requirements can be installed with `pip`.

```pip install -r requirements.txt```

The following will output the anchor words, the anchor word matrix and optionally, the recovered topic vectors in the `output` directory. 

```
mkdir output
python main_anchor_words.py --threshold=10 --num_topics=500 --recovery=True
```


