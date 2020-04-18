# HoloPipelinesCLI

A python command line tool that incorporates a barebone version of [HoloPipelines](https://github.com/nbckr/HoloRepository-Core/tree/dev/HoloPipelines), wich is part of [HoloPipelines](https://github.com/nbckr/HoloRepository-Core), to segment and generate 3D models of various anatominal stuctures. These include the lungs, brain, kidneys, abdominals and bones.


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
The following example uses the `lung_segmentation` pipeline on a stack of dicom images stored in the `lung-scan` directory.
The generated mesh is stored at `output.glb`.

```bash
HoloPipelines lung_segmentation lung-scan output.glb

# or

HoloLung lung-scan output.glb
```

Some pipelines need more than one scan to perform the generation. Below is an example of the `brain_segmentation` that uses
three different MRI modalities to generate the hologram. The three modalities `flair_scan.nii.gz`, `t1_scan.nii.gz`, and
`ir_scan.nii.gz` are stored as compressed NIfTI images.

```bash
HoloPipelines brain_segmentation flair_scan.nii.gz t1_scan.nii.gz ir_scan.nii.gz output.glb

# or

HoloBrain flair_scan.nii.gz t1_scan.nii.gz ir_scan.nii.gz output.glb
```