
import sys, json
from os import listdir
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
                    print("runners/savilerow-%s.sh %s %s %d" % (config, model, param, seed))
