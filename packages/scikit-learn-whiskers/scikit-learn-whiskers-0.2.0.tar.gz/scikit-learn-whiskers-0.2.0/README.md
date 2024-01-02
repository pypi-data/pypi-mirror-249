# `scikit-learn-whiskers`
A collection (only one at this time) of tools aimed to help with some tasks of machine learning and datascience studies.  
These tools are intended to be compatible with scikit-learn utilities, and work properly inside a Pipeline.

## `WhiskerOutliers`
A class to mark as **outliers** the values that can visually be identified as outliers from a typical _box and whiskers_ plot.  
This class implements `.fit`, `transform` and `fit_transform`, as well as `get_params` and `set_params` methods as any standard scikit-learn implementation. 
  
## `StandardOutliers`
A class to mark as **outliers** the values outside the range _`threshold` * standard deviation_ around the _mean_.  
This class implements `.fit`, `transform` and `fit_transform`, as well as `get_params` and `set_params` methods as any standard scikit-learn implementation.

## Requisites:  
- `NumPy`
- `Pandas`
- `Scikit-Learn`

## Installation
To install it: `pip git+https://github.com/ayaranitram/scikit-learn-whiskers`