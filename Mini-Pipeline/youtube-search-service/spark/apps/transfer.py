import re
import pyspark.sql.functions as F
from pyspark.sql.types import StringType
import pandas as pd
from kiwipiepy import Kiwi


@F.pandas_udf(StringType())
def split_sents_udf(series: pd.Series) -> pd.Series:
    kiwi = Kiwi(typos='basic_with_continual')

    def split_and_clean(text):
        if not isinstance(text, str):
            return ""
        text = re.sub(r'(\xa0|\n|\u200b)', ' ', text)
        text = re.sub(r'\[.*?\]|\{.*?\}', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        sents = kiwi.split_into_sents(text, return_tokens=False, return_sub_sents=True)
        sents = [kiwi.join(kiwi.tokenize(s.text)) for s in sents]
        return '. '.join(sents) + "  : <<처리됨>> "

    return series.apply(split_and_clean)

def transfer(df, **args):
    df_transformed = df.withColumn(
        "script",
        split_sents_udf(F.col("script"))
    )
    return df_transformed


