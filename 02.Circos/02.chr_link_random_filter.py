# !/usr/bin/env/python3
# -*- coding:UTF-8 -*-
"""
===================================================
@author:ZhengJiangmin
@desc:filter the chromosome file and link file for Circos input
@date:2021-10-02 16:04:44
@Email:zhengjiangmin@mail.nwpu.edu.cn
@Blog:https://www.cnblogs.com/zhengjm/
Editor:vscode
===================================================
"""


import os
import time
import sys
import re


chr_file = "./Ca.BMC.maf.chromosome.txt"
link_file = "./Ca.BMC.maf.link.txt"
chr_cast_floor = 50000
chr_names = []  # all chr/scaffold names emerged
chr_cast = []

# chr filter partition, all chr over thres will be eliminated
with open(chr_file, mode='r') as input:
    lines = input.readlines()
    for line in lines:
        if int(line.split()[5]) > chr_cast_floor:
            chr_cast.append(line)
    with open(chr_file + ".new", mode='w') as output:
        output.writelines(chr_cast)


for ele in chr_cast:
    chr_names.append(ele.split()[2])


# filter link file
with open(link_file) as input:
    link_out = []
    single_lines = input.readlines()
    lines = [single_lines[2*i] + single_lines[2*i+1]
             for i in range(len(single_lines)//2)]
    for line in lines:
        print(line)
        sign1 = False
        sign2 = False
        # for ele in chr_names:
        #     if ele in line.split('\n')[0].split()[1]:
        #         sign1 = True
        # for ele in chr_names:
        #     if ele in line.split('\n')[1].split()[1]:
        #         sign2 = True
        if line.split('\n')[0].split()[1] in chr_names and line.split('\n')[1].\
                split()[1] in chr_names:
            link_out.append(line)
        # if sign1 and sign2:
        #     link_out.append(line)

    with open(link_file + ".new", mode='w') as output:
        output.writelines(link_out)


# randomnize the link file?


print(time.perf_counter())
