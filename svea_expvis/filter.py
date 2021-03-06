# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-07-07 17:05

@author: a002028
"""
import pandas as pd


class Name:
    """Class to extract information from file names."""

    splitter = '_'

    def __init__(self, file_name):
        """Initialize."""
        args = file_name.strip('.txt').split(self.splitter)
        self.date = pd.Timestamp(args[2])
        self.shipc = args[3]
        self.serno = float(args[4])


class SplitNameList:
    """Holds a lists of file name information."""

    dates = []
    ships = []
    sernos = []

    def __init__(self, name_list):
        """Initialize."""
        self.names = name_list
        for name in name_list:
            name_obj = Name(name)
            self.append_date(name_obj.date)
            self.append_shipc(name_obj.shipc)
            self.append_serno(name_obj.serno)

    @classmethod
    def append_date(cls, d):
        """Append date to class list."""
        cls.dates.append(d)

    @classmethod
    def append_shipc(cls, s):
        """Append ship code to class list."""
        cls.ships.append(s)

    @classmethod
    def append_serno(cls, s):
        """Append serno to class list."""
        cls.sernos.append(s)


class Filter:
    """Filter filenames according to ctd-standard format eg.
    'ctd_profile_20181208_34AR_0171.txt'.
    """

    def __init__(self, name_list):
        """Initialize."""
        lists = SplitNameList(name_list)
        self.serie_names = pd.Series(lists.names)
        self.serie_dates = pd.Series(lists.dates)
        self.serie_ships = pd.Series(lists.ships)
        self.serie_sernos = pd.Series(lists.sernos)

        self._boolean = True

    def add_filter(self, **kwargs):
        """Add new filter.

        If any valid filter arguments: append boolean according
        to @boolean.setter (property.setter).
        """
        if 'month_list' in kwargs:
            self.boolean = self.serie_dates.dt.month.isin(kwargs.get('month_list'))

        if 'ship_list' in kwargs:
            self.boolean = self.serie_ships.isin(kwargs.get('ship_list'))

        if 'serno_max' in kwargs:
            self.boolean = self.serie_sernos <= kwargs.get('serno_max')

        if 'serno_min' in kwargs:
            self.boolean = self.serie_sernos >= kwargs.get('serno_min')

    @property
    def valid_file_names(self):
        """Return valid file names."""
        return self.serie_names[self.boolean].values

    @property
    def boolean(self):
        """Return boolean."""
        return self._boolean

    @boolean.setter
    def boolean(self, add_bool):
        """Set boolean."""
        self._boolean = self._boolean & add_bool
