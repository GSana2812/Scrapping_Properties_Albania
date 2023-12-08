import pandas as pd
from typing import List
import matplotlib.pyplot as plt

class Analysis:


    @staticmethod
    def general_info(df: pd.DataFrame)->None:
        print(df.info())
        print(df.head())
        print(df.describe())

    @staticmethod
    def histograms(df: pd.DataFrame, cols: List[str])->None:
        df[cols].hist(bins=75, figsize=(12, 8))
        plt.show()
