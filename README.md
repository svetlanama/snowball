# snowball
Application of controlled/restricted snowball sampling to collection of the scientific publications


Quick start:
0) you need NLTK and numpy to run the scripts below.
1) get MS Academic API key ( https://azure.microsoft.com/en-us/services/cognitive-services/academic-knowledge/ )
2) copy config-sample.ini to config.ini and update config.ini
3) set desired MS Academic topics in the file data/in-include-topics.txt
4) set undesired MS Academic topics in the file data/in-exclude-topics.txt
5) paste MS Academic Ids into data/in-seed.csv , one ID per row
6) run sequentially the following files
* 000_download.py
* 001_tokenizer.py
* 002_rarewords.py
* 003_joint_probabilities.py
* 004_stopwords.py
* 005_reduced_joint_probabilities.py
* 007_SSNMF.py
* 008_show_topic_coherence.py
* 009_restricted_snowball.py
* 010_search_path_count.py
