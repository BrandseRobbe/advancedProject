# breed= ["a","b","c","d","a","b"]
# breed = list(dict.fromkeys(breed))
# print(breed)
# print(type(breed))

import pandas as pd

table = [["Domestic Shorthair Mix", "5 years", "Brown Tabby/White"], ["Cocker Spaniel", "8 years", "Brown"], ["Flat Coat Retriever/Papillon", "1 month", "Brown"],
         ["Domestic Shorthair Mix", "2 months", "Black/White"], ["Domestic Shorthair Mix", "5 years", "Blue Tabby"], ["Bull Terrier Mix", "1 year", "Black/White"],
         ["Jack Russell Terrier/Rat Terrier", "2 years", "White/Tan"], ["Lhasa Apso", "3 years", "White/Black"]]

df = pd.DataFrame(table)
max_len = [df[col].str.len().max() for col in df.columns]
output = []
for row in table:
    rowstring = ""
    for cel in row:
        rowstring += cel + " " * (max_len[row.index(cel)] - len(cel)) + " | "
    output.append(rowstring[:-2])
for row in output:
    print(row)
