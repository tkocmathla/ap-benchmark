from argparse import ArgumentParser 
import os
import random
import time

import micronap.sdk as ap

import settings
from macros import BenchmarkMacroDef, BenchmarkMacroRef


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    parser.add_argument('--label-set-size', '-l', type=int, default=settings.STE_BITS/2)
    parser.add_argument('--macro-edge-count', '-e', type=int, default=settings.ROW_ROUTES/2)
    parser.add_argument('--macro-ste-count', '-s', type=int, default=settings.STE_PER_ROW-1)
    parser.add_argument('--macro-count', '-c', type=int, default=1)
    parser.add_argument('--random-seed', '-r', type=int, default=time.time())
    return parser.parse_args()

def main():
    args = parse_args()
    random.seed(args.random_seed)
    if (not os.path.isdir(settings.ANML_PATH)): os.makedirs(settings.ANML_PATH)
    if (not os.path.isdir(settings.FSM_PATH)): os.makedirs(settings.FSM_PATH)

    anml = ap.Anml()
    network = anml.CreateAutomataNetwork('{}_network'.format(settings.NAME))
    
    # TODO: replace macro_count param with "total utilization" param and tesselate
    #       macro instances to fill the desired space
    for i in xrange(args.macro_count):
        mdef = BenchmarkMacroDef(anml, 'mdef{}'.format(i), args)
        mdef.assign_edges()
        mref = BenchmarkMacroRef(mdef, network, 'mref{}'.format(i), args)
        mref.assign_labels()

    network.ExportAnml('{}/{}.anml'.format(settings.ANML_PATH, settings.NAME))
    opts = ap.CompileDefs.AP_OPT_MT
    if args.verbose: opts |= ap.CompileDefs.AP_OPT_SHOW_DEBUG
    anml.CompileMacros(options=opts)
    fsm, _ = anml.CompileAnml(options=opts)
    fsm.Save('{}/{}.fsm'.format(settings.FSM_PATH, settings.NAME))


if __name__ == '__main__':
    main()
