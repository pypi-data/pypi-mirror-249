# micronuclAI labeling tool

## Installation
```
pip install micronuclAI-labeling
```

## Requirements
- Python 3.10

## Usage

To launch micronuclAI labeling tool, run the following command:

```
python -m micronuclei_labeling_tool --input path/to/image --mask path/to/mask --output path/to/output
```

Once the tool is launched, you can use the following keyboard shortcuts:

The tool works by pressing any of the keys from 0-9:

The key 0 for no micro-nuclei present.
The keys 1-9 for the number of observed micro-nuclei in the image.
The key r is used to go back one image (in case any labeling mistake occurs).

**NOTE:** Labeling doesn't have to be done in one session, it can be resumed later on.  
**NOTE:** Once labeling is complete the tool will not initiate.  
**NOTE:** Output, Input and Mask paths are required and must be the same in order to resume labeling.  