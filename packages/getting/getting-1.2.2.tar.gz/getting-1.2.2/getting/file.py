import mimetypes
import os
import random
import shutil
import time
from datetime import datetime
import psutil
import requests
from tqdm import tqdm
from typing import Union, Literal
import re
import sys


def download(
    url,
    save_folder="tmp",
    custom_name=None,
    max_retries=10,
    timeout=(5, 30),
    chunk_size=99 * 1024 * 1024,
):
    "下载文件 下载速度控制3mb =  3 * 1024 * 1024"
    # 创建保存文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    retries = 0
    save_path = None  # 初始化保存路径
    while retries < max_retries:
        try:
            # 从外链下载文件
            response = requests.get(url, stream=True, timeout=timeout)

            if response.status_code == 200:
                # 获取文件的MIME类型
                content_type = response.headers.get("content-type")
                file_extension = mimetypes.guess_extension(content_type) or ""

                if custom_name:
                    file_name = custom_name + file_extension
                else:
                    # 生成时间戳+随机数作为文件名
                    timestamp = int(time.time())
                    file_name = (
                        f"{timestamp}{random.randint(1000, 10000)}{file_extension}"
                    )

                # 构建保存路径
                save_path = os.path.join(save_folder, file_name)

                # 获取文件总长度
                content_length = response.headers.get("content-length")
                if content_length is not None:
                    content_length = int(content_length)
                else:
                    content_length = 0  # 设置一个默认值或者根据需求进行处理

                with open(save_path, "ab") as f:  # 使用追加模式
                    with tqdm(
                        total=content_length, unit="B", unit_scale=True, desc="下载进度"
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))

                print(f"文件已下载并保存到 {save_path}")

                # 返回文件名和完整路径
                data = {
                    "response": response,
                    "filename": file_name,
                    "filepath": save_path,
                    "extension": file_extension,
                }
                return data
            else:
                print(f"无法下载文件，尝试次数：{retries + 1}")
                retries += 1
        except Exception as e:
            print(f"下载过程中出现错误: {e}")
            retries += 1
            if save_path is not None and os.path.exists(save_path):
                os.remove(save_path)  # 删除已下载的文件

    print("达到最大尝试次数，无法下载文件，删除已下载的文件")
    if save_path is not None and os.path.exists(save_path):
        os.remove(save_path)  # 删除已下载的文件
    return None


def delete(file_path):
    "删除文件"
    try:
        os.remove(file_path)
        print(f"临时文件 {file_path} 已删除")
    except Exception as e:
        print(f"无法删除临时文件 {file_path}: {e}")


def extract_extension(file_name):
    "使用split()函数来分割文件名和扩展名"
    parts = file_name.split(".")
    if len(parts) > 1:
        # 如果文件名中包含多个点,只取最后一个点后面的部分作为扩展名
        extension = parts[-1]
        return extension
    else:
        # 如果文件名中没有点,或者只有一个点,说明没有扩展名
        return None


def file_name(full_filename):
    "返回不包含扩展名的文件名"
    filename = os.path.basename(full_filename)
    filename_without_extension, _ = os.path.splitext(filename)
    return filename_without_extension


def remove_suffix(text, suffix):
    "删除文件名的格式"
    if text.endswith(suffix):
        return text[: -len(suffix)]
    else:
        return text


def has_file_extension(filename):
    "是否有扩展"
    _, extension = os.path.splitext(filename)
    return bool(extension)


def remove_file_extension(filename):
    "删除扩展名称"
    name, _ = os.path.splitext(filename)
    return name


def remove_substring(a, b):
    "删除指定的值"
    return a.replace(b, "")


def copy_file_if_not_exists(source_path, destination_path):
    "A 复制到 B"
    # 检查目标路径是否已经存在相同文件
    if os.path.exists(destination_path):
        print(f"文件已经存在于目标路径: {destination_path}")
    else:
        try:
            # 复制文件
            shutil.copy2(source_path, destination_path)
            print(f"文件已成功复制到: {destination_path}")
        except Exception as e:
            print(f"复制文件时发生错误: {e}")


def check_file_existence(file_path, file_name, possible_formats):
    "检测文件格式是什么"
    # 尝试不同的文件格式扩展名来检查文件是否存在
    for ext in possible_formats:
        file_path_with_ext = os.path.join(file_path, file_name + ext)
        if os.path.exists(file_path_with_ext):
            return True, ext  # 文件存在,返回存在标志和文件格式扩展名
    return False, None  # 文件不存在


def rename_special_characters(name, special_characters=None):
    "替换特殊字符"
    # 特殊字符列表
    if not special_characters:
        special_characters = [
            "#.",
            "#",
            "￥",
            "%",
            "$",
            "&",
            "!",
            "\\",
            "/",
            "?",
            "^",
            "*",
            "'",
            '"',
            "`",
            ":",
            ";",
            "<",
            ">",
            "|",
            "?",
            "\n",
            "，",
            "。",
            "{",
            "}",
        ]
    # 替换特殊字符
    for char in special_characters:
        name = name.replace(char, "_")
    return name


