#!/bin/bash

for i in {1..424}
do
    python main.py BV1gt411q7Pp-$i
done

for i in {1..22}
do
    python main.py BV1bM4y1G7yC-$i
done

# sh download_deemo.sh