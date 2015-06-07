import string 
import os
import json
import math

def updateJsonFile(json_file, data):
    jsonFile = open(json_file, "w")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def convert():
    for ii in os.listdir(os.getcwd()):
        i = os.path.join(ii, "diffbd")
	if i.endswith(".txt"):
            f = open(i, "r")
            remove_extension = string.strip(i, ".txt")
            print i 
	
            x = json.load(f)
            f.close()
            new_name = "diffbd/%st.json" % remove_extension
            d = {}
            d["num_urls"] = int(math.ceil((len(x) - 2) / 2))
            d["latency"] = x["latency"]
            rtt_times_size = 0

            if "rtt" in x:
                rtt_times_size = rtt_times_size + x["rtt"]  * x["size"]                    
            else:
                for j in range(0, d["num_urls"]):
                    rtt_index = "avg_rtt%d" % j
                    size_index = "avg_size%d" % j
                    rtt_times_size = rtt_times_size + x[rtt_index] + x[size_index]

            d["rtt*size"] = rtt_times_size
            
            updateJsonFile(new_name, d)
        else:
            continue

if __name__ == '__main__':
    convert()
