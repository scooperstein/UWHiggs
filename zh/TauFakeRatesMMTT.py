'''
Base analyzer for hadronic tau fake-rate estimation: Z->mu mu
'''

import TauFakeRatesBase
import baseSelections as selections
from MuMuTauTauTree import MuMuTauTauTree


class TauFakeRatesMMTT(TauFakeRatesBase.TauFakeRatesBase):
    tree = 'mmtt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(TauFakeRatesMMTT, self).__init__(tree, outfile, MuMuTauTauTree, **kwargs)
        
    def zSelection(self, row):
        if not selections.ZMuMuSelection(row): return False
        if not selections.generalCuts(row, 'm1','m2','t1','t2'): return False
        if not selections.looseTauSelection(row, 't1'): return False
        if not selections.looseTauSelection(row, 't2'): return False
        if (row.t1Pt + row.t2Pt < 50): return False
        if not bool(row.t1AntiMuonLoose2): return False
        if not bool(row.t1AntiElectronLoose): return False
        if not bool(row.t2AntiMuonLoose2): return False
        if not bool(row.t2AntiElectronLoose): return False
        return True


       
