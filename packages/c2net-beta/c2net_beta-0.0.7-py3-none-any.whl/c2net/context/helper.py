import os
import json
import moxing as mox
import zipfile
import tarfile
from ..utils import constants
from .env_check import unzip_dataset
def moxing_dataset_to_env(multi_data_url, data_dir, unzip_required):    
    multi_data_json = json.loads(multi_data_url)
    for i in range(len(multi_data_json)):
        datasetfile_path = os.path.join(data_dir, multi_data_json[i]["dataset_name"])
        if unzip_required == constants.DATASET_NEED_UNZIP_TRUE:
            try:
                mox.file.copy(multi_data_json[i]["dataset_url"], datasetfile_path) 
                print("Successfully Download {} to {}".format(multi_data_json[i]["dataset_url"],datasetfile_path))
                filename = os.path.splitext(multi_data_json[i]["dataset_name"])[0]
                unzipfile_path = data_dir + "/" + filename
                if not os.path.exists(unzipfile_path):
                    os.makedirs(unzipfile_path)
                unzip_dataset(datasetfile_path, unzipfile_path)
            except Exception as e:
                print(f'❌ moxing download {multi_data_json[i]["dataset_url"]} to {datasetfile_path} failed: {str(e)}')
        else:
            try:
                mox.file.copy_parallel(multi_data_json[i]["dataset_url"], datasetfile_path)
                print(f'🎉 Successfully Download {multi_data_json[i]["dataset_url"]} to {datasetfile_path}')
            except Exception as e:
                print(f'❌ moxing download {multi_data_json[i]["dataset_url"]} to {datasetfile_path} failed: {str(e)}')
    return

def moxing_pretrain_to_env(pretrain_url, pretrain_dir, unzip_required):
    """
    copy pretrain to training image
    """
    pretrain_url_json = json.loads(pretrain_url)  
    for i in range(len(pretrain_url_json)):
        modelfile_path = pretrain_dir + "/" + pretrain_url_json[i]["model_name"]
        if unzip_required == constants.DATASET_NEED_UNZIP_TRUE:
            try:
                mox.file.copy(pretrain_url_json[i]["model_url"], modelfile_path) 
                print("Successfully Download {} to {}".format(pretrain_url_json[i]["model_url"], modelfile_path))
                filename = os.path.splitext(pretrain_url_json[i]["model_name"])[0]
                unzipfile_path = pretrain_dir + "/" + filename
                if not os.path.exists(unzipfile_path):
                    os.makedirs(unzipfile_path)
                unzip_dataset(modelfile_path, unzipfile_path)
            except Exception as e:
                print(f'❌ moxing download {pretrain_url_json[i]["model_url"]} to {modelfile_path} failed: {str(e)}')
        else:
            try:
                mox.file.copy_parallel(pretrain_url_json[i]["model_url"], modelfile_path) 
                print(f'🎉 Successfully Download {pretrain_url_json[i]["model_url"]} to {modelfile_path}')
            except Exception as e:
                print(f'❌ moxing download {pretrain_url_json[i]["model_url"]} to {modelfile_path} failed: {str(e)}')
    return        

def obs_copy_file(obs_file_url, file_url):
    """
    cope file from obs to obs, or cope file from obs to env, or cope file from env to obs
    """
    try:
        mox.file.copy(obs_file_url, file_url)
        print(f'🎉 Successfully Download {obs_file_url} to {file_url}')
    except Exception as e:
        print(f'❌ moxing download {obs_file_url} to {file_url} failed: {str(e)}')
    return    
    
def obs_copy_folder(folder_dir, obs_folder_url):
    """
    copy folder from obs to obs, or copy folder from obs to env, or copy folder from env to obs
    """
    try:
        mox.file.copy_parallel(folder_dir, obs_folder_url)
        print(f'🎉 Successfully Download {folder_dir} to {obs_folder_url}')
    except Exception as e:
        print(f'❌ moxing download {folder_dir} to {obs_folder_url} failed: {str(e)}')
    return     

def upload_folder(folder_dir, obs_folder_url):
    """
    upload folder to obs
    """
    try:
        mox.file.copy_parallel(folder_dir, obs_folder_url)
        print(f'🎉 Successfully Upload {folder_dir} to {obs_folder_url}')
    except Exception as e:
        print(f'❌ moxing upload {folder_dir} to {obs_folder_url} failed: {str(e)}')
    return       