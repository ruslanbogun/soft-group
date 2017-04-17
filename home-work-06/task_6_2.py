import re

string_1 = "fu, tofu, snafu"
string_2 = "futz, fusillade, functional, discombobulated"

PATTERN = "([a-z]{1,}fu)[^a-z]{0,}|([a-z]{0,}fu)[^a-z]"

print(re.findall(PATTERN, string_1))
print(re.findall(PATTERN, string_2))
