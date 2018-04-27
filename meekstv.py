#!/usr/bin/env python

from __future__ import division

import numpy as np
np.set_printoptions(precision=2,suppress=True)

import pprint

class Blt(object):
  '''
  The Blt object parses the opavote file into an object with attributes
  containing useful information about the election.
  places() <- returns the int of number of open slots to fill
  candidates() <- returns a list of candidates
  all_ballots() <- list of ballots, which is a list of lists, rank in DESC order

  This is some ridiculous stuff going on in here
  '''
  def __init__(self, inputfile,excands,exvotes,excludenamedcands):
    self.inputfile = inputfile
    self.data = open(inputfile).read().splitlines()
    self.np = int(self.data[0].split(" ")[1])
    self.nc = int(self.data[0].split(" ")[0])

    #print self.nc
    #print self.np

    """The list of exluded ballots is passed as a string, e.g. 0,2,31
    and this needs to be a list to be useful
    The value is passed as the blt index before any other parsing.

    ==    blt file example, candidates are indexed at 1
    (0) 1 16 7 17 8 13 1 4 14 15 19 6 5 9 11 2 10 18 3 12 0
    (1) 1 7 2 4 1 11 15 12 17 6 10 9 18 3 14 8 16 5 19 13 0
    (2) 1 1 4 14 17 10 19 15 13 9 16 8 11 5 18 2 12 3 6 7 0
    ==
    --excands=0,2 would exclude and result in a single ballot
    """
    excluded_ballots_by_index = []

    if exvotes:
      for i in exvotes.split(","):
        excluded_ballots_by_index.append(int(i))

    self.excluded_cands_by_index = []

    if excands:
      for i in excands.split(","):
        self.excluded_cands_by_index.append(int(i.strip()))

    # initialize the start value to some int, this should end up being
    # something like votes+1 in the blt file
    candidates_start_line=0
    start_looking_for_ballots_line=1

    #loop the lines list, starting at line 2, and quit at end marker
    for num in xrange(start_looking_for_ballots_line, len(self.data)):
      # a line containing a single character "0" appears to mark the end
      # of ballots, so loop until we find that.
      if self.data[num] == "0":
        #make a numpy array of the range of lines that are ballots
        #@todo this is still a string?
        self.ballots = np.array(self.data[1:num])

        #store this to use for candidate search after
        candidates_start_line=num+1
        break

    temparr = []
    #print excluded_ballots_by_index
    for i in xrange(len(self.ballots)):
      if i not in excluded_ballots_by_index:
        temparr.append(self.ballots[i])

    self.ballots=temparr

    for excluded_ballot in excluded_ballots_by_index:
      #del self.ballots[excluded_ballot:excluded_ballot]
      self.ballots = np.delete(self.ballots, excluded_ballot)

    #print candidates_start_line
    #print self.ballots

    self.ballots = [ np.array(item.split(" ")) for item in self.ballots ]
    self.ballots = np.array(self.ballots)

    #cols = [ i for i in xrange(self.nc+2) ]
    """A ballot row looks like this for 2014;
    (29) 1 7 12 11 16 15 5 19 10 14 4 8 6 2 3 18 13 17 1 9 0
    where the 0th element is the blt ballot index (@todo use this)
    and the [1] and [-1] element are the start and end of rank markers.
    A 2015 vote looks like this;
    1 12 9 2 4 3 5 11 10 13 6 1 7 8 0
    So remove those unecessary parts"""

    if (self.ballots[0][0].startswith("(")):
      cols = [ i for i in xrange(self.nc+2) if i not in (0,1, self.nc+2) ]
    else:
      cols = [ i for i in xrange(self.nc+1) if i not in (0, self.nc+1) ]

    self.ballots = self.ballots[:, cols]

    buff = []

    """subtract 1 from each ranked cand to match python list indexing"""
    def int_reindex(i):
      return int(i)-1

    for row in range(len(self.ballots)):
        #print  map(int, ballots[row])
        buff.append( map(int_reindex, self.ballots[row]) )

    self.ballots=buff

    #print (np.array(self.ballots).shape)
    # the last line is apparently the title of the election
    c = map(str.rstrip, self.data[candidates_start_line:-1])
    c = [s.strip('"') for s in c]

    #dummy zeroeth candidate
    #self.candidates_list = ["blank-candidates-no-indexed-from-zero"]
    self.candidates_list = []

    for i in range(len(c)):
        self.candidates_list.append(c[i])

    #print "\n".join(self.candidates_list[:])
    #pprint.pprint( self.ballots )

  def places(self):
    return self.np

  def num_candidates(self):
    return self.nc

  def candidates(self):
    '''
    The opavotes ranks are 1 indexed, so this array has a padding zero element
    '''
    return self.candidates_list

  def show_candidates(self):
    for foo in xrange(len(self.candidates_list)):
      buffstr=self.candidates_list[foo]+"("+str(foo)+")"
      print(buffstr.rjust(30))

  def excluded(self):
    '''
    The opavotes ranks are 1 indexed, so this array has a padding zero element
    '''
    return self.excluded_cands_by_index

  def num_valid_ballots(self):
    return len(self.ballots)

  def all_ballots(self):
    return self.ballots

  def set_ballots(self, ballots):
    self.ballots = ballots

  def pr(message):
    if not quiet:
      pass
      print message

  def show_candidates_for_voter(self, num):
    if num:
      self.ballots[int(num)-1]
      cnt=1
      for candidate in self.ballots[int(num)-1]:
        print "("+str(cnt).zfill(2)+")"+self.candidates_list[candidate]
        cnt = cnt+1


  def show_votes_for_candidates(self):

    candidate_list = {}

    for foo in xrange(len(self.candidates_list)):
      candidate_list[foo] = [0] * len(self.candidates_list)

    #print   candidate_list

    for ballot in self.ballots:
      #print ballot
      for pos in xrange(len(ballot)):
        candidate_list[ballot[pos]][pos] = candidate_list[ballot[pos]][pos]+1
        #print "candidate %s was ranked %d" % (self.candidates_list[ballot[pos]], pos)
      #print ""

    for cand in candidate_list:
      print self.candidates_list[cand]
      for foo in xrange(len(candidate_list[cand])):
        #print "position %s had %d votes" % (foo+1, candidate_list[cand][foo])
        print str(candidate_list[cand][foo]) + ("." * candidate_list[cand][foo])


