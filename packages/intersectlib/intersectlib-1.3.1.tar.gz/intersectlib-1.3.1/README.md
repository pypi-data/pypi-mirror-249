
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
source: tuple / range
destination: tuple / range
value_to_add: int
intersection: tuple
remainders: list of tupples

# find the intersection between two ranges
find_intersections(source, destination)

find_intersections((2, 10), range(5, 12)) >> (5, 10)

# find the remainders when the intersection is removed
find_remainders(source, destination)

find_remainders((2, 10), range(5, 12)) >> [(2, 5), (10, 12)]

# both of the functions above
find_intersection_and_remainders(source, destination)
find_intersection_and_remainders((2, 10), range(5, 12)) >> (5, 10), [(2, 5), (10, 12)]

# find a new intersection and transform it
transform_new_intersection(source, destination, value_to_add)
transform_new_intersection((2, 10), range(5, 12), 5) >> (10, 15)

# transform an already existing intersection
transform_existing_intersection(intersection, value_to_add)

transform_existing_intersection((5, 10), 5) >> (10, 15)
transform_existing_intersection9=((5, 10), -3) >> (2, 7)
```


## Authors

- [@Rducker](https://github.com/Rducker0208)


## Support

For support:
- email duckerricardo@gmail.com.
- message me on discord: randomduck08
- post an issue at: https://github.com/Rducker0208/intersectlib/issues

