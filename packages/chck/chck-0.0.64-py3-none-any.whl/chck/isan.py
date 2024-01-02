# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/70_isan.ipynb.

# %% auto 0
__all__ = ['isanndata', 'isad']

# %% ../nbs/70_isan.ipynb 4
from typing import TypeGuard

# %% ../nbs/70_isan.ipynb 5
from .atyp import AnnData, anndata

# %% ../nbs/70_isan.ipynb 7
def isanndata(x) -> TypeGuard[anndata]:
    '''Check if `x` is an `ad.AnnData`.'''
    return isinstance(x, AnnData)

def isad(x) -> TypeGuard[anndata]:
    '''Check if `x` is an `ad.AnnData`.'''
    return isinstance(x, AnnData)
