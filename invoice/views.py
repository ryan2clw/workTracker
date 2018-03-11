from django.shortcuts import render
import requests
import dateutil.parser

# helper script to populate git details
# pass scrapeRepo data to the view

def scrapeRepo():

    baseUrlv2 = "https://bitbucket.org/api/2.0"
    baseUrlv1 = "https://bitbucket.org/api/1.0"

    username = ""
    password = ""
    year = 2013

    totalCommits = 0
    totalAdd = 0
    totalRemove = 0
    overallAdd = 0
    overallRemove = 0
    commitCount = 0
    commits = []

    print ""
    print "Stats for {year}".format(year=year)
    print ""

    r = requests.get("{base}/user/repositories/".format(base=baseUrlv1),
	    auth=(username, password))

    repos = r.json()

    for repo in repos:
	    repoSlug = repo['slug']
	    r = requests.get("{base}/repositories/{username}/{repo}/commits".format(base=baseUrlv2, username=username, repo=repoSlug),
	    auth=(username, password))

	    c = r.json()
	    commits.extend(c['values'])

	    while 'next' in c:
		    r = requests.get("{next}".format(next=c['next']), 
			    auth=(username, password))
		    c = r.json()
		    commits.extend(c['values'])

	    for commit in commits:
		    commitDate = dateutil.parser.parse(commit['date'])
		    if commitDate.year == year:
			    commitCount += 1

			    r = requests.get("{base}/repositories/{username}/{repo}/changesets/{hash}/diffstat/".format(base=baseUrlv1, 
			    username=username, repo=repoSlug, hash=commit['hash']),auth=(username, password))
			
			    try:
				    stats = r.json()
			    except ValueError:
			        # decoding failed
			        continue

			    for stat in stats:
				    try:
					    totalAdd += stat['diffstat']['added']
					    totalRemove += stat['diffstat']['removed']
				    except TypeError:
					    continue

	    print "Total commits in {user}/{repo}: {count}".format(user=username, repo=repoSlug, count=commitCount)		
	    print "\tLines added: {add}".format(add=totalAdd)
	    print "\tLines removed: {remove}\n".format(remove=totalRemove)
	    totalCommits += commitCount	
	    overallAdd += totalAdd
	    overallRemove += totalRemove
	    #reset counters
	    commitCount = 0
	    totalAdd = 0
	    totalRemove = 0
	    commits = []

    print ""
    print "Total commits: {count}".format(count=totalCommits)
    print "Total lines added: {count}".format(count=overallAdd)
    print "Total lines removed: {count}".format(count=overallRemove)
