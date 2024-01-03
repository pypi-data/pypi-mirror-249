import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame
from matplotlib import pyplot as plt
import seaborn as sns
from typing import List
import pandas as pd


def missing_values_ratio(df: DataFrame) -> DataFrame:
    count = df.count()
    numeric_cols = [c for c, t in df.dtypes if t in ["int", "float", "double"]]

    numeric_func = lambda c: (F.col(c) == "") | (F.col(c).isNull()) | (F.isnan(F.col(c)))
    non_numeric_func = lambda c: (F.col(c) == "") | (F.col(c).isNull())

    return df.select(
        [
            (F.count(F.when(numeric_func(c) if c in numeric_cols else non_numeric_func(c), c)) / count).alias(c)
            for c in df.columns
        ]
    )


def cardinalities(df: DataFrame) -> DataFrame:
    return df.select([F.countDistinct(F.col(c)).alias(c) for c in df.columns])


def frequencies(df: DataFrame, col: str) -> DataFrame:
    df_group = df.groupBy(F.col(col)).count().sort(F.desc("count"))
    total = df_group.groupBy().agg(F.sum("count").alias("total")).collect()[0].total
    return df_group.withColumn("total", F.lit(total)).withColumn("ratio", F.col("count") / F.col("total")).drop("total")


def cast(df: DataFrame, cols: List[str], type: T.DataType) -> DataFrame:
    for col in cols:
        df = df.withColumn(col, F.col(col).cast(type))
    return df


def deciles(df: DataFrame, col: str) -> list:
    df_filtered = df.filter((F.col(col) != 0) & (F.col(col).isNotNull()) & (~F.isnan(col)))
    return df_filtered.approxQuantile(col, [x / 10 for x in range(10)], 0.1)


def plot_hist_cat(df: DataFrame, col: str, title: str = None, hue: str = None, max_bins: int = 0) -> None:
    group = [col]
    if hue is not None:
        group.append(hue)

    if 0 < max_bins:
        df_max_bins_joiner = df.groupBy([col]).count().sort(F.col("count").desc()).limit(max_bins)
        df = df.join(df_max_bins_joiner, on=col)

    ds = df.groupBy(group).count().sort(group).toPandas()

    plt.clf()
    sns.barplot(ds, x=col, y="count", hue=hue)
    plt.xticks(rotation=45)
    if title is not None:
        plt.title(title)
    plt.show()


def plot_hist_num(df: DataFrame, col: str, bins: int = 12, title: str = None):
    data = df.select(col).rdd.flatMap(lambda x: x).histogram(bins)
    ds = pd.DataFrame(list(zip(*data)), columns=[col, "count"])
    plt.clf()
    sns.barplot(ds, x=col, y="count")
    if title is not None:
        plt.title(title)
    plt.show()
