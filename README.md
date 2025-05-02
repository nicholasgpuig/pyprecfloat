# pyprecfloat
`pyprecfloat` is a Python library that allows you to create floating point numbers with greater precision than native floats

Each `PFloat` object stores extra bits in `ChildNode` objects to preserve precision

## Usage
```python
example1 = PFloat(100.345237)
example1.toInt()
example1.toFloat()

example2 = PFloat(12485209525076533619)
example2.toInt()
example2.showNodes()

example3 = PFloat(0.348975894279782)
example3.toFloat
example3.showNodes()
```


## Roadmap
- Extend range of floating point implementation (i.e. subnormals, NaNs, infinity, etc.)
- Add more complex arithmetic (division, square root, etc.)

## Author
For now, all work is done by Nicholas Puig.

## License
[MIT](https://choosealicense.com/licenses/mit/)