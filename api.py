from flask import Flask,request,make_response,Response
from dict2xml import dict2xml
from flask_restful import Resource, Api
from flask_paginate import get_page_args
import pandas as pd
import os

#Auxiliary function to read the vcf file
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l.rstrip('\n').split('\t') for l in f if not l.startswith('##')]
    
    df=pd.DataFrame(lines[1:],columns=[x if '#' not in x else 'CHROM' for x in lines[0]])
    if path.endswith('.vcf'):
        df.to_csv('./NA12877_API_10.csv')
    return df


# Instantiate Result class
# The class will take implement the /result endpoint and its get functionality
class Result(Resource):

    # implement get request
    def get(self):
        
        #read paging parameters from url
        page,per_page,_ = get_page_args(page_parameter='page',per_page_parameter='per_page')

        if page==0:
            return {'error':'page parameter, if specified cannot be lower than 1'},400

        id = request.args.get('id')

        #generate a unique etag for the request
        etag='%s_%s_%s'%(id,str(page),str(per_page))
        #check if request has If None Match header and if its value is equal to the etag
        if request.if_none_match and etag in request.if_none_match:
            my_resp=make_response({'message':'etag_recognized, computation skipped'})
            my_resp.status_code=304
            return my_resp

        #read data
        is_csv = True if len([x for x in os.listdir() if x.endswith('.csv')]) >0 else False
        if is_csv:
            data = pd.read_csv('./NA12877_API_10.csv',index_col=0)
        else:
            data = read_vcf('./NA12877_API_10.vcf')

        #instantiate repsonse 
        response = data[data['ID']==id] #select rows with the specificed id
        pagination_data = response.iloc[(page-1)*per_page:page*per_page] #limit results to one "page"
        total = response.shape[0]
        pages_overall = int(total/per_page)+1
        
        accept_headers=[] if 'Accept' not in request.headers else request.headers['Accept'].split(',') #read accept headers
        accepted_headers=['application/json','application/xml','*/*']
        #define response body
        data = {'meta':{
                    'entries_per_page':per_page,
                    'displayed_page':page,
                    'has_prev_page':True if page != 1 else False,
                    'has_next_page':True if page < pages_overall else False,
                    'pages':pages_overall,
                    'entries':total},'data':pagination_data.to_dict(orient='index')}
        
        #if no accept header is specified or if the specified one is not among the allowed ones return error 
        if len(accept_headers) > 1 or len(accept_headers)==0 or accept_headers[0] not in accepted_headers:
            return {'error': 'Accept header not acceptable','meassage':'One header has to be passed and it has to be one of the following: "application/json","application/xml" and "*/*"'},406
        elif accept_headers[0]=='application/json' or  accept_headers[0]=='*/*': #handle json response type and default fallback
            if response.shape[0]>0:
                my_resp = make_response(data)
                my_resp.mimetype = 'application/json' 
                my_resp.status_code=200
                my_resp.headers['etag']=etag
                return my_resp
        elif accept_headers[0]=='application/xml': #handle xml response type
            if response.shape[0]>0:
                my_resp = make_response(dict2xml(data))
                my_resp.mimetype = 'application/xml' 
                my_resp.status_code=200
                my_resp.etag=etag
                my_resp.headers['etag']=etag
                return my_resp
        return {'error':'data entry not found'},404 #if no entry is found return error
    
    # Implement POST function
    def post(self):
        #make sure that content type is json
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            #read json payload
            json = request.json
            #add post data to "database"
            new_data = pd.DataFrame({
                'CHROM':json['CHROM'],
                'POS':json['POS'],
                'ALT':json['ALT'],
                'REF':json['REF'],
                'ID':json['ID']
            },index=[0])
            # read our CSV
            is_csv = True if len([x for x in os.listdir() if x.endswith('.csv')]) >0 else False
            if is_csv:
                data = data = pd.read_csv('./NA12877_API_10.csv',index_col=0)
            else:
                data = read_vcf('./NA12877_API_10.vcf')
            #add missing columns to new data and reorder them
            for col in list(data.columns):
                if col not in json:
                    new_data[col]='-'
            new_data=new_data[list(data.columns)]
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('./NA12877_API_10.csv', index=False)
            return {'data': new_data.to_dict()}, 201  # return data with 201 CREATED status code

        else:
            return 'Content-Type not supported!'

#instantiate Flask API
app=Flask(__name__)
api=Api(app)

# Add endpoint to API
api.add_resource(Result,'/result')

if __name__ == '__main__':
    app.run() #run app



