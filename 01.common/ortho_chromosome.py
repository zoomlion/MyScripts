# !/usr/bin/env/python3
# -*- coding:UTF-8 -*-
"""
===================================================
@author:ZhengJiangmin
@desc:find chromosome(also works for scaffolds) orthologues. e.g. 1-22
@date:2021-08-10 22:04:58
@Email:zhengjiangmin@mail.nwpu.edu.cn
@Blog:https://www.cnblogs.com/zhengjm/
Editor:vscode
===================================================
"""


import re
import argparse
import time


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-blastp_first', "--input_first_blastp", type=str,
                        required=True, help="first blastp result")
    parser.add_argument('-blastp_second', "--input_second_blastp",
                        type=str, required=True, help="second blastp result")
    # parser.add_argument('-')
    parser.add_argument('-gff_first', "--input_first_gff", type=str,
                        required=True, help="first species' gff annotation")
    parser.add_argument('-gff_second', "--input_second_gff", type=str,
                        required=True, help="second species' gff annotation")
    parser.add_argument('--Usage', required=False,
                        help="Usage: follow the instruction, if doesnt work, switch the order of gff")
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
        if hits1[hit] in hits2 and hit == hits2[hits1[hit]]:  # key condition
            output.append('\t'.join([hit, hits1[hit]]))
    return output


def fetch_chr_pos(filename):
    gene_pos = {}
    with open(filename) as file:
        for line in file.readlines():
            splits = line.split('\t')
            # standard gff3 file from ensembl site
            if len(splits) > 8 and splits[2] == 'mRNA':
                try:
                    gene_pos[re.match(r'ID=transcript:(\w+)',
                                      splits[8]).group(1)] = splits[0]
                except:
                    print("Change regular expression to match you gff file")
    return gene_pos


def main():
    parser = get_parser()
    args = parser.parse_args()
    blastp1, blastp2 = args.input_first_blastp, args.input_second_blastp
    rbhs = [item.split('\t')
            for item in fetch_rbh(blastp1, blastp2)]
    # print(rbhs)
    gene_pos1 = fetch_chr_pos(args.input_first_gff)
    gene_pos2 = fetch_chr_pos(args.input_second_gff)
    # print(gene_pos1)
    chr_map = []
    for record in rbhs:
        try:
            chr_map.append(gene_pos1[record[0]] + '\t' + gene_pos2[record[1]])
        except KeyError:
            print("Maybe you should switch the order of gff file")
            return 1
        # try:
        #     chr_map.append(gene_pos1[record[0]], gene_pos2[record[1]])
        # except:
        #     pass
    # print(chr_map)
    # print(set(chr_map))
    print('{}\t{}\tCount'.format(args.input_first_gff, args.input_second_gff))
    count = 10
    for item in set(chr_map):
        print('{}\t{}'.format(item, chr_map.count(item)))
        count -= 1
        if count < 0:
            break
    print(".............More.............")
    with open("ortho_chr.out", mode='w+') as output:
        output.writelines('{}\t{}\tCount\n'.format(args.input_first_gff, args.input_second_gff))
        for item in set(chr_map):
            if chr_map.count(item) > 10: # here is the threshold
                output.writelines('{}\t{}\n'.format(item, chr_map.count(item)))

if __name__ == "__main__":
    main()
    print("Elapsed time:\t{}".format(time.perf_counter()))
