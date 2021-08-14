import csv
import glob
import os.path
import string

import numpy as np
import codecs

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

train_folder = "datasets-v2/datasets/train-articles"
dev_folder = "datasets-v2/datasets/dev-articles"
test_folder="datasets-v2/datasets/test-articles"
train_labels="datasets-v2/datasets/train-task2-TC.labels"
dev_labels="datasets-v2/datasets/dev-task-TC.labels"
test_labels="datasets-v2/datasets/test-task-TC-template.out"

def read_file_content(article_id, mode):
    file_content = []
    if mode == 'train':
        file_name = train_folder + "/article" + article_id + '.txt'
    else:
        if mode=='dev':
            file_name = dev_folder + "/article" + article_id + '.txt'
        else:
            file_name = test_folder + "/article" + article_id + '.txt'

    with open(file_name, "r", encoding="utf-8") as f:
        file_content.append(f.read())

    return file_content


def read_predictions(folder_name,mode,file_pattern='*.tsv'):
     file_list = glob.glob(os.path.join(folder_name, file_pattern))
     print(len(file_list))
     print(file_list)
     articles_id,spans, span_starts, span_ends, gold_labels,articles = ([],[], [], [], [],[])
     for filename in sorted(file_list):
        with open(filename, "r", encoding="utf-8") as f:
            for row in f.readlines():
                article_id, gold_label, span_start, span_end = row.rstrip().split("\t")
                articles_id.append(article_id)
                gold_labels.append(gold_label)
                span_starts.append(span_start)
                span_ends.append(span_end)
                content = read_file_content(article_id, mode)
                content = ' '.join(content)
                articles.append(content)
                start = int(span_start)
                end = int(span_end)
                spans.append(content[start:end])

     return articles_id,spans, span_starts, span_ends, gold_labels,articles


def read_predictions_from_file(file_name, mode):

    articles_id, spans, span_starts, span_ends, gold_labels,article = ([], [], [], [], [],[])

    with open(file_name, "r", encoding="utf-8") as f:
        for row in f.readlines():
                article_id, gold_label, span_start, span_end = row.rstrip().split("\t")
                articles_id.append(article_id)
                gold_labels.append(gold_label)
                span_starts.append(span_start)
                span_ends.append(span_end)
                content = read_file_content(article_id, mode)
                article.append(content)
                content = ' '.join(content)
                start = int(span_start)
                end = int(span_end)
                spans.append(content[start:end])

    return articles_id, article,spans, span_starts, span_ends, gold_labels

if __name__ == '__main__':

    ref_articles_id,train_art, spans, ref_span_starts, ref_span_ends, train_gold_labels=read_predictions_from_file(train_labels,'train')
    dev_article_ids, dev_art,dev_spans, dev_span_starts, dev_span_ends, dev_labels = read_predictions_from_file(dev_labels,'dev')
    test_article_ids,test_art, test_spans, test_span_starts, test_span_ends, test_labels = read_predictions_from_file(test_labels,'test')
    #ref_articles_id, spans, ref_span_starts, ref_span_ends, train_gold_labels = read_predictions(train_folder, 'train')
    #dev_article_ids, dev_spans, dev_span_starts, dev_span_ends, dev_labels = read_predictions(dev_folder, 'dev')
    #test_article_ids, test_spans,test_span_starts, test_span_ends, test_labels = read_predictions(test_folder, 'test')

    print("Loaded %d train annotations from %d articles" % (len(ref_span_starts), len(set(ref_articles_id))))
    print("Loaded %d dev annotations from %d articles" % (len(dev_span_starts), len(set(dev_article_ids))))
    print("Loaded %d test annotations from %d articles" % (len(test_span_starts), len(set(test_article_ids))))


    # write train data to csv file
    File = open('Train-Propaganda-context.csv', 'w', encoding="utf-8", newline='')
    with File:
        writer = csv.writer(File)
        writer.writerow(["id",'Article', "span", "label", "start", "end"])
        for i in range(len(ref_articles_id)):
            writer.writerow([str(ref_articles_id[i]), str(train_art[i]),str(spans[i]), str(train_gold_labels[i]), str(ref_span_starts[i]),
                             str(ref_span_ends[i])])

    # write dev data to csv file
    File = open('Dev-propaganda-context.csv', 'w', encoding="utf-8", newline='')
    with File:
        writer = csv.writer(File)
        writer.writerow(["id",'Article', "span", "start", "end", 'label'])
        for i in range(len(dev_article_ids)):
            writer.writerow([str(dev_article_ids[i]),str(dev_art[i]), str(dev_spans[i]), str(dev_span_starts[i]), str(dev_span_ends[i]),
                             str(dev_labels[i])])

    #write test data to csv file
    File = open('Test-propaganda-context.csv', 'w', encoding="utf-8", newline='')
    with File:
        writer = csv.writer(File)
        writer.writerow(["id",'Article', "span",'label'])
        for i in range(len(test_article_ids)):
            writer.writerow([str(test_article_ids[i]), str(test_art[i]),str(test_spans[i]),str(test_labels[i])])
