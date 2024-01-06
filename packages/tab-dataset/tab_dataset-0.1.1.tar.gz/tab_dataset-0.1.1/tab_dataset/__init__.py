# -*- coding: utf-8 -*-
"""
***TAB-dataset Package***

This package contains the following classes and functions:

Field structure

- `tab-dataset.cfield` :
    - `tab-dataset.cfield.Cfield`
    - `tab-dataset.cfield.Cutil`
    - `tab-dataset.cfield.root` (function)
    - `tab-dataset.cfield.identity` (function)

- `tab-dataset.field` :
    - `tab-dataset.field.Field`
    - `tab-dataset.field.Nfield`
    - `tab-dataset.field.Sfield`

- `tab-dataset.field_interface` :
    - `tab-dataset.field_interface.FieldInterface`
    - `tab-dataset.field_interface.FieldEncoder`
    - `tab-dataset.field_interface.CborDecoder`

Dataset structure

- `tab-dataset.cdataset` :
    - `tab-dataset.cdataset.Cdataset`
    - `tab-dataset.cdataset.DatasetAnalysis

- `tab-dataset.dataset` :
    - `tab-dataset.dataset.Dataset

- `tab-dataset.dataset_structure` :
    - `tab-dataset.dataset_structure.DatasetStructure

- `tab-dataset.dataset_interface` :
    - `tab-dataset.dataset_interface.DatasetInterface

Note: Analysis functions are defined in another package `TAB-analysis`

For more information, see the
[user guide](https://loco-philippe.github.io/tab-dataset/docs/user_guide.html)
or the [github repository](https://github.com/loco-philippe/tab-dataset).
"""
from tab_dataset.dataset import Ndataset, Sdataset
from tab_dataset.cdataset import Cdataset
from tab_dataset.field import Nfield, Sfield
from tab_dataset.cfield import Cfield

#print('package :', __package__)
