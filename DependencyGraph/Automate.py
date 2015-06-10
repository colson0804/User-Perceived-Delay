import datetime
import subprocess
import shlex
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urlparse import urlparse
import time
import requests
import logging
import sys
import json
import os
import subprocess
import psutil
import argparse
import time
import threading


def automate_driver(file_name):
    # call firefox-driver.py from the command line to query a given url 15 times
    driver = shlex.split("python firefox-driver.py -f proxyvisit -fu http://www.cnn.com -t 15 -c air_configure -p CNN")
    if subprocess.call(driver) != 0:
    	sys.exit()

    # call LogAnalysis.py from the command line to get the common urls from the output of firefox-driver
    commonurl = shlex.split("python LogAnalysis.py -f getcommonurl -d logs -p CNN -ho cnnHost")
    subprocess.call(commonurl)

    # call LogAnalysis.py from the command line to generate a dependency graph from the common urls
    graph = shlex.split("python LogAnalysis.py -f generategraph -p WSJ -d ./logs/ -fu http://www.cnn.com/ -go cnnGraph -lus finals.txt -c cnnHost")
    subprocess.call(graph)

def automate_analyze(host_name, graph_name, last_url, bandwidth, trial_num):
    bandwidth_in_bits = bandwidth * 8

    # set the bandwidth to the desired bandwidth (based on the value in the bandwidth array)
    dnctl = shlex.split("sudo wondershaper eth0 %d 5120" % bandwidth)
    subprocess.call(dnctl)

    # collecting data...
    url = "http://www.cnn.com/"             
    profile = webdriver.FirefoxProfile("/home/ubuntu/.mozilla/firefox/8ld7gd0a.withoutProxy")

    # call bro from the command line to monitor the network traffic, pipe the output into test.txt
    f = open("broscript/test.txt", "w")
    listen = shlex.split("sudo /usr/local/bro/bin/bro -i eth0 -C broscript/httpinfo.bro")
    browser = webdriver.Firefox(profile)
    background = subprocess.Popen(listen, stdout = f)

    # open a browser and request the desired url while bro runs in the background, then terminate bro
    openNewTab(browser)
    browser.get(url)

    time.sleep(1)
    try:
        background.terminate()
    except:
        # handle error where we can't terminate bro
        print "cannot terminate bro"
        browser.quit()
        f.close()
        automate_analyze(host_name, graph_name, last_url, bandwidth, trial_num)
        return
    f.close()
    try:
        closeCurrentTab(browser)
    except:
        # handle error where we can't terminate bro
        print "cannot close current tab"
        browser.quit()
        automate_analyze(host_name, graph_name, last_url, bandwidth, trial_num)
        return
    browser.quit()

    # call LogAnalysis.py to output our data on latency, rtt, and url size into a text file within the diffbd directory
    output = open("diffbd%d/%dtest.txt" % (trial_num, bandwidth), "w")
    analyze = shlex.split("python LogAnalysis.py -f analyzebrolog -fu http://www.cnn.com/ -lus " + last_url + " -gi " + graph_name + " -c " + host_name + " -b broscript/test.txt")
    subprocess.call(analyze, stderr = output)
    output.close()
        
    output = open("diffbd%d/%dtest.txt" % (trial_num, bandwidth), "r")
    output_string = output.read()
    if len(output_string) < 10:
        print "Output File is empty"
        output.close()
    	automate_analyze(host_name, graph_name, last_url, bandwidth, trial_num)
        return

    output.close()
    clearm = shlex.split("sudo wondershaper remove eth0")
    subprocess.call(clearm)

def openNewTab(browser):
	if sys.platform == "darwin":
		ActionChains(browser).send_keys(Keys.COMMAND, "t").perform()
		ActionChains(browser).send_keys(Keys.COMMAND, "t").perform()
	elif sys.platform == "linux2":
		ActionChains(browser).send_keys(Keys.CONTROL, "t").perform()
		ActionChains(browser).send_keys(Keys.CONTROL, "t").perform()
	else:
		logger.error("openNewTab unsupported OS: %s"%sys.platform)

def closeCurrentTab(browser):
	if sys.platform == "darwin":
		browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
	elif sys.platform == "linux2":
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
	else:
		logger.error("closeCurrentTab unsupported OS: %s"%sys.platform)
    

if __name__ == '__main__':
    host_name = sys.argv[1]
    graph_name = sys.argv[2]
    last_urls = "finals.txt" 
    
    # set the desired bandwidths
    bandwidth = range(64000, 8000, -8000)

    # set the number of trials to collect data for at each given bandwidth, the data collected at each of these trials will be averaged and outputted into one file
    num_trials = 5
    for i in bandwidth:
        rtt = []
        size = []
        avg_rtt = []
        avg_size = []
        # initialize the lists that store rtt and size
        for k in range(0, 200):
            rtt.append(0)
            avg_rtt.append(0)
            size.append(0)
            avg_size.append(0)
        latency = 0
        j = 0
        skip = False
        # perform multiple trials to collect the data
        while j < num_trials:
            skip = False
            j = j + 1
            print j
            # call automate_analyze to collect the data
            automate_analyze(host_name, graph_name, last_urls, i, j)
            f = open("diffbd%d/%dtest.txt" % (j, i), "r")
            x = json.load(f)
            num_rtt_data = len(x['files'])
            single_latency = 0
            for k in range(0, num_rtt_data):
                # check if the data is an outlier and discard it if so
                if x['files'][k]["latency"] < 0.15 or x['files'][k]["rtt"] < 0.00001 or x['files'][k]["latency"] > 20:
                    print "problem with data range"
                    j = j - 1
                    skip = True
                    break
                # parse the data
                if x['files'][k]['latency'] > single_latency:
                    single_latency = x['files'][k]['latency']
                rtt[k] += x['files'][k]["rtt"]
                size[k] += x['files'][k]["size"]
            if skip: 
                f.close()
                continue
            # parse the data
            latency += single_latency
            f.close()

        # average out the data over all the trials and output into a text file in json format
        avg_latency = latency / num_trials
        data_dictionary = {"latency":avg_latency, "time":datetime.datetime.now().hour}
        for k in range(0, num_rtt_data):
            avg_rtt[k] = rtt[k] / num_trials
            avg_size[k] = size[k] / num_trials
            rtt_index = 'avg_rtt%d' % k
            size_index = 'avg_size%d' % k
            data_dictionary[rtt_index] = avg_rtt[k]
            data_dictionary[size_index] = avg_size[k]
        avg_file = open('diffbd/%dtest.txt' % i, 'w')
        json.dump(data_dictionary, avg_file)
        avg_file.close()

