Intersectlib is a package I created to help  with code that contains range intersections.

To install it run: ``pip install intersectlib``

This package comes with the following features:

``Find intersections between ranges: find_intersections()``

``Find a list with remainders after the intersection is removed: find_remainders()``

``Find both of the above: find_intersection_and_remainders()``

``Find and transform the intersection with a provided amount: transform_intersection()``

Examples:

``find_intersection((2, 10), (2, 5)) >> (2, 5)``

``find_remainders(range(2, 10), range(2, 5)) >> [(5, 10)]``

``find_remainders((2, 20), (8, 12)) >> [(2, 8), (12, 20)]``

``find_intersection_and_remainders((2, 10), (2, 5)) >> (2, 5), [(5, 10)]``

``transform_intersection((2, 10), (2, 5), 5) >> (2, 5) + 5 >> (7, 12)``



