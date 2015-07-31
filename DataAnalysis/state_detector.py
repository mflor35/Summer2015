#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""state_detector.py: this script reads a raw data file (python dictionaries of XBee frames)
and determines from the electric current whether an applianc is off or on. Currently this script
is ony tuned to analyze data from our test refrigerator/tweet-a-watt"""

__authors__ = ["Zachary Graham (zwgraham@soe.ucsc.edu)", "Kapil Sinha"]
__author__ = ', '.join(__authors__)
__copyright__ = """Copyright © 2015 The Regents of the University of California 
All Rights Reserved"""
__credits__ = ["Zachary Graham", "Kapil Sinha", "Miguel Flores Silverio", "Andres Aranda"]
__status__ = "prototype"
__license__ = """Copyright © 2015, The Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

     * Neither the name of Center for Sustainable Energy and Power Systems nor 
       the names of its contributors may be used to endorse or promote products 
       derived from this software without specific prior written permission.

     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
import ast
DELTA_OFF = 15
DELTA_ON  = 30
METER_ADDRESS = '\x00\x01'

with open('data_sample/rawdata2.txt', 'r') as inp:
    for line in inp:
        d = ast.literal_eval(line) #raw data is python dictionaries written out as strings, this converts to a dictionary
        if d['source_addr'] == METER_ADDRESS:
            s = str(d['timestamp'])+', '
            samples = [x['adc-4'] for x in d['samples']]
            delta = max(samples) - min(samples)
            if delta < DELTA_OFF:
                print s, 'OFF', ', ' , delta
            elif delta > DELTA_ON:
                print s, 'ON', ', ', delta
            else:
                print s, 'UNSURE', ', ', delta

