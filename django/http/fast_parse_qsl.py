MAX_PARAMS_KEYS = 10000

_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a+b, chr(int(a+b,16)))
                 for a in _hexdig for b in _hexdig)

def unquote(s):
    """unquote('abc%20def') -> 'abc def'."""
    res = s.split('%')
    # fastpath
    if len(res) == 1:
        return s
    s = res[0]
    for item in res[1:]:
        try:
            s += _hextochr[item[:2]] + item[2:]
        except KeyError:
            s += '%' + item
        except UnicodeDecodeError:
            s += unichr(int(item[:2], 16)) + item[2:]
    return s
    
def parse_qsl(qs, keep_blank_values=0, strict_parsing=0):
    # Empey query string return empty list
    if qs.strip() == "":
        return []
    start = 0
    qslen = len(qs)
    i = 0
    r = []
    while i < MAX_PARAMS_KEYS:
        pos = qs.find("&", start)
        if pos < 0 and pos < qslen:
            pos = qslen
        and_splited = qs[start:pos]
        name_values = and_splited.split(";")

        for name_value in name_values:
            if not name_value and not strict_parsing:
                continue
            nv = name_value.split('=', 1)
            if len(nv) != 2:
                if strict_parsing:
                    raise ValueError, "bad query field: %r" % (name_value,)
                # Handle case of a control-name with no equal sign
                if keep_blank_values:
                    nv.append('')
                else:
                    continue
            if len(nv[1]) or keep_blank_values:
                name = unquote(nv[0].replace('+', ' '))
                value = unquote(nv[1].replace('+', ' '))
                r.append((name, value))
            i += 1
        start = pos + 1
        if start > qslen:
            break
    return r