<h1 align="center">OCT Converter</h1>
<p align="center">
 Python-based tools for reading OCT and fundus data.
</p>


<p align="center">
    <img width="320" height="320" src="https://user-images.githubusercontent.com/7947315/202814956-6e7e6702-82f4-4250-8625-ec23c1727e4f.jpg">
    <img width="320" height="320" src="https://user-images.githubusercontent.com/7947315/202814575-9f18b7ca-3028-4d23-9b82-015995c44eab.gif">
</p>

## Description
In ophthalmology, data acquired from the scanner is often exported in the manufacturer's proprietary file format. OCT-Converter provides python-based tools for extracting images (optical coherence tomography and fundus), as well as associated metadata, from these files.

## Supported file formats
* .fds (Topcon)
* .fda (Topcon)
* .e2e (Heidelberg)
* .img (Zeiss)
* .oct (Bioptigen)
* .OCT (Optovue)
* .dcm

## Installation
Requires python 3.7 or higher.

```bash
pip install oct-converter
```


## Usage
A number of example usage scripts are included in `examples/`.

Here is an example of reading a .fds file:

```python
from oct_converter.readers import FDS

# An example .fds file can be downloaded from the Biobank website:
# https://biobank.ndph.ox.ac.uk/showcase/refer.cgi?id=30
filepath = '/home/mark/Downloads/eg_oct_fds.fds'
fds = FDS(filepath)

oct_volume = fds.read_oct_volume()  # returns an OCT volume with additional metadata if available
oct_volume.peek(show_contours=True) # plots a montage of the volume, with layer segmentations is available
oct_volume.save('fds_testing.avi')  # save volume as a movie
oct_volume.save('fds_testing.png')  # save volume as a set of sequential images, fds_testing_[1...N].png
oct_volume.save_projection('projection.png') # save 2D projection

fundus_image = fds.read_fundus_image()  # returns a  Fundus image with additional metadata if available
fundus_image.save('fds_testing_fundus.jpg')

metadata = fds.read_all_metadata(verbose=True) # extracts all other metadata
with open("fds_metadata.json", "w") as outfile:
    outfile.write(json.dumps(metadata, indent=4))

# create and save a DICOM
dcm = create_dicom_from_oct(filepath)
```

## Contributions
Are welcome! Here is a [development roadmap](https://github.com/marksgraham/OCT-Converter/issues/86), including some easy first issues. Please open a [new issue](https://github.com/marksgraham/OCT-Converter/issues/new) to discuss any potential contributions.

## Updates
9 November 2023
- Can now save .e2e, .img, .oct, and .OCT files as DICOMs with correct headers.

22 September 2023
- DICOM support: can now save .fda/.fds files as DICOMs with correct headers.
- Much more complete extraction of .fda/.fds metadata.

28 March 2023
- Metadata extraction for .fds expanded to match that of .fda file.

31 January 2023
- Greatly extended support for extracting metadata from .fda files.

7 August 2022
- Contours (layer segmentations) are now extracted from .e2e files.
- Acquisition date is now extracted from .e2e files.

16 June 2022
- Initial support for reading Optovue OCTs.
- Laterality is now extracted separately for each OCT/fundus image for .e2e files.
- More patient info extracted from .e2e files (name, sex, birthdate, patient ID).

24 Aug 2021
- Reading the Bioptigen .OCT format is now supported.

11 June 2021
- Can now specify whether Zeiss .img data needs to be de-interlaced during reading.

14 May 2021
- Can save 2D projections of OCT volumes.

30 October 2020
- Extract fundus and laterality data from .e2e
- Now attempts to extract additional volumetric data from .e2e files that was previously missed.

22 August 2020
- Experimental support for reading OCT data from .fda files.

14 July 2020
- Can now read fundus data from .fda files.

## Related projects
- [uocte](https://bitbucket.org/uocte/uocte/wiki/Home) inspired and enabled this project
- [LibE2E](https://github.com/neurodial/LibE2E) and [LibOctData](https://github.com/neurodial/LibOctData) provided some additional descriptions of the .e2e file spec
- [eyepy](https://github.com/MedVisBonn/eyepy) for python-based import, visualisation, and analysis of OCT data
- [eyelab](https://github.com/MedVisBonn/eyelab) is a tool for annotating this data

## Clinical use
We can't guarantee images extracted with OCT-Converter will match those extracted or viewed with the manufacturer's software. Any use in clinical settings is at the user's own risk.
