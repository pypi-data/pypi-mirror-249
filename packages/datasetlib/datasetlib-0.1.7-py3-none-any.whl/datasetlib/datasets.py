# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  datasets provide basic access to well known datasets used for machine learning
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import os
import basefunctions as bf
import pandas as pd

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------
_dataSetDict = {
    "aapl": ("datasets/apple.csv", {
        "index_col": [0],
        "parse_dates": [0],
        "header": [0]
    }),
    "babynames": ("datasets/babynames.csv", {
        "index_col":[3]
    }),
    "bmw": ("datasets/bmw.csv", {
        "index_col": [0],
        "parse_dates": [0],
        "header": [0]
    }),
    "summergames": ("datasets/summergames.csv", {
        "index_col": [0],
        "header": [0]
    }),
    "titanic": ("datasets/titanic.csv", {
    })
}


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# FUNCTION DEFINTIONS
# -------------------------------------------------------------
def getDataSetList():
    """get a list of all available datasets

    Returns
    -------
    list
        list of available datasets
    """
    return list(_dataSetDict.keys())


def getDataSetFileName(dataSetName):
    """get the filename for a specific dataset

    Parameters
    ----------
    dataSetName : str
        name of dataset

    Returns
    -------
    str
        file name of dataset

    Raises
    ------
    RuntimeError
        raises RuntimeError if dataset name can't be found
    """
    print(os.path.sep.join(
                [bf.getPathName(os.path.abspath(__file__)), _dataSetDict[dataSetName][0]]))
    if dataSetName in _dataSetDict:
        return bf.normpath(
            os.path.sep.join(
                [bf.getPathName(os.path.abspath(__file__)), _dataSetDict[dataSetName][0]]))
    else:
        raise RuntimeError(f"dataset {dataSetName} not found")


def getDataSet(dataSetName):
    """get a specific dataset

    Parameters
    ----------
    dataSetName : str
        name of dataset

    Returns
    -------
    pandas dataframe
        dataframe of dataset

    Raises
    ------
    RuntimeError
        raises RuntimeError if dataset name can't be found
    """
    if dataSetName in _dataSetDict:
        fileName, kwargs = _dataSetDict[dataSetName]
        return pd.read_csv(getDataSetFileName(dataSetName), **kwargs)
    else:
        raise RuntimeError(f"dataset {dataSetName} not found")
