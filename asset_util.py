def validate_name(name):
    if len(name) < 4 or len(name) > 64:
        return False
    if not name[0].isalnum():
        return False
    chars = set(name)
    if '_' in chars:
        chars.remove('_')
    if '-' in chars:
        chars.remove('-')
    return "".join(chars).isalnum()

valid_asset_class_types = {
    'satellite': set(('dove', 'rapideye', 'skysat')),
    'antenna': set(('dish', 'yagi'))
}

def validate_asset(asset):
    try:
        if not validate_name(asset['name']):
            return False
        if asset['type'] not in valid_asset_class_types:
            return False
        return asset['class'] in valid_asset_class_types[asset['type']]
    except KeyError:
        return False

def construct_mapping(valid_asset_class_types):
    idx = 0
    mapping = {}
    inverse = {}
    for type_key in valid_asset_class_types:
        for class_key in valid_asset_class_types[type_key]:
            mapping[(type_key, class_key)] = idx
            inverse[idx] = (type_key, class_key)
            idx += 1
    return mapping, inverse

asset_mapping, asset_inverse = construct_mapping(valid_asset_class_types)

def compress_asset(asset):
    return asset_mapping[(asset['type'], asset['class'])]

def decompress_asset(name, compressed_asset):
    type_val, class_val = asset_inverse[compressed_asset]
    return {
        'name': name,
        'type': type_val,
        'class': class_val
    }
