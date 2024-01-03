# pylegacy

This library aims to provide backports from Python newer versions into
abandoned Python versions.

The `pylegacy` package tree structure resembles that of the Python
standard libraries, i.e. `pylegacy` consists of `pylegacy.abc`,
`pylegacy.builtins`, `pylegacy.os`, and so on. If a backport is
available for a piece of missing functionality, it can be used by
importing the functionality from the `pylegacy` namespace.

For example, `os.makedirs` in Python 2.7 lacks the `exist_ok` argument,
first introduced in Python 3.2. To enable this functionality, one would
replace the following failing code snippet:
```python
import os
os.makedirs("example_folder", exist_ok=True)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: makedirs() got an unexpected keyword argument 'exist_ok'
```

with the following working code snippet:
```python
from pylegacy import os
os.makedirs("example_folder", exist_ok=True)
```

## License

The `pylegacy` package is released under the [MIT] license (see the
[`LICENSE`] file):
```
Copyright (c) 2021-2024 Víctor Molina García

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Significant portions of the `pylegacy` package are derivative work of
the Python standard libraries. The Python source code is released under
the terms of the [PSF-2.0] license and is Copyright (c) 2001-2022 Python
Software Foundation, All rights reserved. A copy of the [PSF-2.0]
license can be found in the [`LICENSE.PSF-2.0`] file.

[MIT]:
https://spdx.org/licenses/MIT.html
[PSF-2.0]:
https://spdx.org/licenses/PSF-2.0.html
[`LICENSE`]:
https://github.com/pylegacy/pylegacy/blob/v0.2.1/LICENSE
[`LICENSE.PSF-2.0`]:
https://github.com/pylegacy/pylegacy/blob/v0.2.1/LICENSE.PSF-2.0
