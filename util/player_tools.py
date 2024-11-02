#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/11/2 10:18
@FILENAME: player_tools
"""



# 根据分数值排序，并加上序号
def sort_list(init_dict):
    if not init_dict:
        return []
    ordered_list = sorted([{'name': key, 'score': init_dict[key]} for key in init_dict.keys()],
                        key=lambda x: x['score'], reverse=True)
    for i, item in enumerate(ordered_list):
        item['index'] = i+1

    return ordered_list