import logging
import pickle
import random
import os
import logging
import collections
import cherrypy
from spyre import server
import glob
import os
import logging
import collections
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import mysql.connector
import pandas as pd
import numpy as np
import seaborn as sns
import numpy as np
import pandas as pd
import qgrid
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import prettyplotlib as ppl
import statsmodels.api as sm
import seaborn as sns
from bokeh import *
from bokeh import resources as r
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.plotting import *
from bokeh.models import *



# Create database engine
dbname = os.environ["DBNAME"]
uname = os.environ["UNAME"]
passwd = os.environ["PASSWD"]
portnum = os.environ["PORTNUM"]
engine = create_engine('mysql+mysqlconnector://mydb_user:'+uname+'@localhost:'+portnum+'/'+dbname, echo=False)
print engine.url

# Connect to database
conn = mysql.connector.connect(
         user=uname,
         password=passwd,
         host='localhost',
         database=dbname)

def FormatTable(df):

    df = df.round(2)

    df = df[[
    'tenant_client',
    'tenant_id',
    'client_id',
    'first_date',
    'last_date',
    'num_days',
    'num_interactions',
    'frequency',
    'num_emails',
    'email_frequency',
    'num_calls',
    'call_frequency',
    'num_meetings',
    'meeting_frequency',
    'mean_gap',
    'max_gap',
    'min_gap',
    'start_date',
    'end_date',
    'active_count',
    'subscription_length',
    'num_periods',
    'mean_duration',
    # 'total_duration',
    # 'min_duration',
    # 'max_duration',
    # 'comp',
    'recency',
    'churn_no',
    'churn_yes',
    'churn_pred',
    'churned',
    ]]

    colDict = {
    'client_id':'Client ID',
    'num_interactions':'Number of Interactions',
    'num_emails':' Number of Emails',
    'num_calls':'Number of Calls',
    'num_meetings':'Number of Meetings',
    'mean_gap':'Average Gap Between Interactions (days)',
    'max_gap':'Maximum Gap Between Interactions (days)',
    'min_gap':'Minimum Gap Between Interactions (days)',
    'first_date':'Date of First Interaction',
    'last_date':'Date of Last Interaction',
    'num_days':'Length of Relationship (days)',
    'frequency':'Frequency of Interactions',
    'email_frequency':'Frequency of Emails',
    'call_frequency':'Frequency of Calls',
    'meeting_frequency':'Frequency of Meetings',
    'tenant_id':'Tenant ID',
    'num_periods':'Number of Subscription Periods',
    'mean_duration':'Average Subscription Length (days)',
    'total_duration':'Length of Subscriptions (all)',
    'min_duration':'Minimum Length of subscription (days)',
    'max_duration':'Maximum Length of subscription (days)',
    'active_count':'Number of Active Subscriptions (days)',
    'start_date':'Start Date of First Subscription',
    'end_date':'End Date of Last Subscription',
    'subscription_length':'Length of Subscriptions (days)',
    'comp':'comp',
    'recency':'Recency',
    'churn_no':'Probability of Not Churning',
    'churn_yes':'Probability of Churning',
    'churn_pred':'Churn Prediction (0=no, 1=yes)',
    'churned':'Current Churn Status (Ground Truth) (0=no, 1=yes)',
    'tenant_client':'Tenant-Client ID',
    }
    df = df.rename(columns=colDict)
    return df

# Features

dfResults = pickle.load(open("results_int.p","rb"))
print dfResults
#dfResults['tenant_client'] = dfResults['tenant_id'] + '_' + dfResults['client_id']
dfResults['tenant_client'] = dfResults['tenant_id'].astype(str) + '_' + dfResults['client_id'].astype(str)

relationships = set(dfResults['tenant_client'])
starter = str(random.sample(relationships, 1)[0])
print starter

# global tenant_client_in

