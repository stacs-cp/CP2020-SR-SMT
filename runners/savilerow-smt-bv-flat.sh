# solver boolector

model=$1
param=$2
seed=$3
config=smt-bv-flat
outfilename=$param-$config-$seed

if [ -f $outfilename.info ]; then
    echo "Skipping $outfilename.info"
else
    savilerow $model $param -run-solver \
        -timelimit 3600 \
        -out-minion $outfilename.minion \
        -out-gecode $outfilename.fzn \
        -out-chuffed $outfilename.fzn \
        -out-minizinc $outfilename.mzn \
        -out-sat $outfilename.sat \
        -out-smt $outfilename.smt \
        -out-solution $outfilename.solution \
        -out-info $outfilename.info \
        -out-aux $outfilename.aux \
        -smt -smt-seed $seed \
        -boolector-bin boolector -z3-bin z3 -yices-bin yices-smt2 \
        -smt-bv -smt-flat -solver-options "--time=3600"
    rm -f $outfilename.minion $outfilename.fzn $outfilename.mzn $outfilename.sat $outfilename.smt $outfilename.aux
fi
