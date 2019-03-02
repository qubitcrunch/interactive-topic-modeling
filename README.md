# Interactive Topic Modeling

## The New York times dataset
The dataset contains articles from the New York Times World section spanning 10 years (2009 - 2018). The articles are in the `data/docs` directory. There is a `.jsonl` file for each year. Each line corresponds to an article and is a `.json` object that contains the following fields.

* date
* text
* author
* pageUrl


## Computing anchor words

### Installing the requirements
The repository contains code for anchor-based interactive topic modeling. The running environment is with python 2.7.x. You can install the requirements with 

```pip install -r requirements.txt```.

The following commands will generate anchor words using the implementation provided with this paper "A Practical Algorithm for Topic Modeling with Provable Guarantees". 

