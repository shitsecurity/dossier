#!/usr/bin/env python

from difflib import SequenceMatcher as Diff
from functools import partial

Differ=partial(Diff, None)
