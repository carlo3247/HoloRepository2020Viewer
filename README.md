<p align="center">
  <img width="600" alt="HoloPipelinesCLI logo" src="https://user-images.githubusercontent.com/23082383/80860583-6f489c00-8c60-11ea-950c-e27ceb89b410.png">
</p>

This repository contains a python tool that incorporates a barebone version of [HoloPipelines](https://github.com/nbckr/HoloRepository-Core/tree/dev/HoloPipelines), wich is part of [HoloRepository](https://github.com/nbckr/HoloRepository-Core), to segment and generate 3D models of various anatomical stuctures. These include the lungs, brain, kidneys, abdominals and bones.

<p align="center">
  <img width="340" alt="lung scan" src="https://user-images.githubusercontent.com/23082383/81289225-f087a080-905d-11ea-8815-818f9503b2ff.png">
  <img width="540" alt="lung demo" src="https://user-images.githubusercontent.com/23082383/81220853-e8861d00-8fd9-11ea-98f0-7cea18d9916c.gif">
</p>
<br />

Through the GUI interface, one can either process a new medical scan or open an existing hologram. The created objects can be viewed through a proof of concept hologram viewer built on top of [vtkplotter](https://github.com/marcomusy/vtkplotter). The **2D View** will attempt to open the scan using the default program selected for the task. For this, we recommend [mango](http://ric.uthscsa.edu/mango/).

On Windows, the tool also includes an augmented reality (AR) view, which uses the HoloRegistration application. This enables segmented organ models to be overlayed over the human body using the webcam.

Disclaimer: This system is a Proof of Concept, provided as is, and not for redeployment or use in medical scenarios without further development. It does not meet any medical guidelines and is intended to show potential usage and design for future workflows of using Holographics and 3D imaging of CT scans. Use at your own risk.


# Getting started with the latest release
The latest release is the [2020 version](https://github.com/carlo3247/HoloRepository2020Viewer/releases/tag/v1.0). To use this release, download the file called **HoloPipelinesCLI.7z** and uncompress it using [7zip](https://www.7-zip.org/). Then inside the folder, run the viewer by double-clicking **run.bat**.

<br />
<p align="center">
  <img width="600" alt="lung demo" src="https://user-images.githubusercontent.com/23082383/81221140-56324900-8fda-11ea-9c99-02db6fb3bd6c.gif">
</p>


# Manual Setup
The latest code for HoloRepository2020Viewer can be found at https://github.com/carlo3247/HoloRepository2020Viewer
## Installation
The tool has only been tested using [python3.7](https://www.python.org/downloads/release/python-370/), this version is recommended. To do so, first build the environment using one of the [conda](https://docs.conda.io/en/latest/) yaml files.
There are four different environments based on your hardware and software:

||[GPU support](https://github.com/carlo3247/HoloRepository2020Viewer/tree/v0.1_gpu)|[CPU only](https://github.com/carlo3247/HoloRepository2020Viewer/tree/v0.1_cpu)|
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
## Opening the Viewer
The following command will start up the viewer:
```bash
python user_interface.py
```


## CLI Usage of HoloPipelines Functionality
Another method of using the tool involves the command line interface (CLI).

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

### Examples
#### Basic example
The following example uses the `lung_segmentation` pipeline on a stack of dicom images stored in the `lung-scan` directory.
The generated mesh is stored at `output.glb`.

```bash
HoloPipelines lung_segmentation lung-scan output.glb

# or

HoloLung lung-scan output.glb
```

The output will look similar to the one shown below. Rendered are the lung (light blue) and the airway (dark blue).

<p align="center">
  <img width="300" alt="lung output" src="https://user-images.githubusercontent.com/23082383/79738114-37eafe80-82f4-11ea-88d3-cb80b9648671.PNG">
</p>

#### Multiple input files
Some pipelines need more than one scan to perform the generation. Below is an example of the `brain_segmentation` that uses
three different MRI modalities to generate the hologram. The three modalities `flair_scan.nii.gz`, `t1_scan.nii.gz`, and
`ir_scan.nii.gz` are stored as compressed NIfTI images.

```bash
HoloBrain flair_scan.nii.gz t1_scan.nii.gz ir_scan.nii.gz output.glb
```

The output will look similar to the one shown below. Rendered are the cortical gray matter (light blue), basal ganglia (pink), and white matter lesion (yellow).

<p align="center">
  <img width="300" alt="brain output" src="https://user-images.githubusercontent.com/23082383/79739177-b8f6c580-82f5-11ea-88c9-a1b7f2aba05c.PNG">
</p>

### Other functionality
Optional flags can be used when invoking a pipeline. These include the segmentation type and silencing logs, as described below:

#### Specifying Segmentation type
A single integer or a series of integers that correspond to anatominal sub-structures can be passed to the command. Information on the integer mappings can be viewed through the help command.

```bash
HoloAbdominal abdominal_scan output.glb -t 1 5 6 7
```
Here, the invocation with the `-t` flag produces a model with the spleen, liver, stomach and pancreas.

The output will look similar to the one shown below. Rendered are the spleen (green), liver (yellow), stomach (red) and pancreas (blue).

<p align="center">
  <img width="300" alt="abdominal output" src="https://user-images.githubusercontent.com/23082383/79739710-75508b80-82f6-11ea-8a94-56aa401e1201.PNG">
</p>

#### Silencing logging
If no output is needed. The logging level can simply be reduced to ERROR using the `--quiet` or in short `-q` flag.

```bash
HoloBone -q bone_scan output.glb
```

<p align="center">
  <img width="300" alt="bone output" src="https://user-images.githubusercontent.com/23082383/79740241-3ff86d80-82f7-11ea-8eba-afa22ef2e4dd.PNG">
</p>

# Architecture of HoloRepository2020Viewer

![HoloViewer (2)](https://user-images.githubusercontent.com/24452907/81240166-94416400-8ffe-11ea-90e0-744f9f7530fc.png)


# Acknowledgements
Main authors: Immanuel Baskaran, Abhinath Kumar, Carlo Winkelhake, Daren Alfred

Supervisors: Prof. Dean Mohamedally, Prof. Neil Sebire, Sheena Visram

Built at [University College London](https://www.ucl.ac.uk/) in cooperation with [Intel™](https://www.intel.co.uk) and [GOSH DRIVE](https://www.goshdrive.com/).


Logo is derived from a work by <a href="https://www.freepik.com/">Freepik</a> at <a href="https://www.flaticon.com/">www.flaticon.com</a>.
