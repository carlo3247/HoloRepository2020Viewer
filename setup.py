from distutils.core import setup

setup(name="HoloPipelinesCLI",
      version="0.1",
      description="HoloPipelines command line interface",
      author="Abhinath Kumar, Immanuel Baskaran, Carlo Winkelhake",
      entry_points={
          "console_scripts": [
              "HoloPipelines=holopipelines:main",
              "HoloBrain=brain_segmentation_tool:main",
              "HoloKidney=kidney_segmentation_tool:main",
              "HoloLung=lung_segmentation_tool:main",
              "HoloBone=bone_segmentation_tool:main",
              "HoloAbdominal=abdominal_segmentation_tool:main",
          ],
      },
      )
