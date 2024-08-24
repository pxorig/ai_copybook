# -*- coding: utf-8 -*-
import os

def get_list(path: str="") -> list:
    ttfs = []
    for t in os.listdir(path):
        if ".ttf" in t:
            data = t.replace(".ttf", "")
            ttfs.append(data)
    return ttfs