def filer_func(emails):
    is_a = list(filter(lambda a: a.count("@") == 1, emails))
    is_n = list(filter(lambda e: e.split("@")[0].lower().replace("_", "").isalnum(), is_a))
    is_d_s = list(filter(lambda d: not d.split("@")[1].startswith("."), is_n))
    is_d_e = list(filter(lambda d: not d.split("@")[1].endswith("."), is_d_s))
    is_d = list(filter(lambda d: d.split("@")[1].count(".") > 0, is_d_e))
    is_t = list(filter(lambda t: [s for s in t.split(".")], is_d))
    is_v = list(filter(lambda v: all(True if len(s) >= 2 else False for s in v.split("@")[1].split(".")), is_t))
    return is_v


emails = ['abc@gmail.com.ua', '*@ank.com', '_ny@us.gov.us', 'z@b.kk', 'df@fut@.cc.bz', 'df@.rt.ts', 'sff@com',
          'dfs@dfd.dff.', 'sdadas@11.1']

s = filer_func(emails)
print(s)
