<p align="center">
  <img width="400" alt="HoloPipelinesCLI logo" src="https://user-images.githubusercontent.com/23082383/79690583-0ec66180-8253-11ea-8088-0131d01beb89.png">
</p>

A python command line tool that incorporates a barebone version of [HoloPipelines](https://github.com/nbckr/HoloRepository-Core/tree/dev/HoloPipelines), wich is part of [HoloRepository](https://github.com/nbckr/HoloRepository-Core), to segment and generate 3D models of various anatomical stuctures. These include the lungs, brain, kidneys, abdominals and bones.


## Local Installation
As of right now this tool can only run in this local repository. To do so, first build the environment using one of the conda yaml files.
There are four different environments based on your hardware and software:

||GPU support|CPU only|
|-|:-:|:-:|
|**Ubuntu**|environment_gpu.yml|environment.yml|
|**Windows**|environment_win_gpu.yml|environment.yml|


```bash
conda env create -f environment_gpu.yml
```

After building the environment, activate the environment and install the local package.
```bash
conda activate holopipelines

pip install -e .
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

## Example Usage
### Basic Usage
#### Basic example
The following example uses the `lung_segmentation` pipeline on a stack of dicom images stored in the `lung-scan` directory.
The generated mesh is stored at `output.glb`.

```bash
HoloPipelines lung_segmentation lung-scan output.glb

# or

HoloLung lung-scan output.glb
```

The output will look similar to the one shown below:

<p align="center">
  <img width="300" alt="HoloPipelinesCLI logo" src="https://user-images.githubusercontent.com/23082383/79738114-37eafe80-82f4-11ea-88d3-cb80b9648671.PNG">
</p>

#### Multiple input files
Some pipelines need more than one scan to perform the generation. Below is an example of the `brain_segmentation` that uses
three different MRI modalities to generate the hologram. The three modalities `flair_scan.nii.gz`, `t1_scan.nii.gz`, and
`ir_scan.nii.gz` are stored as compressed NIfTI images.

```bash
HoloBrain flair_scan.nii.gz t1_scan.nii.gz ir_scan.nii.gz output.glb
```

### Other functionality
Optional flags can be used when invoking a pipeline. These include the segmentation type and silencing logs, as described below:

#### Specifying Segmentation type
A single integer or a series of integers that correspond to anatominal sub-structures can be passed to the command. Information on the integer mappings can be viewed through the help command.

```bash
HoloAbdominal abdominal_scan output.glb -t 1 5 7
```
Here, the invocation with the `-t` flag produces a model with the spleen, liver and pancreas.

#### Silencing logging
If no output is needed. The logging level can simply be reduced to ERROR using the `--quiet` or in short `-q` flag.

```bash
HoloBone -q bone_scan output.glb
```
