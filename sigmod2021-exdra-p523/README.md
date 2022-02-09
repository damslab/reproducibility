
# ExDRA paper Reproducibility

Hi !

This is the reproducibility repository of the ExDRA paper in SIGMOD Industrial track 2021.
To make this run there is a few setup requirements to address first.

It is expected that anyone who try to reproduce the results have access to multiple (Linux) machines
(we used 7 for the paper submission) all with the following installed:
The machines are close to m5a.8xlarge in aws, adding the storage requirement
use m5ad.8xlarge for the main node.
Also your local laptop have to have at least 32GB ram, if this is not available, then launch a node on another geographically different location,
the laptop used for the experiments had 16 vCPU. A m5ad.4xlarge fits the requirements.

All machines:

- Java 8
- Maven 3.6+
- git (i guess you already have this if you read this message)
- rsync (installed per default on Ubuntu)
- intel MKL - see <https://apache.github.io/systemds/site/run#using-intel-mkl-native-instructions>

Local Machine (the laptop im sitting with) and Main (a server node) machine:

- Python 3.6+ (needed to make a Python Virtual env))

Local Machine (the laptop im sitting with) only:

- pdflatex - to make the paper (Not really needed if you just look at the plots created)

The system it self is supported on Mac and windows, but my scripts are based on Bash, so if using windows install linux subsystem.

Another requirement is at least 150GB available disk space on the "main" machine.

## Install dependencies

Java: <https://openjdk.java.net/install/>
Maven: <https://maven.apache.org/install.html>
git: <https://git-scm.com/downloads>
python: <https://www.python.org/downloads/>

First to verify that the setup is correct:

```bash
java -version
mvn -version
git --version
python3 --version
```

For my system (the laptop im sitting with) the print output looks like:

```txt
Me:~/github/reproducibility/sigmod2021-exdra-p523$ java -version
-versionopenjdk version "1.8.0_292"
OpenJDK Runtime Environment (build 1.8.0_292-8u292-b10-0ubuntu1~20.04-b10)
OpenJDK 64-Bit Server VM (build 25.292-b10, mixed mode)
Me:~/github/reproducibility/sigmod2021-exdra-p523$ mvn -version
Apache Maven 3.8.3 (ff8e977a158738155dc465c6a97ffaf31982d739)
Maven home: /home/baunsgaard/maven/mvn
Java version: 1.8.0_292, vendor: Private Build, runtime: /usr/lib/jvm/java-8-openjdk-amd64/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "5.11.0-40-generic", arch: "amd64", family: "unix"
Me:~/github/reproducibility/sigmod2021-exdra-p523$ git --version
git version 2.25.1
Me:~/github/reproducibility/sigmod2021-exdra-p523$ python3 --version
Python 3.8.10
```

Note that the java version is the same for mvn and for java.

## Systems access setup

The scripts relies on specifying aliases of the different machines, such that we can specify lists of names, and ssh to each and execute commands.

To do this modify or create your .ssh/config file with an entry per server:

```txt
HOST sierra
  User <Your user>
  HostName <host name / ip address>
  IdentityFile <your key>
  ForwardAgent yes
```

Note the Forward Agent is very important here, since we rely on being able to ssh on to the other machines from each machine, do this to verify:

```txt
Me:~/github/reproducibility/sigmod2021-exdra-p523$ ssh delta
...
DELTA:~$ ssh charlie
...
CHARLIE:~$
```

If the above is running go to 'experiments/parameters.sh' to specify this list of names of the machines you want to use.

To verify that you have the correct addresses to the list of machines you want to use,
there is a small verify setup script:

```txt
Me:~/github/reproducibility/sigmod2021-exdra-p523$ ./verify_setup.sh 
alias: delta
delta
openjdk version "1.8.0_282"
OpenJDK Runtime Environment (build 1.8.0_282-8u282-b08-0ubuntu1~20.04-b08)
OpenJDK 64-Bit Server VM (build 25.282-b08, mixed mode)
Apache Maven 3.6.3
Maven home: /usr/share/maven
Java version: 1.8.0_282, vendor: Private Build, runtime: /usr/lib/jvm/java-8-openjdk-amd64/jre
Default locale: en_US, platform encoding: ANSI_X3.4-1968
OS name: "linux", version: "5.4.0-70-generic", arch: "amd64", family: "unix"
git version 2.25.1
Python 3.8.10
  
alias: india
india
...

alias: mike
mike
...
  
alias: papa
papa
...

alias: romeo
romeo
...
  
alias: sierra
sierra
...
  
alias: uniform
uniform
...
  
alias: charlie
charlie
...
  
alias: localhost
XPS-15-7590
openjdk version "1.8.0_292"
OpenJDK Runtime Environment (build 1.8.0_292-8u292-b10-0ubuntu1~20.04-b10)
OpenJDK 64-Bit Server VM (build 25.292-b10, mixed mode)
bash: mvn: command not found
git version 2.25.1
Python 3.8.10
  
```

