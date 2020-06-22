#!/bin/bash
echo "=========Printing Singularity version========="
singularity --version

echo "==========Printing ram size================="
vmstat -s
echo "=========using free command=================="
free -g


/bin/date
echo "Extracting Process Monitor - This is to monitor the processes that we will run"
mkdir -p prmon && tar xf prmon_1.0.1_x86_64-static-gnu72-opt.tar.gz -C prmon --strip-components 1

echo "Running prmon"
./prmon/bin/prmon -p $$ -i 10 &

echo "Let's see in what path are we"
echo $PWD

echo "Let's see what's in here"
ls -lah

echo "Let's see how many processors our machine has"
lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('

echo "Lets create a tmp folder to keep temporal files"
mkdir -p tmp

echo "Let's see what in here again!"
ls -lah

echo "Ok! Let's run the container"
rm -rf .singularity

echo "The image is in /cvmfs/sw.skatelescope.eu/images/MeerKAT.simg"

#singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C /cvmfs/sw.skatelescope.eu/images/MeerKAT.simg wsclean -help
#echo "extracting data"
#time
#tar -xzvf 1491550051.tar.gz
#echo "data set successfully extracted"

tar -xzvf cal_scripts.tar.gz

echo "executing validate_input on data"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/validate_input.py --config myconfig.txt
#time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/validate_input.py --config myconfig.txt

echo "partitioning input data using partition.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/partition.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/partition.py --config myconfig.txt

echo "calculating reference antenna using calc_refant.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/calc_refant.py --config myconfig.txt
time
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/calc_refant.py --config myconfig.txt

echo "running flag_round_1.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/flag_round_1.py --config myconfig.txt
time
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/flag_round_1.py --config myconfig.txt

echo "running setjy.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/setjy.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/setjy.py --config myconfig.txt

echo "running xx_yy_solve.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/xx_yy_solve.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/xx_yy_solve.py --config myconfig.txt

echo "running xx_yy_apply.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/xx_yy_apply.py --config myconfig.txt
time
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/xx_yy_apply.py --config myconfig.txt

echo "running flag_round_2.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/flag_round_2.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/flag_round_2.py --config myconfig.txt

echo "running setjy.py second time"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/setjy.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/setjy.py --config myconfig.txt

echo "running xy_yx_solve.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/xy_yx_solve.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/xy_yx_solve.py --config myconfig.txt

echo "running xy_yx_apply.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/xy_yx_apply.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/xy_yx_apply.py --config myconfig.txt

echo "running split.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa -c cal_scripts/split.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa -c cal_scripts/split.py --config myconfig.txt

echo "running quick_tclean.py"
singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg mpicasa -n 3 casa -c cal_scripts/quick_tclean.py --config myconfig.txt
time 
#singularity exec --cleanenv -H $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg mpicasa -n 17 casa -c cal_scripts/quick_tclean.py --config myconfig.txt

echo "running plot_solutions.py"
singularity exec -B $PWD -B cal_scripts/ -B data/1491550051.ms/ casameer-5.4.1.xvfb.simg casa --nogui --log2term -c cal_scripts/plot_solutions.py --config myconfig.txt
time 
#singularity exec -B $PWD -B cal_scripts/ -B data/1491550051.ms/ /cvmfs/sw.skatelescope.eu/images/meerkat.simg casa --nogui --log2term -c cal_scripts/plot_solutions.py --config myconfig.txt

echo "renaming prmon file"
mv prmon.txt prmon_validate_partition_$1.txt

tar -czvf outputMMS_$1.tar.gz *mms*

cp myconfig.txt myconfig_$1.txt

time 
tar -czvf images_$1.tar.gz images
time 
tar -czvf plots_$1.tar.gz plots
echo "Listing all contents"
ls -lah
