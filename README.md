# Experimental Math

A collection of mathematical experiments and explorations, often venturing outside the author's primary area of expertise.

## Contents

### Statistical Goldbach

Goldbach's Conjecture examined from a statistical point of view. The script (written for [SageMath](https://www.sagemath.org/)) counts the number of ways each even number can be decomposed as a sum of two primes, then plots the results against a conjectured bounding function.

Key ideas:

- For every even number up to a given limit, enumerate all representations as a sum of two primes
- Plot the count of decompositions and color each point based on whether it falls above, on, or below a comparison curve
- The default comparison function uses the golden ratio and pi: `f(x) = (x / (phi * pi))^(1/phi)`

**Usage** (requires SageMath):

```python
# In a Sage notebook or terminal
load("statistical_goldbach/statistical_goldbach")
```

See [`statistical_goldbach/README.md`](statistical_goldbach/README.md) for more details.

## License

The Statistical Goldbach sub-project is released under the GPL v3 license. See the LICENSE file in that directory for details.
