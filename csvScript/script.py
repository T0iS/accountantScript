import pandas as pd
import os
import csv
import math
import glob, os


dobirky = 0
nesedi = 0
nes = []

print("............SCRIPT STARTING..............")

df = pd.concat(
    [pd.read_csv(f, sep=";", encoding="utf-8") for f in glob.glob("zasilkovna/*.csv")],
    ignore_index=True,
)
df.to_csv("combined.csv", index=False, sep=";", encoding="utf-8")


with open("faktury.csv", encoding="Latin-1") as s:
    check = csv.reader(s, delimiter=";", quotechar='"')

    for c in check:
        if c[0] == "Cislo faktury":
            c.append("Cena s DPH")
        else:
            dph = float(c[5]) * 1.21
            c.append(str(math.ceil(dph)))

        fa = open("combined.csv", encoding="utf8")  # zasilkovna
        fak = csv.reader(fa, delimiter=";", quotechar='"')
        for row in fak:
            if row and c and row[4] == c[4]:
                row[12] = row[12].replace(",", ".")
                row[12] = row[12].replace(" ", "")
                row[19] = row[12].replace(",", ".")
                row[19] = row[12].replace(" ", "")
                if int(float(row[12])) == int(float(c[6])) or int(float(row[19])) == 0:
                    print("OK ", row[4])
                    dobirky += int(float(row[12]))
                elif row[19] == "vratka":
                    print("vratka ", row[4])
                else:
                    # print(row[4], " ", int(float(row[12])), "neni", int(float(c[6])))
                    print("NESEDI CASTKA ", row[4])
                    nes.append(row[4])
                    nesedi += 1
        fa.close()

print("\nCastka za dobirky celkem", dobirky)
print("\nCastka nesedi u ", nesedi, " zasilek\n")

if nes != []:
    with open("nesrovnalosti.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        for z in nes:
            writer.writerow([z])
            print(z)
print("Press key to exit.")
input()
