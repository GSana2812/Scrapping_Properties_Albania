import pandas as pd

class Wrangling:

    @staticmethod
    def drop_unnamed_col(df: pd.DataFrame, col_name:str)->pd.DataFrame:
        return df.drop(columns=col_name)

    # Obtain only non-null values (from the target variable - price)
    @staticmethod
    def obtain_non_null_rows(df: pd.DataFrame, col_name:str)->pd.DataFrame:
        return df[~df[col_name].isnull()]

    # Format columns Gross Area, Interior Area, Price
    @staticmethod
    def format_columns(df: pd.DataFrame, col_name: str)->None:
        if col_name in ('Gross Area', 'Interior Area'):
            df[col_name] = df[col_name].str.replace(' m2', '').astype(float)

        elif col_name == 'Price':
            df[col_name] = df[col_name].str.replace(',','').astype(float)

        else:
            print('Column not found or error in processing')


