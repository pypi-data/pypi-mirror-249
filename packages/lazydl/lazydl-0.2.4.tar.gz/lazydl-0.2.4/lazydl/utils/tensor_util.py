import torch.nn.functional as F


def pad_tensor(a, b, pad_side="left", pad_value=0):
    """按照 pad_side 填充两个向量至长度相等

    Args:
        a (_type_): _description_
        b (_type_): _description_
        pad_side (str, optional): _description_. Defaults to "left".
        pad_value (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    if a.shape[-1] == b.shape[-1]:
        return a, b
    a_len = a.shape[-1]
    b_len = b.shape[-1]
    if a_len > b_len:
        pad_len = a_len - b_len
        if pad_side == "left":
            padding = (pad_len, 0)
        else:
            padding = (0, pad_len) 
        b = F.pad(b, padding, 'constant', pad_value)
    elif a_len < b_len:
        pad_len = b_len - a_len
        if pad_side == "left":
            padding = (pad_len, 0)
        else:
            padding = (0, pad_len) 
        a = F.pad(a, padding, 'constant', pad_value)
        
    return a, b