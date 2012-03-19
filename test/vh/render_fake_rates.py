#!/usr/bin/env python
'''

Render the measured and fitted fake rates from a RooWorkspace

Author: Evan K. Friis, UW

'''


from RecoLuminosity.LumiDB import argparse
import logging
import os
import re
import sys
# Need to generate dictionaries
import FinalStateAnalysis.Utilities.RooFitTools as roofit
# Steal the args so ROOT doesn't mess them up!
parser = argparse.ArgumentParser()
args = sys.argv[:]
sys.argv = []

from rootpy.io import open
import ROOT

if __name__ == "__main__":
    log = logging.getLogger("render_fake_rates")
    logging.basicConfig(level=logging.DEBUG)

    parser.add_argument('input', help='Input file w/ fit results RooWorkspace')
    parser.add_argument('output', help='Output directory to store plots in')

    args = parser.parse_args(args[1:])

    log.info("Opening input file %s", args.input)

    file = open(args.input)

    log.info("Getting workspace")
    ws = file.Get("fit_results")

    x = ws.var('x')
    cut = ws.cat('cut')

    # Put everything in python form
    data = {}
    fake_rate_datas = ws.allData()
    # Plot the results of each one
    for datum in fake_rate_datas:
        data[datum.GetName()] = datum
        print datum

    functions = {}
    # We need to unmangle the function names
    name_extractor = re.compile('func_(?P<name>.*)')
    for function in roofit.iter_collection(ws.allFunctions()):
        function_name = function.GetName()
        print function_name
        match = name_extractor.match(function_name)
        if not match:
            continue
        functions[match.group('name')] = function

    fit_results = {}

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

    keeps = []
    frame = x.frame()
    ROOT.SetOwnership(frame,False)
    for data_name, data_info in data.iteritems():
        frame = x.frame()
        data_info.plotOn(frame, ROOT.RooFit.Efficiency(cut))
        function = functions[data_name]
        function.plotOn(frame)
        frame.Draw()
        canvas.SetLogy(True)
        frame.SetMinimum(1e-4)
        frame.SetMaximum(1)
        canvas.SaveAs(os.path.join(args.output, data_name + '.pdf'))
