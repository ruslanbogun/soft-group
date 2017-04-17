import re

string_1 = "afoot, catfoot, dogfoot, fanfoot, foody, foolery, foolish, fooster, footage, foothot, footle, " \
           "footpad, footway, hotfoot, jawfoot, mafoo, nonfood, padfoot, prefool, sfoot, unfool"
string_2 = "Atlas, Aymoro, Iberic, Mahran, Ormazd, Silipan, altered, chandoo, crenel , crooked, fardo, " \
           "folksy, forest, hebamic, idgah, manlike, marly, palazzo, sixfold, tarrock, unfold"

PATTERN = "[A-Za-z]{0,}foo[A-Za-z]{0,}"

print(re.findall(PATTERN, string_1))
print(re.findall(PATTERN, string_2))
