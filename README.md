# COMMENTS

The provided API was developed with Flask.
It supports the use of a vcf file as database although as soon as the first request is received the API will copy it into a csv format.
This is done to avoid handling the extra fields in the vcf file that do not allow its correct handling with pandas.
Therefore, to check the changes to the database please refer to the .csv file

The database name and the secret are hardcoded into the code since at this stage it is the most convenient way of handling such variables. Of course, one can make it more dynamic but is out of the scope of the task.

Tests for the API calls have been implemented and the API itself was tested in development with POSTMAN

# SETUP

A requirement.txt file is provided for you to install all dependencies.

To run the API one simply needs to run the api.py file with the following command:

python api.py

# USAGE

I decided to create the /result endpoint.
This endpoint will handle all GET,POST,PUT and DELETE requests.

(Please make sure to add your ruquest headers in the same way you see them written in this file)

## GET Request

In order to perform a basic get request the user must use the following URL:

local_host:port/result$id=some_id

id is a required field.

The API response will be paginated. To navigate through the results one can add the page and per_page parameters.
They are set to 1 and 10 by default respectively.
So the GET request can also look like this:

local_host:port/result$id=some_id&page=some_page&per_page=value

This call will return per_page number of fields from page.

If page or per_page are set to undesired values the API will default to their default values: page=1 and per_page=10

Along with the request we must make sure to provide the correct headers:
(Required) Accept header -> MUST be ONE value between 'application/json','apllication/xml' or '*/*'
(Optional) If-None-Match -> if provided and etag is recognized the API will behave accordingly

## POST Request

The post request is performed by calling the basic URL: local_host:port/result

We must also provide a body like:

{"CHROM": "chrX", "POS": 102222200, "ALT": "A", "REF": "G","ID": "rs123"}

Along with the request we must make sure to provide the correct headers:
(Required) Content-Type header -> MUST be 'application/json'
(Required) Authorization -> MUST be "password"

The API will check the body for the validity of its fields and the presence of all the required fields/unsupported fields

## PUT Request
The put request is performed by calling the basic URL plus the id of the entries we want to change: 

local_host:port/result?id=some_id

We must also provide a body like:

{"CHROM": "chrX", "POS": 102222200, "ALT": "A", "REF": "G","ID": "rs123"}

Along with the request we must make sure to provide the correct headers:
(Required) Content-Type header -> MUST be 'application/json'
(Required) Authorization -> MUST be "password"

The API will check the body for the validity of its fields and the presence of all the required fields/unsupported fields.
The API will also check the validity of the provided id and the existence of it in the dataset

## DELETE Request
The delete request is performed by calling the basic URL plus the id of the entries we want to change: 

local_host:port/result?id=some_id

Along with the request we must make sure to provide the correct headers:
(Required) Authorization -> MUST be "password"

The API will check the body for the validity of its fields and the presence of all the required fields/unsupported fields.
The API will also check the validity of the provided id and the existence of it in the dataset


