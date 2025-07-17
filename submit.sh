#!/bin/bash
#SBATCH --mem 232G
#SBATCH --cpus-per-task 8
#SBATCH --job-name=pi0_update
#SBATCH --error=error_pi0_update2.%a.log
#SBATCH --output=pi0_update2.%a.log
#SBATCH --open-mode append

# Here, do the real work:
python3 /home/judad/update2zero/tau_pi0_plt_hist_new_update2.py



