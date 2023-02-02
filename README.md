

# Validators selection

Implementation of UTA approach for validators selection based on nominator's preferences.


# Endpoints

Specification of exposed endpoints

## New file
Accepts new file with validators description, should be called at the start of each era.

Endpoint: \fileupload
Method: POST
Parameters:
 - validators - a csv file containing validators that might be recommended to a nominator
 - depth - an integer denoting number of questions to compute in advance (default 7)

Output:
 - 200 "DONE" if properly calculated
 - 400 "Validators file not provided" if there isn't a parameter called validators
 - 400 "Invalid file structure, expected 7 columns, got x" if structure of the file is not matching the expected structure

## Next pair
Search for an optimal question to maximize model's information gain and therefore provide recommendations matching nominator's preferences better.

Endpoint: \next
Method: POST
Parameters:
 - history - collection containing previous answers

Output:
 - ValidatorA:
   - values -  description of the first validator
   - history - history to be provided in the next query if this validator is selected
 - ValidatorB:
   - values -  description of the second validator
   - history - history to be provided in the next query if this validator is selected
- quality - current model quality. It's a value from -1 to 1
- model - definition of current model

## Ranking
Provides a ranking of validators for a provided model and a previously provided file with validators

Endopint: \ranking
Method: POST
Parameters:
 - model - model from "\next" function for which the ranking should be calculated 

Output:
 - 400, "Model not provided" if model parameter is missing
 - 400, "col not present in the model" if model structure is not correct
 - 200, coma separated string with two columns: validator, score

# Tests

## Environment
 - python 3.8 installed
 - pip3 install -r requirements.txt
 - pip3 install requests (to run integration test) 
## Execution
To run unit tests execute ```python -m unittest discover``` in the main directory, not in the /test.
When docker is running:
 - docker build -t "validators_selection:Dockerfile" .
 - docker run -p 14237:14237 validators_selection:Dockerfile

 additional test can be executed from the test directory ```python integration_test.py```
# Example
Call:
```
curl -X POST -F 'validators=@validators.csv' -F 'depth=2' localhost:14237/fileupload
```
Response:
```
DONE
```

Call:
```
curl -X POST http://localhost:14237/next -H 'Content-Type: application/json' -d '{"history": []}'
```
Response:
```json
{"model":[],"quality":-1,"validatorA":{"history":[[[2.0,3.0,2166958.6,780.0,8.0,998.0],[3.0,5349.8,2160212.4,960.0,1.0,385.0]]],"values":{"Cluster Size":8.0,"Commission (in %)":2.0,"Era Points":780.0,"Self Stake (in DOT)":3.0,"Total Stake (in DOT)":2166958.6,"Voters":998.0}},"validatorB":{"history":[[[3.0,5349.8,2160212.4,960.0,1.0,385.0],[2.0,3.0,2166958.6,780.0,8.0,998.0]]],"values":{"Cluster Size":1.0,"Commission (in %)":3.0,"Era Points":960.0,"Self Stake (in DOT)":5349.8,"Total Stake (in DOT)":2160212.4,"Voters":385.0}}}
```

