#
# $Id$
#

# coding:utf-8

from sphinxapi import *
import sys, time, os


def sphinx_search(query):
    q=query
    mode=SPH_MATCH_EXTENDED2
    host='localhost'
    port=9312
    index='dist_ubuntu'
    #index='*'
    filtercol='group_id'
    filtervas=[]
    sortby=''
    groupby=''
    groupsort='@group desc'
    limit=0
    c1=SphinxClient()
    c1.SetServer(host,port)
    c1.SetWeights([1, 1])
    c1.SetMatchMode(mode)
    res=c1.Query(q,index)
    result=[]
    if res.has_key('matches'):
        n=1
        for match in res['matches']:
            attrsdump=''
            for attr in res['attrs']:
                attrname=attr[0]
                attrtype=attr[1]
                #print attrname
                value=match['attrs'][attrname]
                if attrtype==SPH_ATTR_TIMESTAMP:
                    value=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(value))
                attrsdump='%s, %s=%s' %(attrsdump, attrname, value)
            #print "hello"
            #print match
            #print res['time']
            temp='%d, doc_id=%s, weight=%d%s, using %s sec' %(n, match['id'],match['weight'], attrsdump,res['time'])
            n+=1
            #print n
            result.append(temp)
    return result

if __name__=='__main__':
    search('google')