def disk_usage(path, no_print=False):
    "检查路径是否存在"
    if os.path.exists(path):
        try:
            partition = psutil.disk_usage(path)
            if not no_print:
                print("开始检查硬盘")
                print("磁盘路径:", path)
                print("总大小:", partition.total)
                print("已用空间:", partition.used)
                print("剩余空间:", partition.free)
                print("使用率:", partition.percent, "%")
                print("结束检查硬盘")
            return partition
        except PermissionError:
            print(f"无法访问路径 {path} 的信息，可能需要管理员权限。")
    else:
        print(f"路径 {path} 不存在。")


def check_disk_usage(path, percent=90, task_print=False, task_name=""):
    "检查磁盘使用率是否超过一定值"
    partition = disk_usage(path)
    usage_percent = partition.percent
    usage = usage_percent > percent
    if usage and task_print:
        print(f"-----------------------------------磁盘使用率超过{percent}%，停止{task_name}任务。")
    return usage


def find_images_in_directory(
    directory, root_directory, results=None, extension=(".png", ".jpg")
):
    "递归查询指定目录内的文件并返回对象"
    if results is None:
        results = []

    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isdir(filepath):
                # 递归调用函数，查询子目录
                find_images_in_directory(filepath, root_directory, results)
            elif filename.lower().endswith(extension):
                # 如果是png或jpg文件，则将结果添加到列表中
                relative_path = os.path.relpath(filepath, root_directory)
                image_name = os.path.basename(filepath)
                results.append({"name": file_name(image_name), "path": relative_path})

    except PermissionError as e:
        print(f"权限错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

    return results


def remove_empty_directories(directory):
    "清空目录下所有空目录"
    try:
        for root, dirs, files in os.walk(directory, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"空目录已删除：{dir_path}")

    except PermissionError as e:
        print(f"权限错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def log_to_file(
    log_message,
    dir,
    path,
    should_rotate=True,
    max_size_bytes=10 * 1024 * 1024,
    backup_dir="backup_logs",
):
    "创建日志"

    # 创建目录（如果不存在）
    os.makedirs(dir, exist_ok=True)

    # 创建文件（如果不存在）
    with open(path, "a", encoding="utf-8", newline="") as log_file:
        log_file.write(f"{log_message}\n")

    log_size = os.path.getsize(path)

    if should_rotate and log_size > max_size_bytes:
        # 如果启用切割日志且超过大小限制
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        counter = 1

        # 生成唯一的备份文件名
        while True:
            backup_filename = f"{os.path.basename(path)}.{timestamp}.{counter}"
            backup_path = os.path.join(dir, backup_dir, backup_filename)

            if not os.path.exists(backup_path):
                break

            counter += 1

        os.makedirs(os.path.join(dir, backup_dir), exist_ok=True)
        os.rename(path, backup_path)
        print(f"日志已切割，备份为 {backup_path}")


def log_and_print(message, log_dir, log_path, is_print=True):
    "创建日志以及输出"
    log_message = f"[{datetime.now()}] {message}"
    log_to_file(log_message, log_dir, log_path)
    if is_print:
        print(log_message)
    return message


def is_file_in_directory(directory, file_name):
    "查询文件是否存在"
    file_path = os.path.join(directory, file_name)
    return os.path.isfile(file_path)


def is_file_with_name_in_directory(directory, file_name):
    "查询文件是否存在 - 忽略格式名"
    for filename in os.listdir(directory):
        if filename.startswith(file_name):
            return True
    return False


def delimiter_name_extract(
    filename,
    delimiters=["[]", "【】"],
    mode: Union[Literal["all"], Literal["num"]] = "all",
):
    """
    通过定界符提取名称

    mode='all' = 提取定界符内全部字符

    mode='num' = 提取定界符内数字
    """

    valid_modes = ["all", "num"]  # 可接受的 mode 值
    if mode not in valid_modes:
        raise ValueError(f"无效的模式。请选择以下模式之一：{', '.join(valid_modes)}")

    if mode == "num":
        pattern = r"\d+"
    else:
        pattern = r"\w+"

    for delim in delimiters:
        match = re.search(
            rf"{re.escape(delim[0])}({pattern}){re.escape(delim[1])}", filename
        )
        if match:
            return match.group(1)

    return None


def change_extension(filename, new_extension):
    """
    修改文件夹内文件的扩展名

    filename = 指定的文件

    new_extension = 新的扩展名
    """
    base_name = os.path.splitext(filename)[0]
    new_filename = f"{base_name}.{new_extension}"
    return new_filename


def batch_change_extension(folder_path, new_extension):
    """
    批量修改文件夹内文件的扩展名

    folder_path 文件夹路径

    new_extension 新扩展名
    """
    count = 0
    for folder_name, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            if not filename.endswith(new_extension):
                file_path = os.path.join(folder_name, filename)
                new_filename = change_extension(filename, new_extension)
                new_file_path = os.path.join(folder_name, new_filename)
                os.rename(file_path, new_file_path)
                count += 1
    return count
