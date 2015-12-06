#!/usr/bin/python

from __future__ import division

import sys, getopt
from meekstv import Blt
import meekstv as stv

def main(argv):
   inputfile = ''
   excludenamedcands = ''
   excands = ''
   exvotes = ''
   quiet = True
   candidatesonly = False
   stopatballot = 0
   ignorevotesfilter = 0
   bumpvotes = 0
   bumpvotesnum = 0
   url = ""
   try:
      opts, args = getopt.getopt(argv,"vf:",["excands=","excludenamedcands=","exvotes=","filename=","url=","candidatesonly","stopatballot=","ignorevotesfilter=","bumpvotes=","bumpvotesnum="])
   except getopt.GetoptError:
      print __file__ +" --excands <inputfile> --exvotes <outputfile>"
      sys.exit(2)
   for opt, arg in opts:
     
      #print opt, arg
     
      if opt == '-h':
         print 'test.py --excands <idx,...> --exvotes <idx,...> --excludenamedcands <PersonA,PersonB...>'
         sys.exit()
      elif opt in ("--candidatesonly"):
         candidatesonly = True
      elif opt in ("-f", "--filename"):
         inputfile = arg
      elif opt in ("--url"):
         url = arg
      elif opt in ("-v", "--verbose"):
         quiet = False
      elif opt in ("--excludenamedcands"):
         excludenamedcands = arg
      elif opt in ("--stopatballot"):
         stopatballot = int(arg)
      elif opt in ("--ignorevotesfilter"):
         ignorevotesfilter = int(arg)
      elif opt in ("--excands"):
         excands = arg
      elif opt in ("--exvotes"):
         exvotes = arg
      elif opt in ("--bumpvotes"):
         bumpvotes = int(arg)
      elif opt in ("--bumpvotesnum"):
         bumpvotesnum = int(arg)
   
   if  (not (inputfile or url)):
      print 'test2.py --excands <idx,...> --exvotes <idx,...> --excludenamedcands <PersonA,PersonB...>'
      sys.exit()
   
   if not quiet:      
     print ">>>======================"
     print 'Excluded candidates are: ', excands
     print 'Removed votes are: ',       exvotes
     print 'Exclude Named Cands: ',     excludenamedcands
     print 'inputfile votes are: ',     inputfile
     print 'quiet is: ',                "True" if quiet else "False"
     print "<<<======================"

   if inputfile:
     blt = Blt(inputfile,excands,exvotes,excludenamedcands)
   elif url:
     
     import urllib2
     response = urllib2.urlopen(url)
     html = response.read()
     
     import tempfile
     with tempfile.NamedTemporaryFile(delete=False) as temp:
       temp.write(html)
       temp.close()
     
     blt = Blt(temp.name,excands,exvotes,excludenamedcands)

   if candidatesonly:
     blt.show_candidates()
     sys.exit()

   if ignorevotesfilter:
     
     ballots = blt.all_ballots()
     ballots2 = []
     

     print( "filtering "+blt.candidates()[ignorevotesfilter] )
     for foo in ballots:
       #print foo
       if foo[0] != ignorevotesfilter:
         ballots2.append(foo)
         

     
     
     
     blt.set_ballots(ballots2)
     
     
     
   if stopatballot:
     elected,rejected,candidate_weight = stv.mainthing3(blt, stopatballot, quiet)

   
   else:
     dq = stv.droop_quota(blt.num_valid_ballots(),blt.places())        
     
     elected,rejected,candidate_weight = stv.mainthing2(blt, quiet)


if __name__ == "__main__":
   main(sys.argv[1:])


   
