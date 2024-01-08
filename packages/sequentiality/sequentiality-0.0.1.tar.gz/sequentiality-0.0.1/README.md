
# Sequentiality

## Introduction

Sequentiality is a Python package designed for extracting key features from a list of integers. It specializes in identifying various forms of Longest Consecutive Subsequences (LCS) within an integer list. This functionality is crucial for data analysis, statistical assessments, and algorithmic processing in numerous fields.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributors](#contributors)
- [License](#license)

## Installation

```python
pip install sequentiality
```

## Features & Usage

Sequentiality provides methods for the following feature extraction capabilities:

1. **find_LongestConseqSubseq**: Finds the Longest Consecutive Subsequence of integers in the list.
2. **find_LongestConseqSubseq_1gap**: Identifies the LCS with one gap allowed.
3. **find_LongestConseqSubseq_2gap**: Extracts the LCS allowing two gaps (only once between them).
4. **find_LongestConseqSubseq_from_end**: Determines the LCS counted from the end of the list.
5. **find_LongestConseqSubseq_from_end_with_1_gap**: LCS from the end with one gap allowed (only once).
6. **find_LongestConseqSubseq_from_end_with_2_gap**: LCS from the end with two gaps allowed (specific conditions apply).

Additional utility methods:

- **find_sequential_elements_with_difference_of_2**: Finds pairs in the sequence with a difference of 2.
- **find_sequential_elements_with_difference_of_3**: Finds pairs in the sequence with a difference of 3.


```python
seq = Sequentiality()
sample = [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 16]
print(seq.find_LongestConseqSubseq(sample))
print(seq.find_LongestConseqSubseq_1gap(sample))
print(seq.find_LongestConseqSubseq_2gap(sample))
print(seq.find_LongestConseqSubseq_from_end(sample))
print(seq.find_LongestConseqSubseq_from_end_with_1_gap(sample))
print(seq.find_LongestConseqSubseq_from_end_with_2_gap(sample))
```

## Documentation

https://github.com/karaposu/sequentiality


## License

MIT License

Copyright (c) 2024 Enes Kuzucu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