The major version, aka 1.8 java, should be the same on all machines, minor version differences should not matter.
If the default version is not set to java 1.8 then note if the java 1.8 is available.

## IMPORTANT

From here on the settings in parameters.sh really matter, therefore set them appropriately to what you want to reproduce.

Note that the version of systemds installed must be:
systemdsHash="3227fdb70c6afcbfdca28a7a323ae6927048b37e"
for the initial install and to to generate the data
you can set this in the parameters.
After data generation you can install different versions.

also at anytime you can skip to the synchronize and plotting of your results.

## Step 1 Install SystemDS on all machines

If all of the above worked then we should be ready to install SystemDS.

This part installs and setup the directories for the experiments.

note the directories can be changed in the parameters.sh file.

ALL SCRIPTS ARE TO BE EXECUTED FROM INSIDE THE EXPERIMENTS DIRECTORY ON THE LOCAL MACHINE (your laptop) FROM NOW ON!

to install on all machines simply run the 'install.sh'

```bash
./install.sh
```

This script downloads systemds and installs the specified GIT ID from parameters.sh
Following this it setup a python venv, and installs the required packages.
Then it builds the systemds python API for the venv.
finally, it setup the experiments folder.

If you do look at the git status on any of the machines inside systemds it should say that there are modifications in some python files.
Just ignore these changes since these are autogenerated files.

## Setup and distribute datasets

The distribution and generation of the datasets is a bit complicated,
the basic idea is that the main machine (not your laptop) generate the data and distribute the individual federated data partitions to
the different worker addresses.

To generate all the data run:

```bash
./setupData.sh
```

Note this can take about a hour, depending on disk and network speed (because of a part of the script using python that takes for ever)

## Run initial "local" experiments

To run the base line use the run_local script, This ssh to the main machine specified in parameters.sh and execute the local experiment with no distribution.

```bash
./run_local.sh
```

## Run LAN experiments

To run the lan experiments use

```bash
./run_LAN.sh
```

again this ssh to the main machine and execute the distributed experiments with that machine as the controller.

To cover all the experiments, remember to modify the parameters.sh to run the different experiments.

## Run WAN experiments

To run the WAN experiments make sure that either you have direct access to the ports of the workers, or you port forward them through ssh tunnels.
I have to port forward myself.
To enable this set the setting inside `parameters.sh`

then to port forward run the port forward script once.

If you are using cloud resources, allow outside access to the port range 8000 - 8007 and disable the port forward.

```bash
./run_WAN.sh
```

To cover all the experiments, remember to modify the parameters.sh to run the different experiments.

## Run Other (TensorFlow and SKLearn)

Again this require access to the main node, since this experiment is run there.

```bash
./run_other.sh
```

this should cover all the other experiments in it self, so no need to modify anything.

## Synchronize results

This loops through all nodes and copy the results from them to the local machine.

```bash
./syncResults.sh
```

Now you should be able to read the results inside the results folder.
all experiments are separated into the different fed versions with fed 5 meaning 5 workers.
the "fed" folder contains logs from the workers.
"loc" the local experiments, and "other" the Tensorflow and SKLearn experiment results

Also included is a "GitID" file specifying the versions of systemds used.

## Plotting

This script does three things,

1. Aggregate results into readable csv files (located inside the plots folder)
2. Make pdf plots used in the paper.
3. Copy the plots into the paper folder to enable easy building of the paper.

```bash
./plot.sh
```

## Make the paper

The paper can now be build, simply cd into the paper, and
build using:

```bash
./genPaper.sh
```

## Done

Now you should have a reproduced paper, that you can compare the submitted version with.