class SimpleApp(server.App):
    title = 'ClientKeeper: Predicting Engagement and Churn in B2B Relationships'
    inputs = [
                # {   
                #     "type":'radiobuttons',
                #     "label": 'Choose random relationship', 
                #     "options" : [
                #         {"label": "Yes", "value":"Yes", "checked":True}, 
                #         {"label":"No", "value":"No"}
                #     ],
                #     "key": 'random_in', 
                #     "action_id" : "get_random",
                # },
                { "type":"text",
                    "label":"Type in an integer or tenant-client id",
                    'variable_name':'tenant_client_in',
                    "value":starter, 
                    "key":"tenant_client",
                    "action_id":"define_tenant_client"}
            ]

    controls = [
                # {   'control_type' : 'button',
                #     'label' : 'Get Random Relationship',
                #     'control_id' : 'get_random',
                #     'value':'Yes',
                #     'key':'random_in',
                #     'action_id':'get_random'},
                {   'control_type' : 'hidden',
                    'label' : 'tenant_client',
                    'control_id' : 'define_tenant_client'},
                {   'control_type' : 'hidden',
                    'label' : 'get_text',
                    'control_id' : 'get_text'},
                {   'control_type' : 'hidden',
                    'label' : 'get_slides',
                    'control_id' : 'get_slides'}
            ]

    tabs = ['About','Relationship_Plot','Relationship_Table','Slides'] #'',

    outputs = [
                # {'type':'html',
                # 'id':'simple_html_output'},
                # {'output_type' : 'image',
                #     'output_id' : 'tenant_client_out_random',
                #     'control_id' : 'get_random',
                #     'tab' : 'Relationship Plot',
                #     'on_page_load' : True },
                {'output_type' : 'table',
                    'output_id' : 'tenant_client_table',
                    'control_id' : 'define_tenant_client',
                    'tab' : 'Relationship_Table',
                    'on_page_load' : True },
                {'output_type' : 'image',
                    'output_id' : 'tenant_client_plot',
                    'control_id' : 'define_tenant_client',
                    'tab' : 'Relationship_Plot',
                    'on_page_load' : True },
                {   'output_type' : 'html',
                    'output_id' : 'get_text',
                    'control_id' : 'get_text',
                    'tab' : 'About',
                    'on_page_load' : True },
                {   'output_type' : 'html',
                    'output_id' : 'get_slides',
                    'control_id' : 'get_slides',
                    'tab' : 'Slides',
                    'on_page_load' : True }
            ]

#    def getHTML(self, params):
#
#        if (params['output_id'] == 'get_text'):
#            cwd = os.getcwd()
#            htmlFileName = os.path.join(cwd,'About.html')
#            print htmlFileName
#            html = open(htmlFileName,'r')
#            return html
#        if (params['output_id'] == 'get_slides'):
#            cwd = os.getcwd()
#            htmlFileName = os.path.join(cwd,'Slides.html')
#            print htmlFileName
#            html = open(htmlFileName,'r')
#            return html

        # words = params['words']
        # return 'Heres what you wrote in the textbox: <b>%s</b>' # % words

    def getImage(self,params):
        print 'IMAGE'

        fig = mpimg.imread('ContentUnavailable.jpg')
        tenant_client_in = params['tenant_client_in']
        print 'tenant_client_in'
        print tenant_client_in

        try:
            tenant_client_in = int(tenant_client_in)
            tenant_client_res = dfResults.loc[tenant_client_in]
            tenant_client_res = pd.DataFrame(tenant_client_res)
            tenant_client_res = pd.DataFrame.transpose(tenant_client_res).reset_index()
            print tenant_client_res
            tenant_id = str(tenant_client_res['tenant_id'].ix[0,:])
            client_id = str(tenant_client_res['client_id'].ix[0,:])
            print tenant_id
            print client_id
        except:
            tenant_client_res = dfResults[dfResults['tenant_client'] == tenant_client_in]
            print tenant_client_res
            tenant_id = tenant_client_in.split('_')[0]
            client_id = tenant_client_in.split('_')[1]
        
        health_score = str(tenant_client_res['churn_no']).split()[1]
        print
        print 'health_score'
        print health_score
        print 'tenant_client_res'
        print tenant_client_res['churn_pred']
        if int(tenant_client_res['churn_pred']) == 0:
            status = 'healthy'
        else:
            status = 'unhealthy'

        sql_query = """SELECT id, created_date_time FROM client_note WHERE client_id="""+str(client_id)+""";"""
        dfClientNote = dict()
        dfClientNote[client_id]=pd.read_sql_query(sql_query,conn)