Call:
```
curl -X POST http://localhost:14237/next -H 'Content-Type: application/json' -d '{"history": [[[2.0,3.0,2166958.6,780.0,8.0,998.0],[3.0,5349.8,2160212.4,960.0,1.0,385.0]]]}'
```
Response:
```json
{"model":{"Cluster Size":[[1.0,5.0,9.0,13.0],[0.0,0.05110380798578262,0.08571542054414749,0.07616810500621796]],"Commission (in %)":[[0.5,1.0,4.0,7.0,10.0],[0.24016796052455902,0.17940208315849304,0.11632449924945831,0.06259024143218994,0.0]],"Era Points":[[780.0,926.6666666666666,1073.3333333333333,1220.0],[0.0,0.046321600675582886,0.1112983375787735,0.1862511932849884]],"Self Stake (in DOT)":[[1.0,201480.7333333333,402960.4666666666,604440.2],[0.0,0.07729128003120422,0.14550165832042694,0.2152264565229416]],"Total Stake (in DOT)":[[1942391.7,2728076.2666666666,3513760.8333333335,4299445.4],[0.21496045589447021,0.13687363266944885,0.07219888269901276,0.0]],"Voters":[[279.0,1042.3333333333335,1805.6666666666667,2569.0],[0.0,0.057678502053022385,0.047051720321178436,0.043068237602710724]]},"quality":-0.06813186813186813,"validatorA":{"history":[[[1.0,10883.1,2168765.7,880.0,2.0,850.0],[1.0,570807.4,3405665.4,820.0,3.0,2569.0]],[[2.0,3.0,2166958.6,780.0,8.0,998.0],[3.0,5349.8,2160212.4,960.0,1.0,385.0]]],"values":{"Cluster Size":2.0,"Commission (in %)":1.0,"Era Points":880.0,"Self Stake (in DOT)":10883.1,"Total Stake (in DOT)":2168765.7,"Voters":850.0}},"validatorB":{"history":[[[1.0,570807.4,3405665.4,820.0,3.0,2569.0],[1.0,10883.1,2168765.7,880.0,2.0,850.0]],[[2.0,3.0,2166958.6,780.0,8.0,998.0],[3.0,5349.8,2160212.4,960.0,1.0,385.0]]],"values":{"Cluster Size":3.0,"Commission (in %)":1.0,"Era Points":820.0,"Self Stake (in DOT)":570807.4,"Total Stake (in DOT)":3405665.4,"Voters":2569.0}}}
```

Call:
```
curl -X POST http://localhost:14237/ranking -H 'Content-Type: application/json' -d '{"model":{"Cluster Size":[[1.0,5.0,9.0,13.0],[0.0,0.05110380798578262,0.08571542054414749,0.07616810500621796]],"Commission (in %)":[[0.5,1.0,4.0,7.0,10.0],[0.24016796052455902,0.17940208315849304,0.11632449924945831,0.06259024143218994,0.0]],"Era Points":[[780.0,926.6666666666666,1073.3333333333333,1220.0],[0.0,0.046321600675582886,0.1112983375787735,0.1862511932849884]],"Self Stake (in DOT)":[[1.0,201480.7333333333,402960.4666666666,604440.2],[0.0,0.07729128003120422,0.14550165832042694,0.2152264565229416]],"Total Stake (in DOT)":[[1942391.7,2728076.2666666666,3513760.8333333335,4299445.4],[0.21496045589447021,0.13687363266944885,0.07219888269901276,0.0]],"Voters":[[279.0,1042.3333333333335,1805.6666666666667,2569.0],[0.0,0.057678502053022385,0.047051720321178436,0.043068237602710724]]}}'
```
Response:
```
stash_address,score
11BgR7fH8Sq6CcGcXxZrhyrBM2PUpDmhnGZpxPGvVGXEiPT,0.23764662487783952
11MJU5Q1rQh5BKuuECePhSAutv3WEVx6f2x9eZk9HXkCC1e,0.4846110339586901
11uMPbeaEDJhUxzU4ZfWW9VQEsryP9XqFcNRfPdYda6aFWJ,0.4850486249474511
14Vh8S1DzzycngbAB9vqEgPFR9JpSvmF1ezihTUES1EaHAV,0.46354287583757453
1A2ATy1FEu5yQ9ZzghPLsRckPQ7XLmq5MJQYcTvGnxGvCho,0.31873883660579544
1ChRPtPxrTfFTSWyKHtF6ASvaSjL5jqz6f68ih15zcjyM1V,0.4018127143292364
1LMtHkfrADk7awSEFC45nyDKWxPu9cK796vtrf7Fu3NZQmB,0.5065323958400496
1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih,0.5453396709136729
1RG5T6zGY4XovW75mTgpH6Bx7Y6uwwMmPToMCJSdMwdm4EW,0.3679712404353946
1RJP5i7zuyBLtgGTMCD9oF8zQMTQvfc4zpKNsVxfvTKdHmr,0.4824095496689415
1StVBqjDJKogQTsLioHC44iFch1cEAv2jcpsnvsy5buBtUE,0.4065652143054436
1WG3jyNqniQMRZGQUc7QD2kVLT8hkRPGMSqAb5XYQM1UDxN,0.2540182669600084
1dGsgLgFez7gt5WjX2FYzNCJtaCjGG6W9dA42d9cHngDYGg,0.4441334847501082
1hYyu9C3dupTiKGMNcrCRK6HVPS7LYznuofDXsia3N1W6AK,0.5370507641523767
```

