import os
import pandas as pd
import numpy as np
from lm_datahandler.datahandler import DataHandler
from scipy.io import loadmat


def new_datahandler_load_mat(mat_path):
    hypno = loadmat(os.path.join(mat_path, "psg_trans_label.mat"))["psg_trans_label"]
    hypno = np.array(hypno).squeeze()


    data_handler = DataHandler()
    eeg_and_acc = loadmat(os.path.join(mat_path, "eeg_and_acc.mat"))
    eeg = eeg_and_acc["eeg"]
    eeg = np.array(eeg).squeeze()

    epochs = eeg.shape[0]//(7500)
    eeg = eeg[0: epochs * 500 * 15]

    acc = eeg_and_acc["acc"]
    acc = np.array(acc).squeeze()
    acc = acc[:, 0:epochs * 50 * 15]

    hypno = hypno[:epochs]

    data_handler.eeg = eeg
    data_handler.raw_eeg = eeg
    data_handler.acc = acc
    data_handler.raw_acc = acc
    data_handler.features['meta'] = {'male': 1, 'age': 30, 'data_type': 0, 'h/w': 0}
    eeg_sec = eeg.shape[0] // 500
    data_handler.seconds = eeg_sec

    data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]}, tailor_type='no')
    data_handler.sleep_staging_with_internal_model(use_acc=False, staging_mode='offline')

    features = data_handler.features

    epoch = min(hypno.shape[0], features.shape[0])
    if hypno.shape[0] > epoch:
        hypno = hypno[0: epoch]
    if features.shape[0] > epoch:
        features = features.drop(features.index[epoch-features.shape[0]:])
    features['stage'] = hypno

    # 剔除标签异常的epoch
    features = features[features["stage"] <= 5]
    features = features[features["stage"] > 0]
    features = features.reset_index(drop=True)
    return features


def mat_data_to_npz(file_list):
    out_dir = 'E:/githome/lm_datahandler/lm_datahandler/train/'
    df = []
    data_file_list = open(file_list, 'r').readlines()
    data_list = [file[:-1] for file in data_file_list]

    for sub in data_list:
        data_path = sub
        features = new_datahandler_load_mat(data_path)
        df.append(features)
        print("------------" + sub + " finished------------------")

    df = pd.concat(df)

    # df = df[df['stage'] < 5]

    df['dataset'] = "tail"

    # Convert to category
    df['dataset'] = df['dataset'].astype('category')
    df['stage'] = df['stage'].astype('category')

    df = df.reset_index(drop=True)
    # %stage
    print(df['stage'].value_counts(normalize=True, sort=True))
    # Median value of the EEG IQR per stage
    print(df.groupby('stage')['eeg_iqr'].median())
    # Remove nights with a 9 in sleep stages
    # df.drop(index=df[df['stage'] == 9].index.get_level_values(0), level=0, inplace=True)

    # Number of unique nights in dataset
    print(df.index.get_level_values(0).nunique())
    # Export
    df.to_parquet(out_dir + 'xsr_eeg_acc_wholenight_20231218.parquet')


def create_filelist():
    list_dir = r'E:\dataset\x7_XSR'
    list = r'./train_list_xsr.txt'

    f = open(list, 'a+')
    for data_name in os.listdir(list_dir):
        if os.path.isdir(os.path.join(list_dir, data_name)):
            file_all = os.listdir(os.path.join(list_dir, data_name))
            if 'eeg_and_acc.mat' in file_all and 'psg_trans_label.mat' in file_all:
                f.write(list_dir + "\\" + data_name + "\n")


if __name__ == '__main__':
    # create_filelist()
    mat_data_to_npz("./train_list_xsr.txt")
