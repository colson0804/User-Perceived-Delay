# Predicting User Perceived Delay
We predict user perceived delay using a dependency graph.


## Required packages
1. pip
   install pip at https://bootstrap.pypa.io/get-pip.py

2. mitmproxy:
The proxy you will use.
```
pip install mitmproxy
```

3. Network Link Conditioner:
Control the bandwidth and other network condition.Download at https://developer.apple.com/downloads/index.action?q=Network%20Link%20Conditioner#

4. Bro:
Monitor all the traffic.

5. ipfw:
programmatically control the bandwidth and other network condition.

## Set Up
1. Clone the repo: `git clone https://github.com/colson0804/User-Perceived-Delay.git`
2. Run '/Applications/Firefox.app/Contents/MacOS/firefox -p' from the command line, then create two firefox profiles from the window that opens
  - One of these profiles should be entitled proxy and the other should be entitled no proxy
  - Disable proxies for the no proxy profile
  - Add the paths to these two profiles to the air_configure file

Scripts:
proxy-script.py: inline script of mitmproxy
firefox-driver.py: selenium script
LogAnalysis.py: create dependecy graph based on bro traces

## Brief steps

Take Wall street journal (http://www.wsj.com) for example. 
1. Set firefox proxy profile

2. run proxy visit and get logs
  ```
  python firefox-driver.py -f proxyvisit  -fu http://www.wsj.com -t 15 -c air_configure -p WSJ
  ```
3. get common urls
          running firefox for several times with 
          input: first url
          output: common url list
```
 python LogAnalysis.py -f getcommonurl -d logs -p WSJ -ho test          
```
4. get dependency graph
          run firefox multiple times with proxy, each time, one url will be suspended for a long time and these urls are from common url list
          input: common url list
          output: dependency graph
```
python LogAnalysis.py -f generategraph -p WSJ -d ./logs/ -fu http://www.wsj.com/ -go wsjGraph -lu
http://video-api.wsj.com/api-video/player/v2/css/wsjvideo.min.css -c wsjHostList  
```
5. calculate user-perceived delay in different network conditions
          On each network condition, run firefox multiple times without proxy, use bro to monitor, record important information of traffic and get bro log. Then analyze bro log using script.
          input: common url list, dependency graph, first url, last url
          output: user perceived delay for each network condition
```
sudo bro -i en0 -C httpinfo.bro > test.txt
python LogAnalysis.py -f analyzebrolog -fu http://www.wsj.com/ -lu http://video-api.wsj.com/api-video/player/v2/css/wsjvideo.min.css -gi wsjGraph -c wsjHostList -b broscript/test.txt
```

## Automation:
1. The above steps in Brief Steps are automated by the Automate.py script
  - Run Automate.py to automate the above steps
  - After running Automate.py once, you may comment out the automate_driver function because the dependency graph will already have been generated
  - The automate_analyze script will continue to open a website and collect data on its latency, rtt, and url size
  - The script will run five trials for each iteration and will output the average of the 5 trials into a text file in a json format. These files are saved in the equalbd directory
  - In order to change the bandwidth automatically between each iteration, input the bandwidths you want (in kb) into the bandwidth array at the bottom of the file

## Known Bugs and Limitations
- PocketAssistant is currently compatible with iOS devices only
- After authenticating with google calendar on the initial app startup, you must restart the application.
- Suggestions are not context dependent, and are made in only 1 hour and 30 minute time blocks.
- You currently cannot log out of the Google account associated with the application without deleting the application altogether.
