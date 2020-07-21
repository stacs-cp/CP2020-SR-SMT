
model=$1
param=$2
seed=$3
config=fzn2omt-int-mathsat
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
        -flatzinc -fzn-bin fzn2optimathsat.py \
        -solver-options "--int-enc --random-seed $seed" 
    rm -f $outfilename.minion $outfilename.fzn $outfilename.mzn $outfilename.sat $outfilename.smt $outfilename.aux
fi
