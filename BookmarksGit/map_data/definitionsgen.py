import random


end = 16500 #until which number do you want me to generate lines for definiton.csv ?
path = r"C:\Users\warlo\Documents\Paradox Interactive\Crusader Kings III\mod\MoreBookmarks\map_data\definition.csv"


with open(path, "r", encoding="utf-8") as f:
    content = f.read().splitlines()
    f.close()
used_rgb_values = []
for line in content:
    current_line = line.split(";")
    old_rgb = (current_line[1],current_line[2],current_line[3])
    #if rgb not in repaint_rgb_codes:
    used_rgb_values.append(old_rgb)
    last_province_in_file = current_line[0]

start = int(last_province_in_file)
for i in range(start+1, end + 1):
    rgb = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
    if (rgb in used_rgb_values):
        print("Value aready exists")
    else:
        print(f"{i};{rgb[0]};{rgb[1]};{rgb[2]};b_test_{i};x")
        used_rgb_values.append(rgb)
else:
    print("Finally finished!")