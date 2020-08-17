# An Implementation of Stanford NER model and boost with multiprocessing

## Introduction of files:

* generate_input_list.py - code generating input text file for multiprocessing module in __multi_processing_get_df.py__.
* multi_processing_get_df.py - modified version for cloud version of preprocessing script which can run locally.
* temp.csv - a subset of dataframe from GKG dataset
* test.csv - a subset of orgnizations without business entities.

## Project description

The Project was aiming to preprocess the unstruectured data set from Google Big Query. The original dataset is more than 15 TB and here in this Github is just a small subset that provide for test. The original code was running in AWS EC2 using multiprocessing, the code in this Github is modified a little bit because I cannot provide mcuh information about the working dataset, the cloud version code is commanded in the script. My mission was to preprocess the organizations in filtered dataset(temp.csv) and only retain organizations that might be companies (because here organizations might be police department, university, council and etc.).

The Python script multi_processing_get_df.py requires [downloading](https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip) a well trained NLP model from [Stanford Named Entity Recognizer (NER)](https://nlp.stanford.edu/software/CRF-NER.html).

Because this script is running on AWS, and because of connection issue, I want each run with just a small part of each dataset, I wrote the python script generate_input_list.py. For example,  if a dataset contains 100 rows, I want to run through the first row to the last row, and each run just 20 rows, then the script will ask me some details of my requirement generate a text file. Then for the real preprocessing script, it will read text file I generated and loop through them. Therefore, we can minimized the cost of lost connection to AWS.

The cloud version code is running on AWS, using 96 cores machines, the process of the code depends on how many cores you have. Since the model from Stanford NER is a Java Based model, implementing it in Python might require some more time. As my test, each string in python takes around 1.2-1.6 seconds. While using multiprocessing library, the speed of preprocessing 100 rows was increased from 161 seconds to 7 seconds on AWS.

## Execution

* Generate the input list.

```
(base) FandeMacBook-Pro:gkg_preprocessing fanliang$ python generate_input_list.py
Enter the start number: 0
Enter the end number: 300
Enter how many you want to run each time: 20
Do you want to start from 0 and end at 300 and run 20 each time, type in [y/n]: y
```
* Run the preprocessing

```
(base) FandeMacBook-Pro:gkg_preprocessing fanliang$ python multi_processing_get_df.py test.csv input_list.txt
  7%|███▎                                             | 1/15 [00:29<06:56, 29.73s/it]
```
