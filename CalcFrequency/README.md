# Algorithms to Calculate Frequency

The scripts  here are an attempt to understand the different ways to calculate the frequency of the power grid using volatage data.
Matlab files are borrowed from this instructable project http://www.instructables.com/id/Power-System-Frequency-Determination-using-Arduino/

The focus was in the the following algorithms:

1. -MOORE, CARRANZA AND JOHNS, “A numeric technique for quick
evaluation of frequency”, IEE Proc. Gener. Transm. Distib., Vol.141, No.5, Sept
1994, pp 529-536MOORE, CARRANZA AND JOHNS, “A numeric technique for quick
evaluation of frequency”

2. -AGHAZADEH, LESANI, SANAYE-PRASAD AND GANJI, “New technique
for frequency & amplitude estimation of power system signals”, IEE Proc. Gener.
Transm. Distib., Vol.152, No.3, May 2005, pp 435-440

The full report of the instructables project offers a quick overview of methods mentioned.
You can find the full report on here: https://drive.google.com/drive/u/0/folders/0B-6iYWdfHIuJdFhGMzB6SkJCaTA

## Purpose
We are using adafruits [tweet-a-watt](https://learn.adafruit.com/tweet-a-watt/) to interface with the power grid.
We were looking at getting a more accurate frequency reading than the one provided by the kill a watt.
