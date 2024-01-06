hdf5-tools
==================================

This git repository contains a python package with an H5 class to load and combine one or more HDF5 data files (or xarray datasets) with optional filters. The class will then export the combined data to an HDF5 file, file object, or xr.Dataset. This class is designed to be fast and safe on memory. This means that files of any size can be combined and saved even on a PC with low memory (unlike xarray).

TODO:

- Create a sel method for the File class. This should mimic xarray, but create a copy of the File with optional saving to a local file just like creating a new file using the File class. At least initially to make it easier, just do straightforward indexing like is done with the LocationIndexer which gets copied over to a newly created File/dataset object.
- The to_pandas method in datasets should be similar to xarray, which creates pandas indexes. The to_pandas method for the File class should concat all of the datasets to_pandas output together.
- The to_xarray method for both Dataset and File should use the existing hdf5 local file if it exists and close the file via h5py before linking to it via the xarray open_dataset.
