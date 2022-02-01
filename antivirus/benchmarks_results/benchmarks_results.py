import argparse
from grovers import ga
from deutch_jozsa import dj
from bernstein_vazarani import bv
from vqe import vqe_pattern_matching
from qnn import qnn_pattern_matching



def copies_for_mal_type(mal_type):
    if (mal_type == 'M1'):
        return 8
    if (mal_type == 'M2'):
        return 8
    if (mal_type == 'M3'):
        return 4
    if (mal_type == 'M4'):
        return 6
    if (mal_type == 'M5'):
        return 65
    if (mal_type == 'M6'):
        return 65
    if (mal_type == 'M7'):
        return 65
    if (mal_type == 'M8'):
        return 65
    if (mal_type == 'M9'):
        return 2
    if (mal_type == 'M10'):
        return 1



def benchmarks_results(benchmark, is_mal):
    for i in range(1, 11):
        mal_type = "M"+str(i)
        if benchmark == 'ga':
            ga(mal_type, copies_for_mal_type(mal_type), is_mal)
        if benchmark == 'dj':
            dj("balanced", 2, mal_type, copies_for_mal_type(mal_type), is_mal)
        if benchmark == 'bv':
            bv("01", 2, mal_type, copies_for_mal_type(mal_type), is_mal)   
        if benchmark == 'vqe':
            vqe_pattern_matching('long', mal_type, copies_for_mal_type(mal_type), is_mal)
        if benchmark == 'qnn':
            qnn_pattern_matching('long', mal_type, copies_for_mal_type(mal_type), is_mal)



parser = argparse.ArgumentParser()
parser.add_argument('-b','--benchmark', type=str, required=True, help='Benchmark name')
parser.add_argument('-i','--is_mal', type=str, required=True, help='Whether create circuits with malicious circuits')
args = parser.parse_args()
is_mal = (args.is_mal == ("y" or "yes"))

benchmarks_results(args.benchmark, is_mal)


