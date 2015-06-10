import os
import json

def getNumUrls():
    max_num_urls = 0
    for i in os.listdir(os.getcwd()):
        if i.endswith(".txt"):
            f = open(i, "r+")
            x = json.load(f)
            if len(x) > max_num_urls:
                max_num_urls = len(x)
            f.close()
        else:
            continue
    return max_num_urls - 2

def updateJsonFile(json_file, data):
    jsonFile = open(json_file, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def pad():
    max_num_urls = getNumUrls()
    for i in os.listdir(os.getcwd()):
        if i.endswith(".txt"):
            f = open(i, "r+")
            x = json.load(f)
            f.close()
            x["num_urls"] = max_num_urls
            index = len(x) - 3
            last_index = index - 1
            last_value = 'avg_rtt%d' % last_index
            pad_value = x[last_value]
            while index < max_num_urls:
                cur = 'avg_rtt%d' % index
                x[cur] = pad_value
                index = index + 1
            updateJsonFile(i, x)
        else:
            continue

if __name__ == '__main__':
    pad()
