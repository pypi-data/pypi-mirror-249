"""
Author: Daryl.Xu
E-mail: xuziqiang@zyheal.com
"""
import logging
import os
import zipfile
import shutil

from pdf_client_wrapper.rpc import pdf_pb2
from pdf_client_wrapper import app_config


def gen_stream(file_path: str):
    with open(file_path, 'rb') as f:
        chunk = f.read(app_config.CHUNK_SIZE)
        while chunk:
            logging.debug('the chunk, size: %d', len(chunk))
            # stub.uploadResource()
            yield pdf_pb2.Chunk(content=chunk)
            chunk = f.read(app_config.CHUNK_SIZE)


def zip_dir(source_dir: str, target_file: str):
    """
    将给定目录下的所有文件都添加到目标zip文件中，遇到符号链接文件则读取其指向的文件。

    Add all the files contained in the source_dir into the target_file(a zip file),
    read the target file which symbolic links file references to.
    """
    resources_path_length = len(source_dir)

    # TODO write to bytes instead of file
    with zipfile.ZipFile(target_file, 'w') as zip_file:
        path_iterator = os.walk(source_dir, followlinks=True)
        for i in path_iterator:
            dirname = i[0]
            # print('iterator: ', i)
            for filename in i[2]:
                full_path = os.path.join(dirname, filename)
                realpath = os.path.realpath(full_path)
                arcname = full_path[resources_path_length:]
                # print(f'related path: {arcname}, real path: {realpath}')
                zip_file.write(realpath, arcname)


def zip_folder(dir_path):
    """
    压缩一个文件夹，保存在当前目录
    """
    # 确保目标 ZIP 文件名是有效的
    zip_filename = dir_path + ".zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    # 创建一个新的 ZIP 文件
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dir_path):
            for file in files:
                # 构建完整的文件路径
                file_path = os.path.join(root, file)
                # 构建 ZIP 文件内的相对路径
                rel_path = os.path.relpath(file_path, dir_path)
                # 将文件添加到 ZIP 文件中
                zipf.write(file_path, rel_path)
    return zip_filename
