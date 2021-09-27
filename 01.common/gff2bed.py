# !/usr/bin/env/python3
# -*- coding:UTF-8 -*-
"""
===================================================
@author:ZhengJiangmin
@desc:conver gff to bed file
@date:2021-09-27 19:07:47
@Email:zhengjiangmin@mail.nwpu.edu.cn
@Blog:https://www.cnblogs.com/zhengjm/
Editor:vscode
===================================================
"""
from sys import argv
import sys
import os
import re

if len(argv) < 3:
    print("Usage: python3 {} {} {}".format(argv[0], "gff_file", "output_file"))
    sys.exit()


def main():
    back_list = []
    with open(file=argv[1]) as input:
        lines = input.readlines()
        for line in lines:
            info = line.split('\t')
            if len(info) < 3:
                continue
            if info[2] == "gene":
                gene_name = re.match(r'ID=gene:(\w+);', info[8]).group(1)
                back_str = '\t'.join(
                    [info[0], info[3], info[4], gene_name]) + '\n'
                back_list.append(back_str)
                print(back_str)
    with open(file=argv[2], mode='w') as output:
        output.writelines(back_list)


if __name__ == "__main__":
    main()
