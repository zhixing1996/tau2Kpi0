#!/usr/bin/env bash

# Main driver to submit command for tau- --> K-pi0
# Author Maoqiang Jing <jingmq@ihep.ac.cn>
# Created [2021-09-26 Sun 10:02]

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit command for tau- --> K- pi0\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%5-5s\n" "./analysis.sh [OPTION]"
    printf "\nOPTIONS\n"

    printf "\n\t%-9s  %-40s\n" "0.1"   "[Sumbit Projects, Reschedule Projects, Get DataSets]"
    printf "\n\t%-9s  %-40s\n" "0.1.1" "Sumbit Projects"
    printf "\n\t%-9s  %-40s\n" "0.1.2" "Reschedule Projects"
    printf "\n\t%-9s  %-40s\n" "0.1.3" "Get DataSets"

    printf "\n\t%-9s  %-40s\n" ""      ""
    printf "\n\n"
}

if [[ $# -eq 0 ]]; then
    usage
    echo "Please enter your option: "
    read option
else
    option=$1
fi

case $option in

    # ----------------------------------------
    #  0.1 Pretreatment of data and MC samples
    # ----------------------------------------

    0.1) echo "Sumbit Projects, Reschedule Projects, Get DataSets..."
         echo "--> Sample Type: data/mc"
         echo "--> Run Type: --dryrun/--force"
         echo "--> MC Projects: all(taupair/uubar-1/uubar-2/uubar-3/uubar-4/ddbar/ssbar/ccbar-1/ccbar-2/ccbar-3/ccbar-4/charged-1/charged-2/mixed-1/mixed-2)"
         echo "--> Run Parameters: ./attr/run_params.py"
         ;;

    0.1.1) echo "Sumbit Projects..."
           echo "which Sample Type do you want to submit?"
           read sample_type
           echo "which Run Type do you want to perform?"
           read run_type
           echo "which Project do you want to submit? (all/only one)"
           read project
           if [[ $project == "all" ]]
               then
               echo "now in all"  
               python tau2Kpi0.py --type $sample_type --gb2 project_sub --sub $run_type
           else
               echo "now in $project"  
               python tau2Kpi0.py --type $sample_type --gb2 project_sub $project --sub $run_type
           fi
           ;;

    0.1.2) echo "Reschedule Projects..."
           echo "which Sample Type do you want to reschedule?"
           read sample_type
           echo "which Project do you want to reschedule? (all/only one)"
           read project
           if [[ $project == "all" ]]
               then
               echo "now in all"  
               python tau2Kpi0.py --type $sample_type --gb2 project_reschedule
           else
               echo "now in $project"  
               python tau2Kpi0.py --type $sample_type --gb2 project_reschedule $project
           fi
           ;;

    0.1.3) echo "Get DataSets..."
           echo "which Sample Type do you want to get?"
           read sample_type
           echo "which DataSets do you want to get? (all/only one)"
           read project
           if [[ $project == "all" ]]
               then
               echo "now in all"  
               python tau2Kpi0.py --type $sample_type --gb2 ds_get 
           else
               echo "now in $project"  
               python tau2Kpi0.py --type $sample_type --gb2 ds_get $project
           fi
           ;;

esac