# the opavote system uses a modified droop quota
# http://en.wikipedia.org/wiki/Droop_quota

def droop_quota(vv=350, places=5):
    return vv/(places+1)


stopatballot=0

def mainthing2(blt, quiet=True):
    return mainthing(blt.all_ballots(), blt.places(), blt.candidates(), blt.excluded(), quiet)



def mainthing3(blt, limitnum, quiet=True):
    print "limiting to "+str(limitnum)

    return mainthing(blt.all_ballots()[:limitnum], blt.places(), blt.candidates(), blt.excluded(), quiet)

def mainthing_bumpvotes(blt, limitnum, quiet=True, bumpvotecand=0, bumpvotesnum=0):

    return mainthing(blt.all_ballots(), blt.places(), blt.candidates(), blt.excluded(), quiet, bumpvotecand, bumpvotesnum)


def mainthing(ballots, places, candidates, excluded, quiet=True, bumpcand=0, bumpcandvotes=0):
  """
  candidates has a dummy element at index zero
  """

  def pr(message):
    if not quiet:
      pass
      print message


  for foo in xrange(len(candidates)):
    buffstr=candidates[foo]+"("+str(foo)+")"
    pr(buffstr.rjust(30))





  elected = []
  rejected = []

  #print places

  """initialize a list of 0 for each candidate, respecting that zero
  is a dummy"""
  candidate_votes = [0] * (len(candidates))

  #pprint.pprint( candidate_votes )

  # status 0=hopful, 1=excluded, 2=elected
  candidate_status = [0] * (len(candidates))
  #pprint.pprint( candidate_status )


  candidate_weight = [1] * (len(candidates))
  #pprint.pprint( candidate_weight )



  for ex in excluded:
      candidate_weight[ex] = 0
      candidate_status[ex] = 1

  #multi dir comprehensions
  #buckets = [[0 for col in range(5)] for row in range(10)]

  #print candidate_weight
  #print candidate_votes

  dq = droop_quota(len(ballots[:]),places)

  pr( "==============================================================" )
  pr( "Droop quota is "+str(round(dq,2)) )
  pr( "places is "+str(places) )
  pr( "votes are "+str(len(ballots)) )
  pr( 'excluded candidates are "'+'", "'.join(candidates[v] for v in excluded)+'"' )
  pr( ""  )


  def print_weights(weights):
      for candidate in xrange(len(candidates)):
          pr( candidates[candidate].rjust(20), )
          pr( weights[candidate] )
      pr("")

  def print_votes(votes):
      for candidate in xrange(len(candidates)):
        if(votes[candidate]!=0):
          pr( candidates[candidate].rjust(20) + ":" + str(votes[candidate]) )


  round_num = 1

  while places > 0:


      pr( "Round "+str(round_num)+"  -- candidates remaining >>> "+str(places) +" <<< ")
      round_num = round_num+1

      #print candidates
      candidate_votes = [0] * (len(candidates))

      if bumpcand:
        candidate_votes[bumpcand] = bumpcandvotes

      logout = ""

      for ballot in ballots[:]:

          for candidate in xrange(len(candidates)):

              votebuff=1
              #print "cand "+str(candidate)

              for rank in xrange(len(candidates)):


                  if ballot[rank]==candidate:
                      votebuff *=  candidate_weight[candidate]
                      break
                  else:


                      if(candidate_weight[candidate]!=1):
                          #print "rank="+str(rank),"weight="+ str(candidate_weight[candidate]), "votebuf="+str(votebuff)
                          pass

                      votebuff *=  (1-candidate_weight[ballot[rank]])


              candidate_votes[candidate]        += votebuff



      jumpout = False # we only want to do one elect or elim each cycle

      for candidate in range(len(candidates)):
        #print "comparing "+candidates[candidate]+" votes "+str(candidate_votes[candidate])+" against "+str(dq)
        if candidate_votes[candidate] > dq:
          if(places>0):
            if candidate_status[candidate] != 2:
                logout = candidates[candidate][:21].rjust(20)+": elected with " + str(round(candidate_votes[candidate],4)) + "\n" + logout
                places -= 1
                elected.append(candidate)
                jumpout = True
            candidate_status[candidate] = 2
          candidate_weight[candidate] *= (dq/candidate_votes[candidate])
        if (candidate_weight[candidate]!=1 and candidate_weight[candidate]!=0):
          logout = logout +   ( candidates[candidate][:21].rjust(20)+": updating weight to "+str(round(candidate_weight[candidate],4) )) + "\n"

      #print ( candidate_weight)
      #print ( candidate_votes      )

      if not jumpout:
        if(places>0):
            minVotes=99999
            loserId=0
            for loser in range(len(candidate_status)):



                if(candidate_status[loser]==0):
                    if(candidate_votes[loser]<minVotes):
                        minVotes=candidate_votes[loser]
                        loserId=loser

            rejected.append(loserId)

            candidate_weight[loserId] = 0
            candidate_status[loserId] = 1


            logout = candidates[loserId][:21].rjust(20)+": Candidate eliminated #"+str(loserId)+" " + \
            "with vote count " +str(round(minVotes,4)) + "\n" + logout

      pr("summary of round")
      print_votes(candidate_votes)
      pr ("\n")
      pr(logout)
      pr ("\n")

  pr ("\n")
  #    if ballots[rank]
  for candidate in range(len(candidates)):
          if candidate_status[candidate] == 2:
              print( ("winner "+candidates[candidate] + "("+str(candidate)+") ("+str(round(candidate_weight[candidate],3)) +")").rjust(50) )
          if candidate_status[candidate] == 0:
              pr( ("field "+candidates[candidate] + "("+str(candidate)+") ("+str(round(candidate_weight[candidate],3)) +")").rjust(50) )


  return elected, rejected, candidate_weight


