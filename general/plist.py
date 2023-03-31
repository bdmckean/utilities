import sys

out_fn = 'list_o.txt'
out_str = ""
in_fn = sys.arg[1]
with open(in_fn, "r") as fp:
    for line in fp:
        this_item = "".join([x for x in line if (x.isalnum() or x in ['_', '-'] )])
        this_item = "'" + this_item + "',\n"
        out_str += this_item
    out_str = out_str[:-2]
    print(out_str)
        
