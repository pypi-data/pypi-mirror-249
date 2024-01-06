# Fortran to C / C to Fortran (nested) index converter   

## pip install fortran2cc2fortran

### Tested against Windows 10 / Python 3.11 / Anaconda 



```python

FUNCTIONS
    calculate_flat_index_c(nested_index, array_shape)
        Calculate the flat index from a given nested index in C order.
        
        Parameters:
        - nested_index (list): Nested index in C order.
        - array_shape (tuple): Shape of the original array.
        
        Returns:
        - int: Flat index corresponding to the nested index in C order.
    
    calculate_flat_index_f(nested_index, array_shape)
        Calculate the flat index from a given nested index in Fortran order.
        
        Parameters:
        - nested_index (list): Nested index in Fortran order.
        - array_shape (tuple): Shape of the original array.
        
        Returns:
        - int: Flat index corresponding to the nested index in Fortran order.
    
    calculate_nested_index_c_order(flat_index, array_shape)
        Calculate the nested index of a given flat index in C order.
        
        Parameters:
        - flat_index (int): The flat index to be converted.
        - array_shape (tuple): Shape of the original array.
        
        Returns:
        - list: List of indices in C order corresponding to the flat index.
    
    calculate_nested_index_f_order(flat_index, array_shape)
        Calculate the nested index of a given flat index in Fortran order.
        
        Parameters:
        - flat_index (int): The flat index to be converted.
        - array_shape (tuple): Shape of the original array.
        
        Returns:
        - list: List of indices in Fortran order corresponding to the flat index.
    
    convert_c_to_f_index(c_index, array_shape)
        Convert C order to Fortran order and return the corresponding nested index.
        
        Parameters:
        - c_index (list): Nested index in C order.
        - array_shape (tuple): Shape of the original array.
        
        Returns:
        - list: Nested index in Fortran order corresponding to the C order index.
    
    convert_f_to_c_index(f_index, array_shape)
        Convert Fortran order to C order and return the corresponding nested index.
        
        Parameters:
        - f_index (list): Nested index in Fortran order.
        - array_shape (tuple): Shape of the original array.
        
        Returns:
        - list: Nested index in C order corresponding to the Fortran order index.
		
		
import numpy as np
from fortran2cc2fortran import (
    convert_f_to_c_index,
    convert_c_to_f_index,
    calculate_nested_index_c_order,
    calculate_flat_index_c,
    calculate_nested_index_f_order,
    calculate_flat_index_f,
)

indlist = [10, 5, 4, 2, 3]
listex = np.ascontiguousarray(
    np.copy(np.arange(np.product(indlist)).reshape(tuple(indlist)))
)
liste = listex.ravel(order="F")
liste2 = listex.ravel(order="C")
if not liste.flags["F_CONTIGUOUS"]:
    liste = np.asfortranarray(liste)
if not liste2.flags["C_CONTIGUOUS"]:
    liste2 = np.ascontiguousarray(liste2)
for l in range(len(liste)):
    value = liste[l]
    value2 = liste2[l]
    c_order_index = calculate_nested_index_c_order(
        flat_index=l, array_shape=listex.shape
    )
    flatindex1 = calculate_flat_index_f(
        nested_index=c_order_index, array_shape=listex.shape
    )
    f_order_index = calculate_nested_index_f_order(
        flat_index=l, array_shape=listex.shape
    )
    flatindex2 = calculate_flat_index_f(
        nested_index=f_order_index, array_shape=listex.shape
    )
    from_c_to_f = convert_c_to_f_index(c_index=c_order_index, array_shape=listex.shape)
    from_f_to_c = convert_f_to_c_index(f_index=f_order_index, array_shape=listex.shape)
    print(f"values/flat index c: {value2}")
    print(f"values/flat index c_order_index: {c_order_index}")

    print(f"values/flat index flatindex1: {flatindex1}")
    print(f"values/flat index f: {value}")
    print(f"values/flat index f_order_index: {f_order_index}")
    print(f"values/flat index flatindex2: {flatindex2}")
    print("00000000000000000000000000000000000000000000000000")
    print(f"values/flat index from_c_to_f: {from_c_to_f}")
    print(f"values/flat index from_f_to_c: {from_f_to_c}")
    print(
        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )

# ......
# values/flat index c: 10
# values/flat index c_order_index: [0, 0, 1, 1, 1]
# values/flat index flatindex1: 10
# values/flat index f: 24
# values/flat index f_order_index: [0, 1, 0, 0, 0]
# values/flat index flatindex2: 24
# 00000000000000000000000000000000000000000000000000
# values/flat index from_c_to_f: [0, 1, 0, 0, 0]
# values/flat index from_f_to_c: [0, 0, 1, 1, 1]
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# values/flat index c: 11
# values/flat index c_order_index: [0, 0, 1, 1, 2]
# values/flat index flatindex1: 11
# values/flat index f: 144
# values/flat index f_order_index: [1, 1, 0, 0, 0]
# values/flat index flatindex2: 144
# 00000000000000000000000000000000000000000000000000
# values/flat index from_c_to_f: [1, 1, 0, 0, 0]
# values/flat index from_f_to_c: [0, 0, 1, 1, 2]
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# ......
		
```
