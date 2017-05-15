import random

filename = "data/data.csv"
f30 = "data/data-33.txt"
f70 = "data/data-66.txt"

with open(filename, "r") as of, open(f30, "w") as f3, open(f70, "w") as f7:
    lines = of.readlines()

    # put back header
    print(lines[0], file=f3, end='')
    print(lines[0], file=f7, end='')
    lines = lines[1:]
    label = [int(float(line.split(',')[-1])) for line in lines]

   # print(lines, label)
    zipped = list(zip(lines, label))

    class_lines = [[]] * 3
    class_lines[0] = [tup[0] for tup in zipped if tup[1] == 0]
    class_lines[1] = [tup[0] for tup in zipped if tup[1] == 1]
    class_lines[2] = [tup[0] for tup in zipped if tup[1] == 2]

    for li in class_lines:
        random.shuffle(li)

    # write 33%
    stop = [round(len(l) * 0.33) + 1 for l in class_lines]
    all_eles = []
    for i, li in enumerate(class_lines):
        all_eles += li[:stop[i]]
    print("33%%: %d samples." % len(all_eles))
    print(''.join(all_eles), end="", file=f3)

    # write 66%
    stop = [round(len(l) * 0.66) + 1 for l in class_lines]
    all_eles = []
    for i, li in enumerate(class_lines):
        all_eles += li[:stop[i]]
    print("66%%: %d samples." % len(all_eles))
    print(''.join(all_eles), end="", file=f7)



