# !/usr/bin/env/python3
# -*- coding:UTF-8 -*-
"""
===================================================
@author:ZhengJiangmin
@desc:get rbh(reciprocal best hit) from the results of diamond blastp
@date:2021-08-10 18:45:07
@Email:zhengjiangmin@mail.nwpu.edu.cn
@Blog:https://www.cnblogs.com/zhengjm/
Editor:vscode
===================================================
"""


import argparse
import re


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i_first', '--input_first', type=str,
                        required=True, help="one of blastp result")
    parser.add_argument('-i_second', '--input_second', type=str,
                        required=True, help="the other of balstp result")
    parser.add_argument('-gff_first', '--gff_first', type=str,
                        required=False, help="the gff annotation of first species")
    parser.add_argument('-gff_second', '--gff_second', type=str,
                        required=False, help="the gff annotation of second species")
    return parser


def fetch_hits(filename):
    hits = {}
    with open(filename) as file:
        for line in file.readlines()[:: -1]:
            # reverse it to avoid "-k 2,3,4,or more"
            hits[re.match(r'^(\w+)\t(\w+)\s', line).group(1)
                 ] = re.match(r'^(\w+)\t(\w+)\s', line).group(2)
    return hits


def fetch_rbh(input1, input2):
    # input1 and input2 are two blastp results from diamond blastp
    # Caution: use "-k 1" to pick up the best hit
    hits1 = fetch_hits(input1)
    hits2 = fetch_hits(input2)
    output = []
    for hit in hits1:
        if hits1[hit] in hits2:  # key condition
            output.append('\t'.join([hit, hits1[hit]]))
    return output


def main():

    parser = get_parser()
    args = parser.parse_args()
    input1, input2 = args.input_first, args.input_second
    output = fetch_rbh(input1, input2)
    with open('rbh.tsv', mode='w') as file:
        file.writelines('\n'.join(output) + '\n')

    if args.gff_first is not None and args.gff_second is not None:
        transcripts_first, transcripts_second = {}, {}
        with open(args.gff_first) as gff_first:
            lines = gff_first.readlines()
            for line in lines:
                key = re.match(r'^[^\n]+ID=transcript:(\w+)', line)
                result = re.match(r'(^[\w\.]+)\t\w+\tmRNA\t(\w+)\t(\w+)', line)
                if key and result:
                    transcripts_first[key.group(1)] = \
                        [result.group(1), result.group(2), result.group(3)]
        with open(args.gff_second) as gff_second:
            lines = gff_second.readlines()
            for line in lines:
                key = re.match(r'^[^\n]+ID=transcript:(\w+)', line)
                result = re.match(r'(^[\w\.]+)\t\w+\tmRNA\t(\w+)\t(\w+)', line)
                if key and result:
                    transcripts_second[key.group(1)] = \
                        [result.group(1), result.group(2), result.group(3)]
    else:
        return 0
    loci = []
    for item in output:
        if item.split('\t')[0] in transcripts_first:
            loci.append(item.split('\t')[
                        0] + '\t' + '\t'.join(transcripts_first[item.split('\t')[0]]) + '\t')
        if item.split('\t')[1] in transcripts_second:
            loci.append(item.split('\t')[
                        1] + '\t' + '\t'.join(transcripts_second[item.split('\t')[1]]) + '\n')
    for item in loci:
        print(item)
    with open("rbh_loci.tsv", mode='w') as file:
        file.writelines(loci)
    print("Caution: If not output with site info, try to switch the order of gff")
    return 0


if __name__ == '__main__':
    main()