#        status = 'unknown'

        sDateTime = pd.to_datetime(dfClientNote[client_id]['created_date_time'], '%d/%m/%y %H:%M')
        year=sDateTime.dt.year
        month=sDateTime.dt.month
        day=sDateTime.dt.day
        dfClientNote[client_id]=dfClientNote[client_id].assign(year=year)
        dfClientNote[client_id]=dfClientNote[client_id].assign(month=month)
        dfClientNote[client_id]=dfClientNote[client_id].assign(day=day)

        daily=dfClientNote[client_id].groupby(['year','month','day'])['id'].count()
        daily=daily.reset_index(level=0)
        daily=daily.reset_index(level=0)
        daily=daily.reset_index(level=0)
        daily.index = pd.to_datetime(daily.ix[:, ['year', 'month', 'day']])
        daily

        win = 7
        rollMean = daily.id.rolling(window=win, center=False).mean()

        sns.set_context('talk')

        # fig, ax = plt.subplots()
        # ax.scatter(x=daily.index, y=daily.id, label='Raw Data')
        # ax.plot(rollMean, color='red', label='Rolling Mean')
        # ax.set_xlabel('Year')
        # ax.set_ylabel('id')
        # plt.legend()
        # plt.title("Raw Data and the Rolling Mean")
        #sns.despine()
        #plt.save('plt.png')

        fig, ax = plt.subplots()
        ax.scatter(x=daily.index, y=daily.id, label='raw data')
        ax.plot(rollMean, color='red', label='rolling mean (7-day window')
        ax.xaxis.rotation=45
        ax.set_xlabel('time')
        ax.set_ylabel('interaction count')
        title=str(tenant_id) +'-' + (client_id) + '  ' + status + ' (Score: ' + str(health_score) + ')'
        plt.title(title)
        # ax.text(status)

        # plt.legend()
        # plt.title("Raw Data and the Rolling Mean")
        #sns.despine()
        # plt.figure(figsize=(20,10))
        # plt.close()
        fig.savefig('plt.png')
        fig = mpimg.imread('plt.png')
        return fig #fig.gca() #plt.gcf()



    def getData(self, params):
        print 'DATA'

        tenant_client_in = params['tenant_client_in']
        print 'tenant_client_in'
        print tenant_client_in

        # try:
        #     tenant_client_in = int(tenant_client_in)
        #     #tenant_client_res = dfResults[dfResults['tenant_client'] == tenant_client_in]
        #     tenant_client_res = dfResults.loc[tenant_client_in] #,:]
        #     tenant_client_res = pd.DataFrame(tenant_client_res)
        # except:
        #     tenant_client_res = dfResults[dfResults['tenant_client'] == tenant_client_in]        
        #     tenant_client_res = pd.DataFrame.transpose(tenant_client_res).reset_index()
        # print tenant_client_res

        try:
            tenant_client_in = int(tenant_client_in)
            tenant_client_res = dfResults.loc[tenant_client_in]
            tenant_client_res = pd.DataFrame(tenant_client_res)
            tenant_client_res = pd.DataFrame.transpose(tenant_client_res).reset_index()
            print tenant_client_res
            tenant_id = str(tenant_client_res['tenant_id'].ix[0,:])
            client_id = str(tenant_client_res['client_id'].ix[0,:])
            print tenant_id
            print client_id
        except:
            tenant_client_res = dfResults[dfResults['tenant_client'] == tenant_client_in]
            print tenant_client_res
            print ' '.join(tenant_client_res.columns)
            tenant_id = tenant_client_in.split('_')[0]
            client_id = tenant_client_in.split('_')[1]

        tenant_client_res = tenant_client_res.reset_index()
        tenant_client_res = FormatTable(tenant_client_res)
        tenant_client_res = pd.DataFrame.transpose(tenant_client_res).reset_index()
        tenant_client_res.columns = ['Feature','Value']
        tenant_client_res = tenant_client_res.round(2)
        return tenant_client_res

    def getHTML(self,params):
        print 'HTML'
        if (params['output_id'] == 'get_text'):
            cwd = os.getcwd()
            htmlFileName = os.path.join(cwd,'Blog.html')
            print htmlFileName
            html = open(htmlFileName,'r')
            return html
        if (params['output_id'] == 'get_slides'):
            cwd = os.getcwd()
            htmlFileName = os.path.join(cwd,'Slides.html')
            print htmlFileName
            html = open(htmlFileName,'r')
            return html

socketPort = int(os.environ["SOCKETPORT"])
staticDir = os.environ["STATICDIR"]
cherrypy.config.update({'server.socket_host':'0.0.0.0',
                        'server.socket_port':socketPort,
                        '/images': {
                        'tools.staticdir.on': True,
                        'tools.staticdir.dir':staticDir}
                       })

app = SimpleApp()
app.launch(port=socketPort)
