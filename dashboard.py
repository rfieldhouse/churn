import logging
import pickle
import random
import os
import logging
import collections

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import mysql.connector

import cherrypy
from spyre import server



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

# Features

dfResults = pickle.load(open("results.p","rb"))
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
                    "label":"Type in a tenant-client relationship id",
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

    tabs = ['Relationship_Plot','Relationship_Table','About','Slides'] #'',

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
        tenant_client_in=''
        tenant_client_in = params['tenant_client_in']
        print 'tenant_client_in'
        print tenant_client_in

        # if (tenant_client_in ==''):
        #     print 'RANDOM'
        #     relationships = set(dfResults['tenant_client'])
        #     tenant_client_in = str(random.sample(relationships, 1)[0])
        #     print tenant_client_in
        #     len(set(dfResults['tenant_client']))
        # else:
        #     print tenant_client_in

        tenant_client_res = dfResults[dfResults['tenant_client'] == tenant_client_in]
        print tenant_client_res

        health_score = str(tenant_client_res.churn_no).split()[1]
        print
        print 'health_score'
        print health_score
        print 'tenant_client_res'
        print tenant_client_res['churn_pred']
        if int(tenant_client_res['churn_pred']) == 0:
            status = 'healthy'
        else:
            status = 'unhealthy'

        tenant_id = tenant_client_in.split('_')[0]
        client_id = tenant_client_in.split('_')[1]

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
        ax.set_xlabel('time')
        ax.set_ylabel('interaction count')
        title=str(tenant_client_in) + '  ' + status + ' (Score: ' + str(health_score) + ')'
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

        tenant_client_in=''
        tenant_client_in = params['tenant_client_in']
        print 'tenant_client_in'
        print tenant_client_in
        tenant_client_res = pd.DataFrame()

        # if (tenant_client_in ==''):
        #     print 'RANDOM'
        #     dfResults['tenant_client'] = dfResults['tenant_id'] + '_' + dfResults['client_id']
        #     relationships = set(dfResults['tenant_client'])
        #     tenant_client_in = str(random.sample(relationships, 1)[0])
        #     print tenant_client_in
        #     len(set(dfResults['tenant_client']))
        # else:
        #     print tenant_client_in

        tenant_client_res = dfResults[dfResults['tenant_client'] == tenant_client_in]
        tenant_client_res = pd.DataFrame.transpose(tenant_client_res).reset_index()
        print tenant_client_res

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
