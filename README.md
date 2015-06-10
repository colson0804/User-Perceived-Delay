# Predicting User Perceived Delay
We predict user perceived delay using a dependency graph. We automate the process of calculating user perceived delay to any given url at various bandwidths. Our scripts can graph, perform regressions on, and perform a naive baives classification on rtt vs. bandwidth vs. url size vs. user perceived delay.


## Required packages
1. pip
   install pip at https://bootstrap.pypa.io/get-pip.py

2. mitmproxy:
The proxy you will use.
```
pip install mitmproxy
```

3. Network Link Conditioner: YANG PLEASE FILL THIS IN
Control the bandwidth and other network condition.Download at https://developer.apple.com/downloads/index.action?q=Network%20Link%20Conditioner#

4. Bro:
Monitor all the traffic.

5. Pandas, MatplotLib, and Scikitlearn:
Python packages for performing the regression and graphing the data 

## Set Up and Example using Wall Street Journal
1. Clone the repo: `git clone https://github.com/colson0804/User-Perceived-Delay.git`
2. Run '/Applications/Firefox.app/Contents/MacOS/firefox -p' from the command line, then create two firefox profiles from the window that opens
  - One of these profiles should be entitled proxy and the other should be entitled no proxy
  - Disable proxies for the no proxy profile
  - Add the paths to these two profiles to the air_configure file
3. run proxy visit and get logs
  ```
  python firefox-driver.py -f proxyvisit  -fu http://www.wsj.com -t 15 -c air_configure -p WSJ
  ```
4. get common urls
          running firefox for several times with 
          input: first url
          output: common url list
```
 python LogAnalysis.py -f getcommonurl -d logs -p WSJ -ho test          
```
5. get dependency graph
          run firefox multiple times with proxy, each time, one url will be suspended for a long time and these urls are from common url list
          input: common url list
          output: dependency graph
```
python LogAnalysis.py -f generategraph -p WSJ -d ./logs/ -fu http://www.wsj.com/ -go wsjGraph -lu
http://video-api.wsj.com/api-video/player/v2/css/wsjvideo.min.css -c wsjHostList  
```
6. calculate user-perceived delay in different network conditions
          On each network condition, run firefox multiple times without proxy, use bro to monitor, record important information of traffic and get bro log. Then analyze bro log using script.
          input: common url list, dependency graph, first url, last url
          output: user perceived delay for each network condition
```
sudo bro -i en0 -C httpinfo.bro > test.txt
python LogAnalysis.py -f analyzebrolog -fu http://www.wsj.com/ -lu http://video-api.wsj.com/api-video/player/v2/css/wsjvideo.min.css -gi wsjGraph -c wsjHostList -b broscript/test.txt
```

## Automation:
1. The above steps are automated by the Automate.py script
  - Run Automate.py to automate the above steps
  - After running Automate.py once, you may comment out the automate_driver function because the dependency graph will already have been generated
  - The automate_analyze script will continue to open a website and collect data on its latency, rtt, and url size
  - The script will run five trials for each iteration and will output the average of the 5 trials into a text file in a json format. These files are saved in the equalbd or diffbd directory. You may change what directory the files are saved in and what their title is at line 59 of Automate.py that says output = open("%dkb_output.txt" % bandwidth, "a+")
  - In order to change the bandwidth automatically between each iteration, input the bandwidths you want (in kb) into the bandwidth array at the bottom of the file

## Graphing and Regression **** Can you fill this in Craig?
1. Run the plot.py function within the equalbd or diffbd in order to graph your data and perform a regression on it. Furthermore, calling the pad.py function will pad your data so that each file has an equal number of rtt values; this is only a problem if some of your essential urls are unstable and are not found upon each request.
 
## Naive Bayes ******* Can you fill this in Yang?

