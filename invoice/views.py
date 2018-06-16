from django.shortcuts import render, redirect, reverse
import requests
import dateutil.parser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from clockin.models import IntervalWork, Bill
from invoice.models import Project
from invoice.tables import BillingTable
from django_tables2 import RequestConfig
from django.utils import timezone
from pytz import timezone as pytzTZ
from django.http import HttpResponseRedirect
from rest_framework.generics import CreateAPIView, UpdateAPIView
import logging
from invoice.serializers import BillSerializer
from invoice.forms import PayForm


log = logging.getLogger("workTracker")

class InvoiceView(LoginRequiredMixin, ListView):
    model = IntervalWork
    template_name = 'invoice/bill.html'
    myProject = None
    myHours = None
    my_bill = None
    
    def get_queryset(self):
        try:
            self.myProject = Project.objects.get(name=self.request.GET["project"])
            self.myHours = IntervalWork.objects.filter(project__name=self.request.GET["project"], paid=False).order_by('started')
            self.my_bill = Bill.objects.filter(project__name=self.request.GET["project"]).latest('created')
            return self.myHours
        except:
            return IntervalWork.objects.none()

    def get_context_data(self, **kwargs): 
        context = super(InvoiceView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['pay_form'] = PayForm()
        # Update or create current bill
        if self.myProject:
            context['myProject'] = self.myProject.name
            if not self.my_bill:
                self.my_bill = Bill.objects.create(customer=self.request.user,project=self.myProject)
        context['bill_id'] = self.my_bill.id
        context['tax'] = self.my_bill.tax;
        context['pay_rate'] = self.my_bill.pay_rate;
        if self.myHours:
            for interval in self.myHours:
                interval.bill = self.my_bill
                interval.save()
            table = BillingTable(self.myHours) # gotta love list comprehensions
            context['totalHours'] = format(sum([float(interval.timeApart()) for interval in self.myHours]), '.2f')
            RequestConfig(self.request, paginate=False).configure(table)
            context['table'] = table

        return context
      
    # COULD FILTER BY ADMIN GROUP IF I CREATE ONE, OR BY OBJECT OWNERSHIP, REDIRECT BACK IF CRITERIA NOT MET
    '''
    def get(self, request, *args, **kwargs):
        try: 
            project = self.request.GET["project"]
            return super(InvoiceView, self).get(request, *args, **kwargs)
        except:
            return HttpResponseRedirect(reverse('menu') + "?project=none")'''
        

    def scrapeRepo():

        baseUrlv2 = "https://bitbucket.org/api/2.0"
        baseUrlv1 = "https://bitbucket.org/api/1.0"

        username = ""
        password = ""
        year = 2018

        totalCommits = 0
        totalAdd = 0
        totalRemove = 0
        overallAdd = 0
        overallRemove = 0
        commitCount = 0
        commits = []

        print("")
        print("Stats for {year}".format(year=year))
        print("")

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

	        print("Total commits in {user}/{repo}: {count}".format(user=username, repo=repoSlug, count=commitCount))	
	        print("\tLines added: {add}".format(add=totalAdd))
	        print("\tLines removed: {remove}\n".format(remove=totalRemove))
	        totalCommits += commitCount	
	        overallAdd += totalAdd
	        overallRemove += totalRemove
	        #reset counters
	        commitCount = 0
	        totalAdd = 0
	        totalRemove = 0
	        commits = []

        print("")
        print("Total commits: {count}".format(count=totalCommits))
        print("Total lines added: {count}".format(count=overallAdd))
        print("Total lines removed: {count}".format(count=overallRemove))

class BillCreate(CreateAPIView):
    
    serializer_class = BillSerializer
    myHours = None

    def get_queryset(self):
        self.myHours = IntervalWork.objects.filter(project__name=self.request.POST["project"], paid=False).order_by('started')
        return Bill.objects.all()

    # OVERRIDE VALIDATE AND IF VALID SAVE BILL ID TO WORK INTERVAL


class BillUpdate(UpdateAPIView):
    
    serializer_class = BillSerializer

    def get_queryset(self):
        return Bill.objects.all()

