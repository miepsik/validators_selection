import requests
import pandas as pd
import io

f = open("../validators.csv", "rb")
files = {"validators":("../validators.csv", f)}

print("Testing file upload")
response = requests.post("http://127.0.0.1:14237/fileupload", files=files, data={"depth":2})
assert response.text == "Done"
print("File uploaded successfully")

response = requests.post("http://127.0.0.1:14237/next", json={"history": [[[2.0,3.0,2166958.6,780.0,8.0,998.0],[3.0,5349.8,2160212.4,960.0,1.0,385.0]]]})
response = eval(response.text)
model = response['model']

response = requests.post("http://127.0.0.1:14237/ranking", json={"model": model})
df = pd.read_csv(io.StringIO(response.text))
assert df.score[9] > df.score[5]
print("Model created successfully")
