
# meekstv
`python-meekstv` is a Python 2.7 package implementing [Meeks](https://en.wikipedia.org/wiki/Counting_single_transferable_votes#Meek) 's
[STV](https://en.wikipedia.org/wiki/Single_transferable_vote) ranked voting
algorithm. For the simple case it can be used as follows to show you who would
be elected from a [BLT file](https://www.opavote.com/help/overview#blt-file-format) of voting data;

~~~~
meekstv$ ./main.py \
--url=https://london.hackspace.org.uk/organisation/elections/2015-election-ballots.blt
                    winner Paddy Duncan(2) (0.653)
                     winner Dean Forbes(3) (0.775)
                     winner Andy Tidman(9) (0.766)
                winner Charles Yarnold(11) (0.555)
~~~~

## File format

The [BLT file](https://www.opavote.com/help/overview#blt-file-format) contains the data on the number/names of candidates, the number of
seats being contested, and each individual (anonymized) vote. From this data the
result of the election can be reconstructed.

The file format looks like
this;

~~~~
19 5
(0) 1 16 7 17 8 13 1 4 14 15 19 6 5 9 11 2 10 18 3 12 0
(1) 1 7 2 4 1 11 15 12 17 6 10 9 18 3 14 8 16 5 19 13 0
...
(299) 1 17 12 1 14 8 6 3 16 5 13 7 10 11 4 15 9 2 18 19 0
0
"Candidate 1"
...
"Candidate N"
"NO FURTHER PLACES"
"Trustees Election"
~~~~

## Usage

The purpose of this module is largely to allow investigating `what if X?`
scenarios for voting results. There are also options for fixing incomplete data
in the voting entries.

For example to fix a row with missing data,
`--exvotes=N,M,` will exclude those votes from the calculations;

~~~~
meekstv$ ./main.py --exvotes=173  --url=https://london.hackspace.org.uk/organisation/elections/2015-election-ballots.blt
                winner Paddy Duncan(2) (0.651)
                 winner Dean Forbes(3) (0.771)
                 winner Andy Tidman(9) (0.756)
            winner Charles Yarnold(11) (0.549)
~~~~

This option was required for that data file, because vote 173 was blank;

~~~~
(172) 1 17 7 15 12 13 19 9 14 1 2 6 18 5 16 11 8 10 4 3 0
(173) 1  0
(174) 1 13 17 6 10 9 12 15 16 7 11 2 4 8 19 14 3 18 1 5 0
~~~~

If you want to see how each round of the voting played out, give the `-v` option
and each elimination and election is shown in full;

~~~~
>>>======================
Excluded candidates are:
Removed votes are:  173
Exclude Named Cands:
inputfile votes are:
quiet is:  False
<<<======================
              Martin Clarke(0)
                   Sam Cook(1)
               Thomas Greer(2)
         Matthew Israelsohn(3)
                 Nick Large(4)
               Ruben Martin(5)
           Eugene Nadyrshin(6)
                Lucia Naidu(7)
              Blanca Regina(8)
               Tim Reynolds(9)
                Philip Roy(10)
               Henry Sands(11)
                Ryan Sayre(12)
            David Sullivan(13)
          Heather Sullivan(14)
         Samantha Thompson(15)
             Jonty Wareing(16)
                 Tom Wyatt(17)
         NO FURTHER PLACES(18)
==============================================================
Droop quota is 49.67
places is 5
votes are 298
...
  Matthew Israelsohn: elected with 52.8172
  Matthew Israelsohn: updating weight to 0.9404
    Eugene Nadyrshin: updating weight to 0.7678
         Lucia Naidu: updating weight to 0.9942
   Samantha Thompson: updating weight to 0.8735
       Jonty Wareing: updating weight to 0.4348

               winner Matthew Israelsohn(3) (0.94)
                winner Eugene Nadyrshin(6) (0.768)
                     winner Lucia Naidu(7) (0.994)
              winner Samantha Thompson(15) (0.873)
                  winner Jonty Wareing(16) (0.435)
~~~~


Another scenario that is interesting, is to consider how votes are reallocated
if some pariticular candidate was hypothetically withdrawn;

First we find the number for the candidate;

~~~~
./main.py --candidatesonly --exvotes=173  --url=https://london.hackspace.org.uk/organisation/elections/2014-election-ballots.blt
              Martin Clarke(0)
                   Sam Cook(1)
               Thomas Greer(2)
         Matthew Israelsohn(3)
                 Nick Large(4)
               Ruben Martin(5)
           Eugene Nadyrshin(6)
                Lucia Naidu(7)
              Blanca Regina(8)
               Tim Reynolds(9)
                Philip Roy(10)
               Henry Sands(11)
                Ryan Sayre(12)
            David Sullivan(13)
          Heather Sullivan(14)
         Samantha Thompson(15)
             Jonty Wareing(16)
                 Tom Wyatt(17)
         NO FURTHER PLACES(18)
~~~~

and then we exclude that candidate (i.e. if the candidate had withdrawn after
voting had started, but before results were counted.

~~~~
./main.py  --excands=7 --exvotes=173  --url=https://london.hackspace.org.uk/organisation/elections/2014-election-ballots.blt
              winner Matthew Israelsohn(3) (0.695)
                winner Eugene Nadyrshin(6) (0.565)
                   winner Blanca Regina(8) (0.801)
              winner Samantha Thompson(15) (0.629)
                  winner Jonty Wareing(16) (0.365)
~~~~

In addition, we can pick a particular candidate and bump their vote tally to see
how many more votes they would have need for them to have been elected;

~~~~
./main.py  --bumpvotecand=4 --bumpvotesnum=4  \
--url=https://london.hackspace.org.uk/organisation/elections/2015-election-ballots.blt
                    winner Paddy Duncan(2) (0.769)
                      winner Tom Hodder(4) (0.991)
                     winner Andy Tidman(9) (0.977)
                winner Charles Yarnold(11) (0.659)
~~~~





