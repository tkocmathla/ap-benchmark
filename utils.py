import micronap.sdk as ap

def ste_chain(anml_net, symbols, head_props={}, tail_props={}):
    chain = []
    for i, sym in enumerate(symbols):
        if i == 0:
            ste = anml_net.AddSTE(sym, **head_props)
        elif i == len(symbols) - 1:
            ste = anml_net.AddSTE(sym, **tail_props)
            anml_net.AddAnmlEdge(last_ste, ste)
            anml_net.AddAnmlEdge(ste, ste)
        else:
            ste = anml_net.AddSTE(sym)
            anml_net.AddAnmlEdge(last_ste, ste)
            anml_net.AddAnmlEdge(ste, ste)
        chain.append(ste)
        last_ste = ste
    return chain
