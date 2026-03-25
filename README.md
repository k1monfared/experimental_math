# Experimental Math

A collection of mathematical experiments and explorations, often venturing outside the author's primary area of expertise.

## Contents

### [Statistical Goldbach](statistical_goldbach/)

Goldbach's Conjecture examined from a statistical point of view. For each even number up to 10,000, count how many ways it can be written as a sum of two primes, then analyze the patterns.

![Goldbach's Comet](statistical_goldbach/goldbach_comet.png)

Key ideas:

- Enumerate all prime-pair decompositions of every even number up to a given limit
- The resulting scatter plot ("Goldbach's comet") reveals striking structure with multiple arms
- Compare against a conjectured bounding curve using the golden ratio: `f(x) = (x / (phi * pi))^(1/phi)`
- The minimum number of decompositions grows steadily -- it never approaches zero, supporting the conjecture

![Lower Bound](statistical_goldbach/goldbach_minimum.png)

**Usage** (requires SageMath):

```python
load("statistical_goldbach/statistical_goldbach.sage")
plot_number_of_decompositions(2, 1000, (x/(a*pi))^(1/a))
```

See [`statistical_goldbach/README.md`](statistical_goldbach/README.md) for full analysis with 6 visualizations.

## License

The Statistical Goldbach sub-project is released under the GPL v3 license. See the LICENSE file in that directory for details.
