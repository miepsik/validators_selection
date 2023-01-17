import numpy as np

class Selector:
    def __init__(self, df):
        self.df = df

    def select(self, model): 
        droped = self.df.drop_duplicates()
        bestScore = -99
        bestPair = None
        for _ in range(20):
            try:
                i, j = np.random.choice(np.arange(len(droped)), 2)
                score = model.scorePair(droped.iloc[i].values, droped.iloc[j].values)
                if score > bestScore:
                    bestScore = score
                    bestPair = (i, j)
            finally:
                pass
        i, j = bestPair
        return (droped.iloc[i].values, droped.iloc[j].values)
       

    def updateModel(self, model):
        self.model = model
        return model.getPrecision()
