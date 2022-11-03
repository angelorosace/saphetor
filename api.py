from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import io

#Auxiliary function to read the vcf file
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l.rstrip('\n').split('\t') for l in f if not l.startswith('##')]
    return pd.DataFrame(lines[1:],columns=[x if '#' not in x else 'CHROM' for x in lines[0]])

# Instantiate Result class
class Result(Resource):

    # implement get request
    def get(self):
        data = read_vcf('./data')
        return {'data':list(data.columns)[0]}



app=Flask(__name__)
api=Api(app)

# Add endpoint to API
api.add_resource(Result,'/result')

if __name__ == '__main__':
    app.run() #run app



