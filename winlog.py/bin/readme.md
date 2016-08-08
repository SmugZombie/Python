
<pre>
usage: winlog.exe [-h] --application APPLICATION [--eventid EVENTID]
                 [--category CATEGORY] [--type TYPE] [--logtitle LOGTITLE]
                 --rawlog RAWLOG

optional arguments:
  -h, --help            show this help message and exit
  --application APPLICATION, -a APPLICATION
                        Name of the application to be logged as
  --eventid EVENTID, -e EVENTID
                        Specific Event Id for forwarded log (Default 1)
  --category CATEGORY, -c CATEGORY
                        Specific Event Category for forwarded log (Default 5)
  --type TYPE, -t TYPE  Type of Log (Information / Error / Warning) (Default
                        Information)
  --logtitle LOGTITLE, -lt LOGTITLE
                        Title of forwarded log
  --rawlog RAWLOG, -r RAWLOG
                        Raw contents of forwarded log
</pre>
