# plant-rank

An online ranking site for NTU CSIE Sprout 2017.

For a live demo, see: http://plantrank.pcchou.me

## Prerequisites

**CAUTION: WE THROW EVERYTHING INTO MONGODB!**

* Install MongoDB
* `pip install -r requirements.txt`
* `crontab -l | { cat; echo "*/3 * * * * python3 $PWD/sprout.py > /dev/null 2>&1";  } | crontab -`
