# ARRAY SCALER

## Introduction
A simple python tool for scaling and rescaling arrays:

## Installation

To install Array Scaler, run the following command:

```bash
pip install -e '.[lint, test]'  
```

## Usage

Here is a simple example of how to use Array Scaler:

```python
from arrayscaler.arrayscaler import ScalingHelper
import numpy as np

# Scaling integers (5) with a lower limit of 0 and upper limit of 10
print(ScalingHelper.scale(5, 0, 10))

# Scaling numpy array
print(ScalingHelper.scale(np.array([1,3,4,5,3,2]), 0, 2))

# Rescaling the scaled numpy array
print(ScalingHelper.rescale(ScalingHelper.scale(np.array([1,3,4,5,3,2]), 0, 2), 0, 2))
```

The `scale` method will scale the input array to a range of 0 to 1. The `rescale` method will rescale the scaled array back to its original range.

## Contributing