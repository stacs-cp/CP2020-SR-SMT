
model=$1
param=$2
seed=$3
config=chuffed
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
        -out-solution $outfilename.solution \
        -out-info $outfilename.info \
        -out-aux $outfilename.aux \
        -chuffed -solver-options "--rnd-seed $seed --time-out 3600000"
    rm -f $outfilename.minion $outfilename.fzn $outfilename.mzn $outfilename.sat $outfilename.smt $outfilename.aux
fi
