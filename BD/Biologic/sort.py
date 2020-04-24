
reads = []

with open("tmp.txt", "r", encoding = "utf-8") as cin:
    reads = cin.readlines()

reads.sort()

with open("tmp.txt", "w", encoding = "utf-8") as out:
    for i in reads:
        out.write(i)