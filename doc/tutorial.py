#!/usr/bin/env python

import sys
import wordseg
from wordseg.algos import tp, puddle, dibs

# load the input text file
text = open(sys.argv[1], 'r').readlines()

# Prepare the input for segmentation
prepared = list(wordseg.prepare(text))

# Generate the gold text
gold = list(wordseg.gold(text))

# segment the prepared text with different algorithms
segmented_tp = tp.segment(prepared, threshold='relative')
segmented_puddle = puddle.segment(prepared, njobs=4, window=2)
segmented_dibs = dibs.segment(prepared, prob_word_boundary=0.1)

# evaluate them against the gold file
eval_tp = wordseg.evaluate(segmented_tp, gold)
eval_puddle = wordseg.evaluate(segmented_puddle, gold)
eval_dibs = wordseg.evaluate(segmented_dibs, gold)

# concatenate the evaluations in a table
sys.stdout.write(' '.join(('score', 'tp', 'puddle', 'dibs')) + '\n')
sys.stdout.write(' '.join(('-'*15, '-'*7, '-'*7, '-'*7)) + '\n')
for score in eval_tp.keys():
    line = ' '.join((
        score,
        '%.4g' % eval_tp[score],
        '%.4g' % eval_puddle[score],
        '%.4g' % eval_dibs[score]))
    sys.stdout.write(line + '\n')
