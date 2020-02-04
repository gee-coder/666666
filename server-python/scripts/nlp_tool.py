# Author: Acer Zhang
# Datetime:2020/1/29 22:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from typing import List

from os_tool import generate_json_file


def add_separator_in_words(words: List[str]) -> str:
    """
    为分词数据增加分隔符
    :param words:List[str] 输入数据
    :return:str 分割后字符串数据

    Example:
    '今天|天气|怎么样' = add_separator_in_list(['今天', '天气', '怎么样'])
    """
    container = "|".join(words).replace("|\n", "")
    return container


def keyword2label_mask(keyword_data: List[str], server: classmethod):
    """
    关键字转标签
    :param keyword_data: 关键字数据
    :param server: 转换关键字方法
    :return: label_data:List[str], mask_data:List[str] 标签数据, 蒙版数据

    Example:
    from sentence2words import server
    input: keyword2label(["今天 天气很好 赞", "今天 天气很好 赞"], server)
    output: ([['今天', '天气', '很好', '赞'], ['今天', '天气', '很好', '赞']], [[2, 1, 1, 2], [2, 1, 1, 2]])
    """
    label_data = []
    mask_data = []
    for keywords in keyword_data:
        keywords = keywords.split(" ")
        labels = []
        masks = []
        for keyword in keywords:
            tmp = server([keyword])[0][0].split("|")
            labels += tmp
            masks += [1] * len(tmp) if len(tmp) != 1 else [2]
        label_data.append(labels)
        mask_data.append(masks)
    return label_data, mask_data


def generate_index(all_data: list, save_index_file_path: str = None, file_name: str = "index"):
    """
    数据索引制作
    :param all_data:list 完整数据
    :param save_index_file_path:str 数据保存位置
    :param file_name:str 保存的文件名

    Example:
    input: generate_index([2, 3, 4])
    output: {2: 0, 3: 1, 4: 2}
    """
    index_dict = {}
    max_index = 0
    for sample in all_data:
        if sample not in index_dict:
            index_dict[sample] = max_index
            max_index += 1

    if save_index_file_path:
        generate_json_file(index_dict, save_index_file_path, file_name=file_name)
    return index_dict


def generate_index_in_data(data_file, save_index_path):
    """
    从分词完毕的数据文件中制作索引
    :param data_file: 数据文件
    :param save_index_path: 保存路径
    """
    with open(data_file, "r", encoding="utf-8") as f:
        a = f.read().replace("\n", "|").split("|")
        generate_index(a, save_index_file_path=save_index_path)


# generate_index_in_data(r"D:\a13\server-python\example_data\words.csv", r"D:\a13\server-python\example_data")


def transform_data2id(data: list, data_dict: dict):
    """
    转换数据为对应数字索引号
    :param data: list 原始数据
    :param data_dict: dict 索引字典
    :return: 转换后的数据
    """
    container = []
    for samples in data:
        samples = samples.split("|")
        for sample in samples:
            container.append(data_dict[sample])
    return container


def transform_id2data(data_id: list, data_dict: dict):
    """
    转换索引号为对应数据
    :param data_id: list id数据
    :param data_dict: dict 索引字典
    :return: 转换后的数据
    """
    tmp_dict = dict(zip(data_dict.values(), data_dict.keys()))
    container = []
    for sample in data_id:
        container.append(tmp_dict[sample])
    return container
