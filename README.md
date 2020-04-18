# HoloPipelinesCLI

A python command line tool that incorporates a barebone version of HoloPipelines to segment and generate 3D models of various anatominal stuctures. These include the lungs, brain, kidneys, abdominals and bones.


## Local Installation
As of right now this tool can only run in this local repository. To do so, first build the environment using one of the conda yaml files.
There are four different environments based on your hardware and software:

||GPU support|CPU only|
|-|:-:|:-:|
|**Unix based**|environment_gpu.yml|envioronment.yml|
|**Windows**|environment_win_gpu.yml|envioronment_win.yml|


```bash
conda env create -f environment_gpu.yml
```

After building the environment, install the local package.
```bash
pip install .
```

## Usage
There are several ways to run the local HoloPipelines.
The general command line interface can be invoked like this:
```bash
HoloPipelines -h
```

Instead of running the tool through the main interface, a pipeline-specific interface is also provided.

```bash
HoloBrain -h
HoloKidney -h
HoloLung -h
HoloAbdominal -h
HoloBone -h
```