import mimetypes
from flask import Flask,request,make_response,Response
from dict2xml import dict2xml
from flask_restful import Resource, Api
from flask_paginate import get_page_args
import pandas as pd
import io

#Auxiliary function to read the vcf file
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l.rstrip('\n').split('\t') for l in f if not l.startswith('##')]
    return pd.DataFrame(lines[1:],columns=[x if '#' not in x else 'CHROM' for x in lines[0]])


etag=''

# Instantiate Result class
class Result(Resource):
    # implement get request
    def get(self):
        #read data file

        page,per_page,_ = get_page_args(page_parameter='page',per_page_parameter='per_page')

        data = read_vcf('./data')

        if page==0:
            return {'error':'page parameter, if specified cannot be lower than 1'},400
        
        

        id = request.args.get('id')

        etag='%s_%s_%s'%(id,str(page),str(per_page))
        if request.if_none_match and etag in request.if_none_match:
            my_resp=make_response({'message':'etag_recognized, computation skipped'})
            my_resp.status_code=304
            return my_resp

        #instantiate repsonse 
        response = data[data['ID']==id]
        pagination_data = response.iloc[(page-1)*per_page:page*per_page]
        total = response.shape[0]
        pages_overall = int(total/per_page)+1

        
        
        accept_headers=[] if 'Accept' not in request.headers else request.headers['Accept'].split(',')
        accepted_headers=['application/json','application/xml','*/*']
        data = {'meta':{
                    'entries_per_page':per_page,
                    'displayed_page':page,
                    'has_prev_page':True if page != 1 else False,
                    'has_next_page':True if page < pages_overall else False,
                    'pages':pages_overall,
                    'entries':total},'data':pagination_data.to_dict(orient='index')}
        
        if len(accept_headers) > 1 or len(accept_headers)==0 or accept_headers[0] not in accepted_headers:
            return {'error': 'Accept header not acceptable','meassage':'One header has to be passed and it has to be one of the following: "application/json","application/xml" and "*/*"'},406
        elif accept_headers[0]=='application/json' or  accept_headers[0]=='*/*':
            if response.shape[0]>0:
                my_resp = make_response(data)
                my_resp.mimetype = 'application/json' 
                my_resp.status_code=200
                my_resp.headers['etag']=etag
                return my_resp
        elif accept_headers[0]=='application/xml':
            if response.shape[0]>0:
                my_resp = make_response(dict2xml(data))
                my_resp.mimetype = 'application/xml' 
                my_resp.status_code=200
                my_resp.etag=etag
                my_resp.headers['etag']=etag
                return my_resp
        return {'error':'data entry not found'},404

app=Flask(__name__)
api=Api(app)

# Add endpoint to API
api.add_resource(Result,'/result')

if __name__ == '__main__':
    app.run() #run app



