"""
Flowa V10.5.5

Copyright (c)     2023 flowa 
License   (Lic.)  MIT

A package for easy and simple Machine Learning, Image Generation, Decision Trees, Label Encoders, and more!

Classes:
  - ai.Encoder: Encodes categorical data into numerical data.
  - ai.Tree: Represents a Decision Tree.
  - ai.ImageModel: Image generation model.

  - ai.Dataset: Class for getting pre-made datasets.

  - Node: Represents a Node in a Decision Tree.
  - Map: Represents a Map in an Encoder.

  - Network: Create a neural network.
  - Input(size): Create an input layer.
  - Hidden(size, acitvation, *activation_args, **activation_kwargs): Create a hidden layer.
  - Output(size): Create an output layer.

Functions:
  - ai.convert: Converts string of text into an object that can be converted into a dataframe using read_csv()
  - ai.read_csv: Reads a CSV file into a DataFrame.

Constants:
  - PYTHON_REQUIRED_MAJOR: Major version of Python.
  - PYTHON_REQUIRED_MINOR: Minor version of Python.

Variables:
  - datasets: Dictionary of datasets.
  - version_dict: Dictionary of version information.
  - python_tuple: Tuple of the Python version.

  - __version__: Current version of Flowa.
  - __author__: Author of Flowa.
  - __email__: Email of Flowa.
  - __discord__: Discord user for Flowa.
  - __github__: Github link for Flowa.
  - __repo__: Github link for Flowa's Repository.
  - __license__: License of Flowa.
  - __copyright__: Copyright of Flowa.
  - __all__: List of all Flowa classes.

=================================================


EXAMPLE USAGE:

```python
'''
Dataset Snippet: (music_data.csv)

age,gender,genre
25,male,Rock
30,female,Pop
22,male,HipHop
28,female,Classical
'''


from flowa.ai import (
    Encoder,
    Tree,
    read_csv,
)

encoder: Encoder = Encoder()
classifier: Tree = Tree()

csv: object = read_csv('music_data.csv')
dataframe: object = encoder.df(csv, 'gender')

X_matrix: object = dataframe.drop('genre', axis=1).values
y_column: object = encoder(dataframe['genre'].values)

classifier.fit(X_matrix, y_column)

age, gender = encoder.new(30, 'female')
fix: list = encoder.fix(age, gender)

prediction: list[int] = classifier.predict(fix)
print(encoder.inverse(prediction))

>>> ['Pop']
```

=================================================

"""

import sys


from ._version import (
    get_version,
    get_python,
)
from .network import *

version_dict: dict = get_version()
python_tuple: tuple = get_python()

PYTHON_REQUIRED_MAJOR = python_tuple[0]
PYTHON_REQUIRED_MINOR = python_tuple[1]

if (
    sys.version_info.major != PYTHON_REQUIRED_MAJOR
    or sys.version_info.minor < PYTHON_REQUIRED_MINOR
):
    import warnings

    warnings.warn(
        f"Please update python to {PYTHON_REQUIRED_MAJOR}.{PYTHON_REQUIRED_MINOR} or higher."
        f"Current Version: {sys.version}",
        category=RuntimeWarning,
    )

__version__ = "10.5.5"
__author__ = "flowa (Discord: @flo.a)"
__email__ = "flowa.dev@gmail.com"
__discord__ = "@flo.a"
__github__ = "https://github.com/flowa-ai"
__repo__ = "https://github.com/flowa-ai/flowa"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2023 flowa"
__all__: tuple = (
    "Encoder",
    "Dataset",
    "Images",
    "Tree",
    "Node",
    "Map",
    "Module",
    "Network",
    "Input",
    "Hidden",
    "Output",
    "Array",
    "Seed",
    "Random",
    "get",
    "remove",
    "modules",
    "seed",
    "Sigmoid",
    "Tanh",
    "ReLU",
    "LeakyReLU",
    "ELU",
    "Swish",
    "Gaussion",
    "Identity",
    "BinaryStep",
    "PReLU",
    "Exponential",
    "Softplus",
    "Softsign",
    "BentIdentity",
    "ArcTan",
    "SiLU",
    "Mish",
    "HardSigmoid",
    "HardTanh",
    "SoftExponential",
    "ISRU",
    "Sine",
    "Cosine",
    "SQNL",
    "SoftClipping",
    "BentIdentity2",
    "LogLog",
    "GELU",
    "Softmin",
)
