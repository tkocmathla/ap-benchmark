import random

import micronap.sdk as ap

import settings
import utils


class BenchmarkMacroDef(object):
    def __init__(self, anml, name, args):
        self.anml = anml
        self.name = name
        self.args = args

        self.inst = None
        self.chain = []
        self.init()

    def init(self):
        self.inst = self.anml.CreateMacroDef(anmlId=self.name)
        self.chain = utils.ste_chain(self.inst, '*' * self.args.macro_ste_count, head_props={'startType': ap.AnmlDefs.ALL_INPUT}, tail_props={'match': True})
        self.parameterize_stes()
        self.compile()

    def parameterize_stes(self):
        for i, ste in enumerate(self.chain):
            self.inst.AddMacroParam('%p{}'.format(i), ste)

    def assign_edges(self):
        taken = set()
        for _ in xrange(self.args.macro_edge_count):
            src_idx = random.randint(0, len(self.chain)-1)
            dst_idx = random.randint(0, len(self.chain)-1)
            while src_idx == dst_idx or src_idx == dst_idx-1 or (src_idx, dst_idx) in taken:
                dst_idx = random.randint(0, len(self.chain)-1)
            self.inst.AddAnmlEdge(self.chain[src_idx], self.chain[dst_idx])
            taken.add((src_idx, dst_idx))

    def compile(self):
        self.inst.SetMacroDefToBeCompiled()
        

class BenchmarkMacroRef(object):
    def __init__(self, mdef, network, name, args):
        self.mdef = mdef
        self.network = network
        self.name = name
        self.args = args

        self.inst = self.network.AddMacroRef(self.mdef.inst, anmlId=self.name)

    def rand_char(self):
        return '\\x{:02x}'.format(random.choice(xrange(settings.STE_BITS)))

    def rand_label(self):
        return ''.join([self.rand_char() for _ in xrange(self.args.label_set_size)])

    def assign_labels(self):
        for i in xrange(len(self.mdef.chain)):
            param = self.mdef.inst.GetMacroParamFromName('%p{}'.format(i))
            subs = self.mdef.inst.GetMacroParamSubstitutionHolder(param)
            subs.ste.new_symbols = '[{}]'.format(self.rand_label())
            self.network.SetMacroParamSubstitution(self.inst, subs)

