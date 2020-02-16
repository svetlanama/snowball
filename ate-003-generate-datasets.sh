#!/bin/sh
# uncomment one of the lines below to invoke different strategies of dataset generation
# pipenv run python ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline/txt_clean --out_dataset_dir=ontology-1-baseline/datasets --strategy=time-asc    --increment_size=20
# pipenv run python ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline/txt_clean --out_dataset_dir=ontology-1-baseline/datasets --strategy=time-desc   --increment_size=20
# pipenv run python ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline/txt_clean --out_dataset_dir=ontology-1-baseline/datasets --strategy=random      --increment_size=20
# pipenv run python ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline/txt_clean --out_dataset_dir=ontology-1-baseline/datasets --strategy=time-bidir  --increment_size=20
# pipenv run python ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline/txt_clean --out_dataset_dir=ontology-1-baseline/datasets --strategy=citation-desc --increment_size=20 --citations=data/citations/ontology-1.xls

pipenv run python ate-003-generate-datasets.py --in_txt_dir=ontology-1/txt_clean --out_dataset_dir=ontology-1/datasets --strategy=citation-desc --increment_size=20 --citations=ontology-1/etc/ontology-1.xls
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=ontology-1/txt_clean --out_dataset_dir=ontology-1/datasets --strategy=citation-desc --increment_size=20 --citations=ontology-1/etc/ontology-1-ecc.xls
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=ontology-1/txt_clean --out_dataset_dir=ontology-1/datasets --strategy=citation-desc --increment_size=20 --citations=ontology-1/etc/ontology-1-spc.xls
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=ontology-1/txt_clean --out_dataset_dir=ontology-1/datasets --strategy=citation-desc --increment_size=20 --citations=ontology-1/etc/ontology-1-dist.xls
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline-acm/txt_clean --out_dataset_dir=ontology-1-baseline-acm/datasets --strategy=time-asc    --increment_size=20
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline-google-scholar/txt_clean --out_dataset_dir=ontology-1-baseline-google-scholar/datasets --strategy=time-asc    --increment_size=20
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=ontology-1-baseline-ms-academic/txt_clean --out_dataset_dir=ontology-1-baseline-ms-academic/datasets --strategy=time-asc    --increment_size=20
#pipenv run python  ate-003-generate-datasets.py --in_txt_dir=speechsegmentation/txt_clean --out_dataset_dir=speechsegmentation/datasets --strategy=citation-desc --increment_size=20 --citations=speechsegmentation/etc/ordering.xls
