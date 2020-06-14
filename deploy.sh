#!/bin/bash
rsync -avze ssh --exclude-from 'exclude.txt' --progress ./ root@111.230.131.247:/home/www/JUDGE/