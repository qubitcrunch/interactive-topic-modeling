# Interactive Topic Modeling

## The New York times dataset
The dataset contains articles from the New York Times World section spanning 10 years (2009 - 2018). The articles are in the `data/docs` directory. There is a `.jsonl` file for each year. Each line corresponds to an article and is a `.json` object that contains the following fields.

* date
* text
* author
* pageUrl

### Processing
To process the data you will need R and some packages. 

```install R
 install package_1
 install package_2
 install package_3
```

The following will remove numbers, stops words, perform stemming, will extract the vocabulary and will convert the data in the sparse uci format that is needed to run the anchor word algorithm.

```Rscript json_to_uci.R nytimes data/docs data_uci```

Some other useful commands

```Rscript ```

```Rscript ```

## Computing anchor words

### Installing the requirements
Here we show how to compute anchor words that will then be used for interaction. The running environment is python 2.7.x. The requirements can be installed with `pip`.

```pip install -r requirements.txt```

```python uci_to_scipy.py data_uci/nytimes.txt <.mat>```

```python truncate_vocabulary.py", paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat"), paste0("../data_uci/vocab.",dtm_txt_file),trunc_thresh)```

```python learn_topics.py",paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat.trunc.mat"),"settings.example", paste0(" ../data_uci/vocab.",dtm_txt_file,".trunc"),num_topics,loss,"../py_code_output/result_")```



