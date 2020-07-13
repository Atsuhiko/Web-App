import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno


def draw_pairplot(df):

    # sns で描画
    # sns_plot_1 = sns.pairplot(df, hue="label")
    # label列がないデータの時に失敗するためheuパラメータを除外
    sns_plot_1 = sns.pairplot(df)

    # グラフ画像を保存
    filepath_1 = "./graph/pairplot.png"
    sns_plot_1.savefig(filepath_1)

    return filepath_1


def draw_lmplot(df):

    # 数値featureが2列以上存在しているか。いない場合は、新しくfeatureを作成。
    if len(df.select_dtypes(include="number").columns) < 2:
        append = np.arange(0, len(df))
        df["__append1__"] = pd.Series(append)
        df["__append2__"] = pd.Series(append)

    # type=number　の columna-name から　グラフに使用する seriesを選択
    x = df.select_dtypes(include="number").columns[0]
    y = df.select_dtypes(include="number").columns[1]

    # sns で描画
    # sns_plot_2 = sns.lmplot(x="a1", y="a4", data=df, hue="label")
    sns_plot_2 = sns.lmplot(x=x, y=y, data=df)

    # グラフ画像を保存
    filepath_2 = "./graph/lmplot.png"
    sns_plot_2.savefig(filepath_2)

    return filepath_2


def draw_duplicated(df):

    # 重複行数を算出
    df_dup = pd.DataFrame(df.duplicated())
    df_dup = df_dup.rename(columns={0: "isdup"})

    # グラフを描画
    fig_dup = sns.catplot(x="isdup", kind="count", data=df_dup)
    fig_dup.set_xticklabels(rotation=90)

    # グラフ画像を保存
    filepath = "./graph/duplicated.png"
    fig_dup.savefig(filepath)

    return filepath


def draw_missing(df):

    # missingno
    fig = missingno.matrix(df).get_figure()

    # グラフ画像を保存
    filepath = "./graph/missing.png"
    fig.savefig(filepath)

    return filepath


# グラフが意図したとおりに生成去れない問題が未解決 (2020.07.10)
def draw_univariate_analysis(df):
    print("utils.draw_univariate_analysis: start")

    # 列数を算出
    height = len(df.columns)

    # subplotを生成
    fig = plt.figure()

    # グラフを生成
    for i, cname in enumerate(df.columns):
        if df[cname].dtype in (np.float64, np.float32, np.int32, np.int64):
            print("utils.draw_univariate_analysis: dtype: ", df[cname].dtype)
            print("utils.draw_univariate_analysis: draw distplot")
            ax = fig.add_subplot(1, height, i)
            sns.distplot(df[cname], ax=ax)
        else:
            print("utils.draw_univariate_analysis: dtype: ", df[cname].dtype)
            print("utils.draw_univariate_analysis: draw catplot")
            ax = fig.add_subplot(1, height, i)
            sns.catplot(x=cname, kind="count", data=df, ax=ax)
    plt.close("all")
    plt.tight_layout()

    # グラフ画像を保存
    filepath = "./graph/univariate.png"
    fig.savefig(filepath)

    return filepath
