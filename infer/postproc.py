import sys


dir_path = sys.argv[1]
quality_type = sys.argv[2]

f = open("%s/infer.out" % dir_path, 'r')
data = [line.strip() for line in f]
hyp_list = [line.split("\\n")[0] for line in data]
if quality_type == "label":
    label_list = [line.split("\\n")[1][1:-1] if len(line.split("\\n")) > 1 else "Bad" for line in data]
else:
    label_list = [line.split("\\n")[1][1:-1] if len(line.split("\\n")) > 1 else "0" for line in data]

# hyp_file = open(f"{dir_path}/hyp.txt", 'w')
hyp_file = open("%s/hyp.txt" % dir_path, 'w')
for hyp in hyp_list:
    hyp_file.write(hyp + "\n")

label_file = open("%s/label.txt" % dir_path, 'w')
for label in label_list:
    label_file.write(label + "\n")
