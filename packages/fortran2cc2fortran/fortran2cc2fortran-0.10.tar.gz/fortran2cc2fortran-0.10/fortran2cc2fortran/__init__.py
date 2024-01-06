def calculate_nested_index_f_order(flat_index, array_shape):
    r"""
    Calculate the nested index of a given flat index in Fortran order.

    Parameters:
    - flat_index (int): The flat index to be converted.
    - array_shape (tuple): Shape of the original array.

    Returns:
    - list: List of indices in Fortran order corresponding to the flat index.
    """
    indlistlen = len(array_shape)
    doneindex = []
    geht = flat_index
    for zahlx in range(indlistlen):
        geht1 = geht // array_shape[zahlx]
        bleibt = geht % array_shape[zahlx]
        geht = geht1
        doneindex.append(bleibt)
    return doneindex


def calculate_flat_index_f(nested_index, array_shape):
    r"""
    Calculate the flat index from a given nested index in Fortran order.

    Parameters:
    - nested_index (list): Nested index in Fortran order.
    - array_shape (tuple): Shape of the original array.

    Returns:
    - int: Flat index corresponding to the nested index in Fortran order.
    """
    maxind = len(nested_index) - 1
    array_shape_len = len(array_shape)
    wholeindex = nested_index[maxind]
    for y in range(maxind):
        tmpda = nested_index[y]
        for x in range(y + 1, array_shape_len):
            tmpda = tmpda * array_shape[x]
        wholeindex = wholeindex + tmpda
    return wholeindex


def calculate_flat_index_c(nested_index, array_shape):
    r"""
    Calculate the flat index from a given nested index in C order.

    Parameters:
    - nested_index (list): Nested index in C order.
    - array_shape (tuple): Shape of the original array.

    Returns:
    - int: Flat index corresponding to the nested index in C order.
    """
    maxind = len(nested_index) - 1
    wholeindex = 0
    for y in range(maxind, -1, -1):
        tmpda = nested_index[y]
        for x in range(y - 1, -1, -1):
            tmpda = tmpda * array_shape[x]
        wholeindex = wholeindex + tmpda
    return wholeindex


def calculate_nested_index_c_order(flat_index, array_shape):
    r"""
    Calculate the nested index of a given flat index in C order.

    Parameters:
    - flat_index (int): The flat index to be converted.
    - array_shape (tuple): Shape of the original array.

    Returns:
    - list: List of indices in C order corresponding to the flat index.
    """
    indlistlen = len(array_shape)
    doneindex = []
    geht = flat_index
    for zahlx in range(indlistlen - 1, -1, -1):
        geht1 = geht // array_shape[zahlx]
        bleibt = geht % array_shape[zahlx]
        geht = geht1
        doneindex.insert(0, bleibt)
    return doneindex


def convert_c_to_f_index(c_index, array_shape):
    r"""
    Convert C order to Fortran order and return the corresponding nested index.

    Parameters:
    - c_index (list): Nested index in C order.
    - array_shape (tuple): Shape of the original array.

    Returns:
    - list: Nested index in Fortran order corresponding to the C order index.
    """
    flatind = calculate_flat_index_f(nested_index=c_index, array_shape=array_shape)
    return calculate_nested_index_f_order(flat_index=flatind, array_shape=array_shape)


def convert_f_to_c_index(f_index, array_shape):
    r"""
    Convert Fortran order to C order and return the corresponding nested index.

    Parameters:
    - f_index (list): Nested index in Fortran order.
    - array_shape (tuple): Shape of the original array.

    Returns:
    - list: Nested index in C order corresponding to the Fortran order index.
    """
    flatind = calculate_flat_index_c(nested_index=f_index, array_shape=array_shape)
    return calculate_nested_index_c_order(flat_index=flatind, array_shape=array_shape)
