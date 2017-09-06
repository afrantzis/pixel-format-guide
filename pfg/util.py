import os

def split_every_eight_chars(s):
    return [s[i:i+8] for i in range(0, len(s), 8)]

# Parse component strings of the form: R8G8B8A8
def parse_components_with_mixed_sizes(component_str, default_size=8):
    ret = ""
    current_component = ''
    current_size = 0

    component_size = lambda : current_size if current_size > 0 else default_size

    for c in component_str:
        if c.isdigit():
            current_size = current_size * 10 + int(c)
        else:
            ret = ret + current_component * component_size()
            current_size = 0
            current_component = c

    ret = ret + current_component * component_size()

    return ret

# Parse component strings of the form: RGBA8888
def parse_components_with_separate_sizes(component_str, default_size=8):
    ret = ""
    components = []
    sizes = []

    for c in component_str:
        if c.isdigit():
            if c == '0':
                sizes[-1] = sizes[-1] * 10
            else:
                sizes.append(int(c))
        else:
            components.append(c)

    sizes.extend([default_size] * (len(components) - len(sizes)))

    for c,s in zip(components, sizes):
        ret = ret + c * s

    return ret

def native_to_memory_be(native):
    return split_every_eight_chars(native)

def native_to_memory_le(native):
    byte_list = split_every_eight_chars(native)
    return [b for b in reversed(byte_list)]

def read_documentation(docfile):
    here_path = os.path.realpath(os.path.dirname(__file__))
    doc_path = os.path.join(here_path, "..", "docs", docfile)
    doc = ""

    with open(doc_path) as f:
        doc = f.read()

    return doc
