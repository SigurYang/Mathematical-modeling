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

def time_factor_processor(df):
    # 获取唯一的标识符和索引
    admission_num, admission_index = np.unique(df['mr_bah'], return_inverse=True)
    specimens = np.unique(df['specimen_code'])
    item_group_names = np.unique(df['item_group_name'])
    item_names = np.unique(df['item_name'])
    
    # 创建需要处理的列
    processed_columns = []
    for item_group in item_group_names:
        for item in item_names:
            processed_columns.append(f"{item_group}-{item}")
    
    # 创建初始的DataFrame
    processed_df = pd.DataFrame(0, columns=['mr_bah'] + processed_columns, index=specimens)
    processed_df.index.name = 'specimen_code'
    
    # 填充数据
    for i, row in df.iterrows():
        specimen_code = row['specimen_code']
        item_group = row['item_group_name']
        item_name = row['item_name']
        result_quantitative = row['result_quantitative']
        mr_bah = row['mr_bah']
        
        # 更新对应位置的值
        try:
            result_quantitative = float(result_quantitative)
        except:
            result_quantitative = float('inf')
        processed_df.at[specimen_code, f'{item_group}-{item_name}'] = result_quantitative
        processed_df.at[specimen_code, 'mr_bah'] = mr_bah
    
    # 根据'mr_bah'排序
    processed_df = processed_df.reset_index().sort_values(by=['mr_bah', 'specimen_code']).set_index('specimen_code')
    
    return processed_df

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