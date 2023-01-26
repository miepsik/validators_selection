import unittest
import polkadot
import io
import pandas as pd
import json
import time

class ValidatorsSelectionTest(unittest.TestCase):

    def setUp(self):
        polkadot.app.testing = True
        self.app = polkadot.app.test_client()
        
    def test_fileuploadNoFile(self):
        result = self.app.post('fileupload', data={'validator':(open('validators.csv', 'rb'), 'validators.csv'), 'depth':2})
        self.assertEqual(result.data, b"Validators file not provided")
        
    def test_fileuploadWrongFormat(self):
        result = self.app.post('fileupload', data={'validators':(open('validatorsWrong.csv', 'rb'), 'validatorsWrong.csv'), 'depth':2})
        self.assertEqual(result.data, b"Invalid file structure, expected 7 columns, got 6")

    def test_fileupload(self):
        result = self.app.post('fileupload', data={'validators':(open('validators.csv', 'rb'), 'validators.csv'), 'depth':2})
        self.assertEqual(result.data, b"Done")
        
    def test_query(self):
        result = self.app.post('fileupload', data={'validators':(open('validators.csv', 'rb'), 'validators.csv'), 'depth':2})
        self.assertEqual(result.data, b"Done")
        start = time.time()
        result = self.app.post('next', data=json.dumps({'history':[]}), content_type='application/json')
        response = eval(result.data)
        quality0 = response['quality']
        history = response['validatorA']['history']
        result = self.app.post('next', data=json.dumps({'history':history}), content_type='application/json')
        response = eval(result.data)
        quality1 = response['quality']
        end = time.time()
        self.assertTrue(end-start < 1)
        self.assertTrue(quality1 > quality0)
        
    def test_query2(self):
        result = self.app.post('fileupload', data={'validators':(open('validatorsEval.csv', 'rb'), 'validatorsEval.csv'), 'depth':2})
        self.assertEqual(result.data, b"Done")
        model = {'Cluster Size': [[1.0, 5.0, 9.0, 13.0], [0.0, 0.04, 0.07, 0.06]], 'Commission (in %)': [[0.5, 1.0, 4.0, 7.0, 10.0], [0.25, 0.18, 0.12, 0.06, 0.0]], 'Era Points': [[780, 926, 1073, 1220], [0.0, 0.05, 0.12, 0.2]], 'Self Stake (in DOT)': [[1.0, 201480, 402960, 604440.2], [0.0, 0.08, 0.15, 0.22]], 'Total Stake (in DOT)': [[1942391.7, 2728076, 3513760, 4299445.4], [0.22, 0.14, 0.07, 0.0]], 'Voters': [[279.0, 1042, 1805, 2569.0], [0.0, 0.02, 0.01, 0.02]]}
        response = self.app.post('ranking', data=json.dumps({'model':model}), content_type='application/json')
        response = response.data
        df = pd.read_csv(io.BytesIO(response))
        expected = [0.08, 0.57, 0.31, 0.38, 0.28]
        for i in range(len(expected)):
            self.assertTrue(abs(df.score.values[i]-expected[i])<0.0001)
