

# Validators selection

Implementation of UTA approach for validators selection based on nominator's preferences.


# Endpoints

Specification of exposed endpoints

## New file
Accepts new file with validators description, should be called at the start of each era.

Endpoint: \fileuploadPolkadot\
Method: POST\
Time: ~15 minutes for depth=6\
Parameters:
 - validators - a csv file containing validators that might be recommended to a nominator
 - depth - an integer denoting number of questions to compute in advance (default 7)

Output:
 - 200 "DONE" if properly calculated
 - 400 "Validators file not provided" if there isn't a parameter called validators
 - 400 "Invalid file structure, expected 7 columns, got x" if structure of the file is not matching the expected structure

## Next pair
Search for an optimal question to maximize model's information gain and therefore provide recommendations matching nominator's preferences better.

Endpoint: \nextPolkadot\
Method: POST\
Time: ~200ms per pair\
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

Endopint: \rankingPolkadot\
Method: POST\
Time: ~150ms\
Parameters:
 - model - model from "\next" function for which the ranking should be calculated 

Output:
 - 400, "Model not provided" if model parameter is missing
 - 400, "col not present in the model" if model structure is not correct
 - 200, coma separated string with two columns: validator, score

# Tests

## Environment
 ### python 3.8 installed
 - pip3 install -r requirements.txt
 - pip3 install requests (to run integration test) 
 ### python 3.9 installed
 - pip3 install -r requirementsLocal.txt
## Execution
To run unit tests execute ```python -m unittest discover``` in the main directory, not in the /test.

When docker is running:
 - docker build -t "validators_selection:Dockerfile" .
 - docker run -p 14237:14237 validators_selection:Dockerfile

 additional test can be executed from the test directory ```python integration_test.py```
# Example
Call:
```
curl -X POST -F 'validators=@validators.csv' -F 'depth=2' localhost:14237/fileuploadPolkadot
```
Response:
```
DONE
```

Call:
```
curl -X POST http://localhost:14237/nextPolkadot -H 'Content-Type: application/json' -d '{"history": []}'
```
Response:
```json
{"model":[],"quality":-1,"validatorA":{"history":[[[10.0,1.0,2162675.0,880.0,1.0,451.0],[2.0,3.0,2166958.6,780.0,8.0,998.0]]],"values":{"clusterSize":1.0,"commission":10.0,"eraPoints":880.0,"selfStake":1.0,"totalStake":2162675.0,"voters":451.0}},"validatorB":{"history":[[[2.0,3.0,2166958.6,780.0,8.0,998.0],[10.0,1.0,2162675.0,880.0,1.0,451.0]]],"values":{"clusterSize":8.0,"commission":2.0,"eraPoints":780.0,"selfStake":3.0,"totalStake":2166958.6,"voters":998.0}}}
```

Call:
```
curl -X POST http://localhost:14237/nextPolkadot -H 'Content-Type: application/json' -d '{"history": [[[2.0,3.0,2166958.6,780.0,8.0,998.0],[10.0,1.0,2162675.0,880.0,1.0,451.0]]]}'
```
Response:
```json
{"model":{"clusterSize":[[1.0,5.0,9.0,13.0],[0.0,0.0045360601507127285,0.016621457412838936,0.01422062423080206]],"commission":[[0.5,1.0,4.0,7.0,10.0],[0.2627783715724945,0.20055368542671204,0.13935373723506927,0.07155085355043411,0.0]],"eraPoints":[[780.0,926.6666666666666,1073.3333333333333,1220.0],[0.0,0.07101559638977051,0.14314094185829163,0.2209450751543045]],"selfStake":[[1.0,201480.7333333333,402960.4666666666,604440.2],[0.0,0.08295433223247528,0.16195763647556305,0.23893168568611145]],"totalStake":[[1942391.7,2728076.2666666666,3513760.8333333335,4299445.4],[0.23925749957561493,0.15444865822792053,0.08066676557064056,0.0]],"voters":[[279.0,1042.3333333333335,1805.6666666666667,2569.0],[0.0,0.021465888246893883,0.011682764627039433,0.015950998291373253]]},"quality":-0.3494505494505495,"validatorA":{"history":[[[1.5,3801.3,2167745.0,860.0,1.0,1166.0],[10.0,604440.2,4299445.4,860.0,1.0,458.0]],[[2.0,3.0,2166958.6,780.0,8.0,998.0],[10.0,1.0,2162675.0,880.0,1.0,451.0]]],"values":{"clusterSize":1.0,"commission":1.5,"eraPoints":860.0,"selfStake":3801.3,"totalStake":2167745.0,"voters":1166.0}},"validatorB":{"history":[[[10.0,604440.2,4299445.4,860.0,1.0,458.0],[1.5,3801.3,2167745.0,860.0,1.0,1166.0]],[[2.0,3.0,2166958.6,780.0,8.0,998.0],[10.0,1.0,2162675.0,880.0,1.0,451.0]]],"values":{"clusterSize":1.0,"commission":10.0,"eraPoints":860.0,"selfStake":604440.2,"totalStake":4299445.4,"voters":458.0}}}
```

