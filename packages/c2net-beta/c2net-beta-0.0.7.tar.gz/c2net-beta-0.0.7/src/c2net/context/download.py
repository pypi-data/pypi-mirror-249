import os
import glob
from .env_check import dataset_to_env, pretrain_to_env, unzip_dataset
from ..utils import constants

def prepare_code():
    data_download_method = os.getenv(constants.DATA_DOWNLOAD_METHOD)
    if data_download_method is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.DATA_DOWNLOAD_METHOD} environment variables.')
    if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOXING:
        return prepare_code_for_moxing()
    if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOUNT:
        return prepare_code_for_mount()
    raise ValueError(f'Unknown data download method: {data_download_method}')

def prepare_dataset():
    data_download_method = os.getenv(constants.DATA_DOWNLOAD_METHOD)
    if data_download_method is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.DATA_DOWNLOAD_METHOD} environment variables.')
    if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOXING:
        return prepare_dataset_for_moxing()
    if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOUNT:
        return prepare_dataset_for_mount()
    raise ValueError(f'Unknown data download method: {data_download_method}')

def prepare_pretrain_model():
    data_download_method = os.getenv(constants.DATA_DOWNLOAD_METHOD)
    if data_download_method is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.DATA_DOWNLOAD_METHOD} environment variables.')
    if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOXING:
        return prepare_pretrain_model_for_moxing()
    if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOUNT:
        return prepare_pretrain_model_for_mount()
    raise ValueError(f'Unknown data download method: {data_download_method}')

def prepare_output_path():
    local_output_path = os.getenv(constants.LOCAL_OUTPUT_PATH)
    if local_output_path is None:
            raise ValueError(f'Failed to obtain environment variables. Please set the {constants.LOCAL_OUTPUT_PATH} environment variables.')
    else:	
        if not os.path.exists(local_output_path):	
            os.makedirs(local_output_path)   
    print(f'please set c2net_context.output_path as the output location')
    return local_output_path

def prepare_code_for_moxing():
    local_code_path= os.getenv(constants.LOCAL_CODE_PATH)
    if local_code_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.LOCAL_CODE_PATH} environment variables.')
    else:
        if not os.path.exists(local_code_path):
            os.makedirs(local_code_path) 
    return local_code_path

def prepare_dataset_for_moxing():
    dataset_url = os.getenv(constants.DATASET_URL)
    local_dataset_path = os.getenv(constants.LOCAL_DATASET_PATH)
    dataset_need_unzip= os.getenv(constants.DATASET_NEED_UNZIP, constants.DATASET_NEED_UNZIP_FALSE)

    if dataset_url is None or local_dataset_path is None:
        raise ValueError(f'Failed to obtain environment variables.Please set the {constants.PRETRAIN_MODEL_URL} and {constants.LOCAL_DATASET_PATH} environment variables')
    else:
        if not os.path.exists(local_dataset_path):
            os.makedirs(local_dataset_path)

    if dataset_url != "":
        dataset_to_env(dataset_url, local_dataset_path, dataset_need_unzip)
    else:
        print(f'No dataset selected')       
    return local_dataset_path

def prepare_pretrain_model_for_moxing():
    pretrain_model_url = os.getenv(constants.PRETRAIN_MODEL_URL)
    local_pretrain_model_path= os.getenv(constants.LOCAL_PRETRAIN_MODEL_PATH)
    pretrain_model_need_unzip= os.getenv(constants.PRETRAIN_MODEL_NEED_UNZIP, constants.PRETRAIN_MODEL_NEED_UNZIP_FALSE)
    if pretrain_model_url is None or local_pretrain_model_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.PRETRAIN_MODEL_URL} and {constants.LOCAL_PRETRAIN_MODEL_PATH} environment variables.')
    else:
        if not os.path.exists(local_pretrain_model_path):
            os.makedirs(local_pretrain_model_path) 
    if pretrain_model_url != "":             
        pretrain_to_env(pretrain_model_url, local_pretrain_model_path, pretrain_model_need_unzip)
    else:
        print(f'No pretrainmodel selected')           
    return local_pretrain_model_path   

def prepare_code_for_mount():
    local_code_path= os.getenv(constants.LOCAL_CODE_PATH)
    code_need_unzip = os.getenv(constants.CODE_NEED_UNZIP, constants.CODE_NEED_UNZIP_FALSE)
    if local_code_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.LOCAL_CODE_PATH} environment variables.')
    else:
        if not os.path.exists(local_code_path):
            os.makedirs(local_code_path) 
    if code_need_unzip == constants.CODE_NEED_UNZIP_TRUE:
        path = os.path.join(local_code_path, "*")
        for filename in glob.glob(path):
            if filename.endswith('.zip') or filename.endswith('.tar.gz'):
                base = os.path.basename(filename)
                dirname = os.path.splitext(base)[0]
                target_path = os.path.join(local_code_path, dirname)
                unzip_dataset(filename, target_path)
    return local_code_path

def prepare_dataset_for_mount():
    local_dataset_path = os.getenv(constants.LOCAL_DATASET_PATH)
    dataset_need_unzip = os.getenv(constants.DATASET_NEED_UNZIP, constants.DATASET_NEED_UNZIP_FALSE)
    if local_dataset_path is None :
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.LOCAL_DATASET_PATH} environment variables.')
    else:
        if not os.path.exists(local_dataset_path):
            os.makedirs(local_dataset_path)
    if dataset_need_unzip == constants.DATASET_NEED_UNZIP_TRUE:
        path = os.path.join(local_dataset_path, "*")
        for filename in glob.glob(path):
            if filename.endswith('.zip') or filename.endswith('.tar.gz'):
                base = os.path.basename(filename)
                dirname = os.path.splitext(base)[0]
                target_path = os.path.join(local_dataset_path, dirname)
                unzip_dataset(filename, target_path)
    return local_dataset_path    

def prepare_pretrain_model_for_mount():
    local_pretrain_model_path= os.getenv(constants.LOCAL_PRETRAIN_MODEL_PATH)
    if local_pretrain_model_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.LOCAL_PRETRAIN_MODEL_PATH} environment variables.')
    else:
        if not os.path.exists(local_pretrain_model_path):
            os.makedirs(local_pretrain_model_path) 
    return local_pretrain_model_path
