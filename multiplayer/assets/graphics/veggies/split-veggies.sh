#!/bin/bash

for offset_y in {0..4}; do
    for offset_x in {0..11}; do
        # echo offset_x: $(($offset_x * 32))
        # echo offset_y: $(($offset_y * 32))
        # echo
        convert -extract 32x32+$((${offset_x} * 32))+$((${offset_y} * 32)) veggies.png veggie-${offset_x}-${offset_y}.png
    done
done
