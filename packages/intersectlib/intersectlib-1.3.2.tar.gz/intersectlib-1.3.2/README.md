
# intersectlib

intersectlib is a library created to find intersections and remainders between two ranges and transform those.

## Features

- Find range intersections
- Find remaining source
- Transform intersections


## Installation

Install intersectlib using pip

```bash
pip install intersectlib
```
    
## Usage/Examples

```python

# find the intersection between two ranges
find_intersections(source: tuple | range, destination: tuple | range)

find_intersections((2, 10), range(5, 12)) >> (5, 10)
find_intersections((2, 10), (20, 30)) >> None

# find the remainders when the intersection is removed
find_remainders(source: tuple | range, destination: tuple | range)

find_remainders((2, 10), range(5, 12)) >> [(2, 5), (10, 12)]
find_remainders((2, 10), (1, 12)) >> []

# both of the functions above
find_intersection_and_remainders(source: tuple | range, destination: tuple | range)
find_intersection_and_remainders((2, 10), range(5, 12)) >> (5, 10), [(2, 5), (10, 12)]

# find a new intersection and transform it
transform_new_intersection(source: tuple | range, destination: tuple | range, value_to_add: int)
transform_new_intersection((2, 10), range(5, 12), 5) >> (10, 15)

# transform an already existing intersection
transform_existing_intersection(intersection: tuple | range, value_to_add: tuple | range)

transform_existing_intersection((5, 10), 5) >> (10, 15)
transform_existing_intersection((5, 10), -3) >> (2, 7)
```


## Authors

- [@Rducker](https://github.com/Rducker0208)


## Support

For support:
- email duckerricardo@gmail.com.
- message me on discord: randomduck08
- post an issue at: https://github.com/Rducker0208/intersectlib/issues