Call:
```
curl -X POST http://localhost:14237/rankingPolkadot -H 'Content-Type: application/json' -d '{"model":{"clusterSize": [[1.0, 5.0, 9.0, 13.0], [0.0, 0.04, 0.07, 0.06]], "commission": [[0.5, 1.0, 4.0, 7.0, 10.0], [0.25, 0.18, 0.12, 0.06, 0.0]], "eraPoints": [[780, 926, 1073, 1220], [0.0, 0.05, 0.12, 0.2]], "selfStake": [[1.0, 201480, 402960, 604440.2], [0.0, 0.08, 0.15, 0.22]], "totalStake": [[1942391.7, 2728076, 3513760, 4299445.4], [0.22, 0.14, 0.07, 0.0]], "voters": [[279.0, 1042, 1805, 2569.0], [0.0, 0.02, 0.01, 0.02]]}}'
```
Response:
```json
{
   "score":{
      "11BgR7fH8Sq6CcGcXxZrhyrBM2PUpDmhnGZpxPGvVGXEiPT":0.2363253933,
      "11MJU5Q1rQh5BKuuECePhSAutv3WEVx6f2x9eZk9HXkCC1e":0.4779707505,
      "11uMPbeaEDJhUxzU4ZfWW9VQEsryP9XqFcNRfPdYda6aFWJ":0.4407020016,
      "14Vh8S1DzzycngbAB9vqEgPFR9JpSvmF1ezihTUES1EaHAV":0.4404848282,
      "1A2ATy1FEu5yQ9ZzghPLsRckPQ7XLmq5MJQYcTvGnxGvCho":0.3200742682,
      "1ChRPtPxrTfFTSWyKHtF6ASvaSjL5jqz6f68ih15zcjyM1V":0.4089138424,
      "1LMtHkfrADk7awSEFC45nyDKWxPu9cK796vtrf7Fu3NZQmB":0.4701029547,
      "1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih":0.5216442482,
      "1RG5T6zGY4XovW75mTgpH6Bx7Y6uwwMmPToMCJSdMwdm4EW":0.3568800114,
      "1RJP5i7zuyBLtgGTMCD9oF8zQMTQvfc4zpKNsVxfvTKdHmr":0.438481586,
      "1StVBqjDJKogQTsLioHC44iFch1cEAv2jcpsnvsy5buBtUE":0.4104116691,
      "1WG3jyNqniQMRZGQUc7QD2kVLT8hkRPGMSqAb5XYQM1UDxN":0.2520892655,
      "1dGsgLgFez7gt5WjX2FYzNCJtaCjGG6W9dA42d9cHngDYGg":0.4143351187,
      "1hYyu9C3dupTiKGMNcrCRK6HVPS7LYznuofDXsia3N1W6AK":0.5446222004
   }
}
```

