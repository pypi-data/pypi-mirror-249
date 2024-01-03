import os
import sys
import eyed3
from mutagen.flac import FLAC


def get_audio_files(folder, extension=[".mp3", ".flac"]):
    "根据扩展获取指定文件夹中的所有音频文件"
    audio_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extension):
                audio_files.append(os.path.join(root, file))
    return audio_files


def update_audio_metadata(file_path):
    "更新音频文件的标题"
    _, extension = os.path.splitext(file_path)

    try:
        if extension.lower() == ".mp3":
            # 更新MP3文件的元数据
            audio = eyed3.load(file_path)
            if audio.tag:
                filename = os.path.splitext(os.path.basename(file_path))[0]
                audio.tag.title = filename
                audio.tag.save(version=eyed3.id3.ID3_V2_3)  # 强制设置为 ID3 v2.3
                print(f"已更新 {file_path} 的元数据")
        elif extension.lower() == ".flac":
            # 更新FLAC文件的元数据
            audio = FLAC(file_path)
            if audio:
                filename = os.path.splitext(os.path.basename(file_path))[0]
                audio["title"] = filename
                audio.save()
                print(f"已更新 {file_path} 的元数据")
        else:
            print(f"不支持的格式或无法解析的文件: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")
        raise  # 重新引发异常，终止脚本执行


def id_to_intid(id):
    "文件编号转文件编号id"
    intid = "".join(filter(str.isnumeric, id))
    return int(intid)


def intid_to_id(intid):
    "文件编号id转文件编号"
    intid = "".join(filter(str.isnumeric, intid))
    id = int(intid)
    if 1000000 < id < 10000000:
        return f"0{id}"
    else:
        if id == 0:
            return "00"
        else:
            return int(id)
