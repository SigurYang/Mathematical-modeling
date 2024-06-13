import pandas as pd
import numpy as np
import os
from collections import Counter


def data_reader(data_path,data_file,fill_na=''):
    '''
    读取数据
    可选择是否填充nan值
    '''
    data_path = os.path.join(data_path,data_file)
    df = pd.read_excel(data_path)[1:]
    if fill_na is not None:
        df = df.fillna(fill_na)

    return df

def frequency_count(df):
    all_text = ' '.join(df.astype(str).values.flatten())

    # 使用Counter统计每个词的频率
    df_count = Counter(all_text.split())
    count_df = pd.DataFrame(df_count.items(), columns=['word', 'frequency']).sort_values(by='frequency', ascending=False)
    
    return count_df


def Infector_chooser(
        df,
        key='颅内感染',
        index=False):
    '''
    返回感染者和非感染者
    '''
    infection_index = df.apply(lambda row: row.astype(str).str.contains(key, na=False).any(), axis=1)
    rows_with_infection = df[infection_index]
    rows_without_infection = df[~infection_index]
    if index:
        return rows_with_infection, rows_without_infection, infection_index
    else:
        return rows_with_infection, rows_without_infection

def patient_splitter(
        df,
        indicators=['mr_bah', 'mr_xb', 'mr_nn', 'mr_sjzyts', 'mr_cyzyzdmc', 'mr_cyqtzdmc1',
       'mr_cyqtzdmc2', 'mr_cyqtzdmc3', 'mr_cyqtzdmc4', 'mr_cyqtzdmc5',
       'mr_cyqtzdmc6', 'mr_cyqtzdmc7', 'mr_cyqtzdmc8', 'mr_cyqtzdmc9',
       'mr_cyqtzdmc10', 'mr_ssmc1', 'mr_ssmzfs1', 'mr_sscxsj1', 'mr_ssmc2',
       'mr_ssmzfs2', 'mr_ssmc3', 'mr_ssmzfs3', 'mr_ssmc4', 'mr_ssmzfs4',
       'mr_sscxsj4']
        ):
    '''
    返回选中病人属性的唯一值
    '''
    
    Patients = df[indicators]
    Patients = Patients.drop_duplicates()

    return Patients

def one_hot(df,columns):
    '''
    用于将标签映射到onehot编码
    输入为dataframe
    columns需要和dataframe列数一致，用于列表标记
    '''
    data_size = len(df)
    is_series = len(df.shape) == 1
    one_hot_matrix = pd.DataFrame(0, index=np.arange(data_size), columns=columns)
    for i in range(data_size):
        category = df.iloc[i]
        if not is_series:
            category = " ".join(category.astype(str).values.flatten())
            category = category.strip().split(" ")
            category = pd.unique(category)
        one_hot_matrix.loc[i, category] += 1
    return one_hot_matrix


if __name__ == "__main__":
    data_path = './data'
    data_file = "治疗过程记录.xlsx"

    df = data_reader(data_path,data_file)