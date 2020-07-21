
import sys, json, math, csv
from os import listdir
from os.path import splitext
from pprint import pprint

seeds = [1,3,8]

configs = [ "sat"
          # , "chuffed"
          , "smt-bv-flat"
          , "smt-bv-nested"
          # , "smt-bv-nested-z3"
          # , "smt-bv-nested-z3-pairwisealldiff"
          , "smt-idl-flat"
          , "smt-idl-nested"
          , "smt-lia-flat"
          , "smt-lia-nested"
          , "smt-nia-flat"
          , "smt-nia-nested"
          # , "fzn2omt-bv-mathsat"
          # , "fzn2omt-bv-z3"
          # , "fzn2omt-int-mathsat"
          # , "fzn2omt-int-z3"
          ]


with open("results/combinedInfo.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    headers = next(reader, None)
    allInfos = []
    for row in reader:
        info = {}
        for i, h in enumerate(headers):
            info[h] = row[i]
        allInfos.append(info)

def transpose(l):
    out = {}
    for x in l:
        for k, v in x.items():
            if not k in out.keys():
                out[k] = []
            out[k].append(v)
    return out

with open("results/clauseRatios.csv", "w") as f:
    clauseRatios = {}
    for info in allInfos:
        key = (info["problem"], info["instance"])
        if not key in clauseRatios.keys():
            clauseRatios[key] = {}
            for c in configs:
                clauseRatios[key][c] = "NA"
        if info["SATClauses"] != "NA":
            clauseRatios[key][info["configuration"]] = info["SATClauses"]

    print(",".join(["problem", "instance"]
                        + configs
                        + ["%s ratio to SAT" % c for c in configs]), file=f)
    ratioToSATList = []
    for (problem, instance), instanceData in clauseRatios.items():
        # print(problem, instance, instanceData)
        for c in configs:
            if c in instanceData.keys():
                pass
            else:
                pass
                # print("Missing %s in %s" % (c, instanceData))
                # print("runners/savilerow-%s.sh data/problems/%s/%s.eprime data/problems/%s/%s.param 1" % (c, problem, problem, problem, instance))
        ratioToSAT = {}
        for c in configs:
            ratioToSAT[c] = "NA"
            if c in instanceData.keys() and instanceData[c] != "NA" and "sat" in instanceData.keys() and instanceData["sat"] != "NA":
                ratioToSAT[c] = str(float(instanceData[c]) / float(instanceData["sat"]))
        print(",".join([problem, instance]
                            + [ instanceData[c] for c in configs ]
                            + [ ratioToSAT[c] for c in configs ]),file=f)
        ratioToSATList.append(ratioToSAT)

    ratioToSATList = transpose(ratioToSATList)
    # pprint(ratioToSATList)
    print("\t".join(["config", "median", "mean", "min", "max"]))
    for k, values in ratioToSATList.items():
        if k == "sat": continue
        valuesInt = [float(x) for x in values if x != "NA"]
        median = sorted(valuesInt)[round(len(valuesInt)/2)]
        mean = sum(valuesInt) / len(valuesInt)
        print("\t".join([ "%-20s" % k
                        , "%8.4f" % (100 * median)
                        , "%8.4f" % (100 * mean)
                        , "%8.4f" % (100 * min(valuesInt))
                        , "%8.4f" % (100 * max(valuesInt))
                        ]))
