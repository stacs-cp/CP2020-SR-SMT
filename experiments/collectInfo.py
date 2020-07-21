
import sys, json, math
from os import listdir
from os.path import splitext
from pprint import pprint

seeds = [1,3,8]

configs = [ "sat"
          , "chuffed"
          , "smt-bv-flat"
          , "smt-bv-nested"
          , "smt-bv-nested-z3"
          , "smt-bv-nested-z3-pairwisealldiff"
          , "smt-idl-flat"
          , "smt-idl-nested"
          , "smt-lia-flat"
          , "smt-lia-nested"
          , "smt-nia-flat"
          , "smt-nia-nested"
          , "fzn2omt-bv-mathsat"
          , "fzn2omt-bv-z3"
          , "fzn2omt-int-mathsat"
          , "fzn2omt-int-z3"
          ]


def readInfo(path):
    info = {}
    nblines = 0
    with open(path) as f:
        for line in f:
            nblines += 1
            if line.strip() == "Timeout":
                return { "ExitCode": "Timeout"
                       , "SolverTotalTime" : "3600"
                       , "SavileRowTotalTime": "3600"
                       }
            if line.strip() == "OutOfMemory":
                return { "ExitCode": "OutOfMemory"
                       , "SolverTotalTime" : "3600"
                       , "SavileRowTotalTime": "3600"
                       }
            try:
                [key, value] = line.strip().split(":")
                info[key] = value
            except:
                print("Warning: %s" % line)
        info["ExitCode"] = "Success"
    if nblines == 0:
        print("Warning, empty info file: %s" % path, file=sys.stderr)
        return None
    if not "SolverTotalTime" in info.keys():
        # if not "fzn2omt" in path:
        # print("Warning, no SolverTotalTime: %s" % path)
        info["SolverTotalTime"] = "3600"
        return info
    if not "SavileRowTotalTime" in info.keys():
        # if not "fzn2omt" in path:
        # print("Warning, no SavileRowTotalTime: %s" % path)
        info["SavileRowTotalTime"] = "3600"
        return info
    return info


allKeys = set()
allInfos = []
for problemClass in listdir("data/problems"):
    models = []
    params = []
    for path in listdir("data/problems/%s" % problemClass):
        if path.endswith(".eprime"):
            models.append("data/problems/%s/%s" % (problemClass, path))
        if path.endswith(".param"):
            params.append("data/problems/%s/%s" % (problemClass, path))
    for model in models:
        for param in params:
            for seed in seeds:
                for config in configs:
                    infoFilePath = "%s-%s-%s.info" % (param, config, seed)
                    try:
                        info = readInfo(infoFilePath)
                        if info != None:
                            # add some more info
                            info["problem"] = problemClass
                            info["configuration"] = config
                            # drop prefix and the .param exteension
                            prefixLen = len("data/problems/%s/" % problemClass)
                            info["instance"] = param[prefixLen:][:-6]
                            info["seed"] = str(seed)
                            allKeys = allKeys.union(info.keys())
                            allInfos.append(info)
                    except FileNotFoundError:
                        # print("FileNotFoundError", infoFilePath)
                        pass

with open("results/combinedInfo.csv", "w") as f:
    allKeys = sorted(allKeys)
    print(",".join(allKeys), file=f)
    for info in allInfos:
        print(",".join([info[k] if k in info.keys() else "NA" for k in allKeys]), file=f)

def median(xs):
    if len(xs) == 0:
        print("median of empty list")
        return 0
    return sorted(xs)[math.floor(len(xs)/2)]

with open("results/allData.csv", "w") as f:
    allData = {}
    for info in allInfos:
        key = (info["problem"], info["instance"], info["configuration"])
        if not key in allData.keys():
            allData[key] = []
        allData[key].append(info)

    outputLines = {} # indexed by instance
    allDataFields = set()
    for (problem, instance, configuration), infos in allData.items():
        SolverTime = median([float(info["SolverTotalTime"]) for info in infos])
        SavileRowTime = median([float(info["SavileRowTotalTime"]) for info in infos])
        TotalTime = SolverTime + SavileRowTime
        if TotalTime >= 3600: TotalTime = 3600  
        key = "%s--%s" % (problem, instance)
        if not key in outputLines.keys():
            outputLines[key] = {}
        outputLines[key]["%s-SolverTime" % configuration] = "%.2f" % SolverTime
        outputLines[key]["%s-SavileRowTime" % configuration] = "%.2f" % SavileRowTime
        outputLines[key]["%s-TotalTime" % configuration] = "%.2f" % TotalTime
        allDataFields.add("%s-SolverTime" % configuration)
        allDataFields.add("%s-SavileRowTime" % configuration)
        allDataFields.add("%s-TotalTime" % configuration)
        # print(info)

    allDataFields = sorted(allDataFields)
    print(",".join(["instance"] + allDataFields), file=f)
    for instance, instanceData in outputLines.items():
        print(",".join([instance] + [instanceData[key] if key in instanceData.keys() else "3600" for key in allDataFields]), file=f)
