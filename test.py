from api import app
import unittest

POST_BODY={"CHROM": "chrX", "POS": 102222200, "ALT": "A", "REF": "G","ID": "rs123"}
POST_BODY_WRONG={"CHROM": "wrongCHROM", "POS": 102222200, "ALT": "A", "REF": "G","ID": "rs123"}
PUT_BODY={"CHROM": "chr21", "POS": 1, "ALT": "G", "REF": "A","ID": "rs123"}

class FlaskTest(unittest.TestCase):

    ##TEST GET
    
    #check succesfull get response
    def test_1_get_200(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=rs123',headers={'Accept':'application/json'})
        status_code=response.status_code
        self.assertEqual(status_code,200)
    
    #check failed get request due to missing the accept header
    def test_2_get_406_no_accept_header(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=rs123')
        status_code=response.status_code
        self.assertEqual(status_code,406)
    
    #check failed get request due to unsupported accept header
    def test_3_get_406_wrong_accept_header(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=rs123',headers={'Accept':'application/madeupheader'})
        status_code=response.status_code
        self.assertEqual(status_code,406)

    #check failed get request due to multiple accept headers
    def test_4_get_406_multiple_accept_header(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=rs123',headers={'Accept':'application/json,application/xml'})
        status_code=response.status_code
        self.assertEqual(status_code,406)
    
    #check failed get request due to unsupported page parameter value accept headers
    def test_5_get_400_unsupported_page_path_variable(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=rs123&page=0',headers={'Accept':'application/json'})
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check get request response when etag is provided
    def test_6_get_304_wrong_etag(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=rs123',headers={'Accept':'application/json','If-None-Match':'rs123_1_10'})
        status_code=response.status_code
        self.assertEqual(status_code,304)
    
    #check failed get request due to unsupported id
    def test_7_get_404_data_entry_not_found(self):
        tester=app.test_client(self)
        response=tester.get('/result?id=dummyID',headers={'Accept':'application/json'})
        status_code=response.status_code
        self.assertEqual(status_code,404)
    
    ##TEST POST

    #check failed post request due to unauthorized user (no password provided)
    def test_8_post_403_unauthorized_user_no_password(self):
        tester=app.test_client(self)
        response=tester.post('/result',headers={'Accept':'application/json'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,403)
    
    #check failed post request due to unauthorized user (wrong password)
    def test_9_post_403_unauthorized_user_wrong_password(self):
        tester=app.test_client(self)
        response=tester.post('/result',headers={'Content-Type':'application/json','Authorization':'wrong_password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,403)
    
    #check failed post request due to unsupported content type
    def test_10_post_400_wrong_content_type(self):
        tester=app.test_client(self)
        response=tester.post('/result',headers={'Content-Type':'application/wrong_content_type','Authorization':'password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check failed post request due to wrong body
    def test_11_post_400_wrong_body(self):
        tester=app.test_client(self)
        response=tester.post('/result',headers={'Content-Type':'application/json','Authorization':'password'},json=POST_BODY_WRONG)
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check successful post request
    def test_12_post_201_created_data(self):
        tester=app.test_client(self)
        response=tester.post('/result',headers={'Content-Type':'application/json','Authorization':'password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,201)
    
    ##TEST PUT
    #check failed put request due to unauthorized user (no password provided)
    def test_13_put_403_unauthorized_user_no_password(self):
        tester=app.test_client(self)
        response=tester.put('/result',headers={'Accept':'application/json'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,403)
    
    #check failed put request due to unauthorized user (wrong password)
    def test_14_put_403_unauthorized_user_wrong_password(self):
        tester=app.test_client(self)
        response=tester.put('/result',headers={'Content-Type':'application/json','Authorization':'wrong_password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,403)
    
    #check failed put request due to unsupported id
    def test_15_put_400_unsupported_id(self):
        tester=app.test_client(self)
        response=tester.put('/result',headers={'Content-Type':'application/json','Authorization':'password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check failed put request due to unsupported content type
    def test_16_put_400_wrong_content_type(self):
        tester=app.test_client(self)
        response=tester.put('/result?id=rs123',headers={'Content-Type':'application/wrong_content_type','Authorization':'password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check failed put request due to wrong body
    def test_17_put_400_wrong_body(self):
        tester=app.test_client(self)
        response=tester.put('/result?id=rs123',headers={'Content-Type':'application/json','Authorization':'password'},json=POST_BODY_WRONG)
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check failed put request due to unsupported id
    def test_18_put_404_wrong_body(self):
        tester=app.test_client(self)
        response=tester.put('/result?id=fake_id_123',headers={'Content-Type':'application/json','Authorization':'password'},json=POST_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,404)
    
    #check successful put request
    def test_19_put_200(self):
        tester=app.test_client(self)
        response=tester.put('/result?id=rs123',headers={'Content-Type':'application/json','Authorization':'password'},json=PUT_BODY)
        status_code=response.status_code
        self.assertEqual(status_code,200)
    
    #TEST DELETE
    #check failed delete request due to unauthorized user (no password provided)
    def test_20_delete_403_unauthorized_user_no_password(self):
        tester=app.test_client(self)
        response=tester.delete('/result',headers={'Accept':'application/json'})
        status_code=response.status_code
        self.assertEqual(status_code,403)
    
    #check failed delete request due to unauthorized user (wrong password)
    def test_21_delete_403_unauthorized_user_wrong_password(self):
        tester=app.test_client(self)
        response=tester.delete('/result',headers={'Content-Type':'application/json','Authorization':'wrong_password'})
        status_code=response.status_code
        self.assertEqual(status_code,403)
    
    #check failed delete request due to unsupported id
    def test_22_delete_400_unsupported_id(self):
        tester=app.test_client(self)
        response=tester.delete('/result',headers={'Content-Type':'application/json','Authorization':'password'})
        status_code=response.status_code
        self.assertEqual(status_code,400)
    
    #check failed delete request due to not present id
    def test_23_delete_404_not_present_id(self):
        tester=app.test_client(self)
        response=tester.delete('/result?id=fake_id',headers={'Content-Type':'application/json','Authorization':'password'})
        status_code=response.status_code
        self.assertEqual(status_code,404)
    
    #check succesful delete
    def test_24_delete_204(self):
        tester=app.test_client(self)
        response=tester.delete('/result?id=rs123',headers={'Content-Type':'application/json','Authorization':'password'})
        status_code=response.status_code
        self.assertEqual(status_code,204)

if __name__ == '__main__':
    unittest.main()