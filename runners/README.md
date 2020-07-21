Scripts to launch the various configurations of SR-SMT

We previously used for each theory:

* QF\_LIA - Yices 2.6.1 (7th)
* QF\_IDL - Yices 2.6.1 (3rd - very close)
* QF\_BV - Boolector 3.1.0 (1st)
* QF\_NIA - Z3 4.8.7 (6th)

If we take into account the competition winners of [SMTCOMP-2019](https://smt-comp.github.io/2019/results.html),
and incorporate portfolios, we should use:

* QF\_LIA - [Par4](https://smt-comp.github.io/2019/participants/par4) or [SPASS-SATT](https://www.mpi-inf.mpg.de/departments/automation-of-logic/software/spass-workbench/) (depending if we consider portfolios)
* QF\_IDL - Z3
* QF\_BV - Boolector
* QF\_NIA - CVC4

Not including portfolios:

* QF\_LIA - [SPASS-SATT](https://www.mpi-inf.mpg.de/departments/automation-of-logic/software/spass-workbench/) -- A decent improvement on Yices
* QF\_IDL - Z3  -- Similar to Yices
* QF\_BV - Boolector
* QF\_NIA - CVC4  -- Miles better than Z3. 
