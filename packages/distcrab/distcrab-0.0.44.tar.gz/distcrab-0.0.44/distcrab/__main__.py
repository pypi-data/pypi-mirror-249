#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True

from asyncio import run
from .main import Distcrab
from .future import future

run(future(Distcrab))
