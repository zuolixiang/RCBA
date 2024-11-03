#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/11/2 10:18
@FILENAME: player_tools
"""



# 根据分数值排序，并加上序号
def sort_list(init_dict, flag):
    """
    :param init_dict:
    :param flag:  标记是否需要做百分号处理
    :return:
    """
    if not init_dict:
        return []
    ordered_list = sorted([{'name': key, 'score': init_dict[key]} for key in init_dict.keys()],
                        key=lambda x: x['score'], reverse=True)
    if flag:
        ordered_list = [{'name': item['name'], 'score': f"{item['score'] * 100:.1f}%"} for item in ordered_list]

    for i, item in enumerate(ordered_list):
        item['index'] = i+1

    return ordered_list


def format_dict(init_dict, formatted_dict):
    if not init_dict:
        return {}
    for p in init_dict:
        if init_dict[p][0] == 0:
            formatted_dict[p] = 0.0
            # formatted_dict[p] = "0.0%"
        else:
            rate = init_dict[p][1] / init_dict[p][0]
            # formatted_dict[p] = f"{rate * 100:.1f}%"
            formatted_dict[p] = rate
    return formatted_dict