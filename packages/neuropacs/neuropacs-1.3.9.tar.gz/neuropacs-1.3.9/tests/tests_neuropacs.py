import unittest
import re
import json
from neuropacs.sdk import Neuropacs
from datetime import datetime, timezone


# RUN TESTS: python -m unittest tests.tests_neuropacs

'''
Test Scenarios

- invalid server url
- get public key
    - success X
- connect 
    - success X
    - invalid api key X
- new job 
    - success X
    - invalid connection id X
- upload 
    - File object success X
    - Uint8Array success X
- upload dataset 
    - dataset path success X
- run job
    - success X
    - invalid product X
    - invalid order id X
    - invalid connection id X
- check status
    - success X
    - invalid order id X
    - invalid connection id X
- get results
    - success X
        - TXT X
        - JSON X
        - XML X
    - invalid result format X
    - invalid order id X
    - invalid connection id X
'''

def logTest(description, input_data, expected_output, actual_output):
    log_message = """
Test Description: {description}

    Input:
    {input_data}

    Expected Output:
    {expected_output}

    Actual Output:
    {actual_output}

----------------------------------------------------------------------
    """.format(
        description=description,
        input_data=str(input_data),
        expected_output=str(expected_output),
        actual_output=str(actual_output)
    )
    print(log_message)

class UnitTests(unittest.TestCase):

    def setUp(self):
        server_url = "http://ec2-3-142-212-32.us-east-2.compute.amazonaws.com:5000"
        api_key = "m0ig54amrl87awtwlizcuji2bxacjm"
        self.npcs = Neuropacs(server_url, api_key)   

    # Test 1: get_public_key() - Success
    def test_get_public_key(self):

        public_key = self.npcs.get_public_key() #Get public key

        ### TEST PUBLIC KEY ###
        self.assertIsInstance(public_key, str, "Public key should be a string")
        public_key_regex = re.compile(r'-----BEGIN PUBLIC KEY-----\r?\n([A-Za-z0-9+/=\r\n]+)\r?\n-----END PUBLIC KEY-----')
        self.assertTrue(public_key_regex.match(public_key), "Public key should be a valid base64 encoded key")
        ### TEST PUBLIC KEY ###
        logTest("Successfully retrieve public key.", None, "Valid PEM formatted base64 encoded public key", public_key)

    # Test 2: connect() - SUCCESS
    def test_connect_success(self):
    
        connection = self.npcs.connect() # Get connection

        connection_id = connection['connection_id']
        aes_key = connection['aes_key']

        ### TEST CONNECTION ID ###
        self.assertIsInstance(connection_id, str, "Connection ID should be a string")
        self.assertEqual(len(connection_id), 32, "Connection ID should be length 32")
        self.assertTrue(connection_id.isalnum(), "Connection ID should contain only alphanumeric characters")
        self.assertIsInstance(aes_key, str, "Key should be a string")
        self.assertEqual(len(aes_key), 24, "Key should be length 24")
        aes_key_regex = re.compile(r'^[A-Za-z0-9+/]{22}==$')
        self.assertTrue(aes_key_regex.match(aes_key), "Key should be a valid base64 encoded key")
        ### TEST CONNECTION ID ###
        logTest("Successfully create a connection.",{"aes_key": self.npcs.aes_key,"api_key": self.npcs.api_key},"Connection object containing AES key, connection ID, and timestamp", connection)

    # Test 3: connect() - INVALID API KEY
    def test_connect_invalid_api_key_fail(self):
        
        invalid_api_key = "thisisnotarealapikey12345"
        self.npcs.api_key = invalid_api_key

        with self.assertRaises(Exception) as context:
            connection = self.npcs.connect() # Get connection
        ### TEST CONNECTION ID FAIL ###
        self.assertEqual(str(context.exception),"Connection failed!")  
        ### TEST CONNECTION ID FAIL ###
        logTest("Fail while creating a connection due to invalid API key.", {"aes_key": self.npcs.aes_key,"api_key": self.npcs.api_key}, "Connection failed!", str(context.exception))
        
    # Test 4: new_job() - SUCCESS
    def test_new_job_success(self):
        
        self.npcs.connect() # Get connection

        order_id = self.npcs.new_job() # Create new order
        ### TEST ORDER ID ###        
        self.assertIsInstance(order_id, str, "Order ID should be a string")
        self.assertEqual(len(order_id), 20, "Order ID should be length 32")
        self.assertTrue(order_id.isalnum(), "Order ID should contain only alphanumeric characters")
        ### TEST ORDER ID ###
        logTest("Successfully create a new job and return an order ID.", {'connection-id': self.npcs.connection_id}, "Order ID (string, length 20, alphanumeric)", order_id)

    # Test 5: new_job() - INVALID CONNECTION ID
    def test_new_job_invalid_connection_id_fail(self):
        
        invalid_connection_id = "thisisnotarealconnectionid12345"
        self.npcs.connection_id = invalid_connection_id

        with self.assertRaises(Exception) as context:
            order_id = self.npcs.new_job() # Create new order
        ### TEST ORDER ID FAIL ###  
        self.assertEqual(str(context.exception), "Job creation failed!") 
        ### TEST ORDER ID FAIL ###
        logTest("Fail while creating a new job due to invalid connection ID.", {'connection-id': self.npcs.connection_id}, "Job creation failed!", str(context.exception))


    # Test 6: upload() - SUCCESS (path)
    def test_upload_by_path_success(self):

        test_dicom_file_path = "./tests/test_dataset/testdcm"

        self.npcs.connect() # get connection

        self.npcs.new_job() # Create new order

        upload_status = self.npcs.upload(test_dicom_file_path) # Upload file

        ### TEST UPLOAD STATUS ###
        self.assertEqual(upload_status, 201)
        ### TEST UPLOAD STATUS ###
        logTest("Successfully upload a file via path string.", test_dicom_file_path, 201, upload_status)

    # Test 7: upload() - SUCCESS (bytes)
    def test_upload_by_bytes_success(self):

        with open('./tests/test_dataset/testdcm', 'rb') as file:
            test_dicom_bytes = file.read()

        self.npcs.connect() # Get connection

        self.npcs.new_job() # Create new order

        upload_status = self.npcs.upload(test_dicom_bytes) # Upload file

        ### TEST UPLOAD STATUS ###
        self.assertEqual(upload_status, 201)
        ### TEST UPLOAD STATUS ###
        logTest("Successfully upload a file via byte array (bytes).", test_dicom_bytes[:50], 201, upload_status)


    # Test 8: upload_dataset() - SUCCESS (path)
    def test_upload_dataset_by_path_success(self):

        test_dicom_file_path = "./tests/test_dataset/"

        self.npcs.connect() # Get connection

        self.npcs.new_job() # Create new order

        upload_status = self.npcs.upload_dataset(test_dicom_file_path) # Upload file

        ### TEST UPLOAD STATUS ###
        self.assertEqual(upload_status, 201)
        ### TEST UPLOAD STATUS ###
        logTest("Successfully upload a dataset via path string.", test_dicom_file_path, 201, upload_status)

    # Test 9: run_job() - SUCCESS
    def test_run_job_success(self):

        product_id = "PD/MSA/PSP-v1.0" # product ID

        self.npcs.connect() # Get connection id

        self.npcs.new_job() # Create new order

        job = self.npcs.run_job(product_id) # Run job

        ### TEST UPLOAD STATUS ###
        self.assertEqual(job, 202)
        ### TEST UPLOAD STATUS ###
        logTest("Successfully run a job and return a status 202.", {'orderID': self.npcs.order_id,'productID': product_id}, 202, job)
        

    # Test 10: run_job() - INVALID PRODUCT ID
    def test_run_job_invalid_product_id_fail(self):

        product_id = "notARealProduct" # product ID

        self.npcs.connect() # Get connection 

        self.npcs.new_job() # Create new order

        with self.assertRaises(Exception) as context:
            job = self.npcs.run_job(product_id) # Run job

        ### TEST JOB RUN FAIL ###  
        self.assertEqual(str(context.exception), "Job run failed.") 
        ### TEST JOB RUN FAIL ###
        logTest("Fail running a job due to invalid product ID.", {'connection-id':self.npcs.connection_id, 'orderID': self.npcs.order_id,'productID': product_id}, "Job run failed.", str(context.exception))


    # Test 11: run_job() - INVALID ORDER ID
    def test_run_job_invalid_order_id_fail(self):

        product_id = "PD/MSA/PSP-v1.0" # product ID

        self.npcs.connect() # Get connection

        with self.assertRaises(Exception) as context:
            job = self.npcs.run_job(product_id, "notARealOrderID") # Run job

        ### TEST JOB RUN FAIL ###  
        self.assertEqual(str(context.exception), "Job run failed.") 
        ### TEST JOB RUN FAIL ###
        logTest("Fail running a job due to invalid order ID.", {'connection-id':self.npcs.connection_id, 'orderID': "notARealOrderID" ,'productID': product_id}, "Job run failed.", str(context.exception))


    # Test 12: run_job() - INVALID CONNECTION ID
    def test_run_job_invalid_connection_id_fail(self):

        product_id = "PD/MSA/PSP-v1.0" # product ID

        self.npcs.connect() # Get connection id

        self.npcs.new_job() # Create new order

        self.npcs.connection_id = "notARealConnectionID"

        with self.assertRaises(Exception) as context:
            job = self.npcs.run_job(product_id) # Run job

        ### TEST JOB RUN FAIL ###  
        self.assertEqual(str(context.exception), "Job run failed.") 
        ### TEST JOB RUN FAIL ###
        logTest("Fail running a job due to invalid connection ID.", {'connection-id':self.npcs.connection_id, 'orderID': self.npcs.order_id,'productID': product_id}, "Job run failed.", str(context.exception))

    # Test 13: check_status() - SUCCESS
    def test_check_status_success(self):

        product_id = "PD/MSA/PSP-v1.0" # product ID

        self.npcs.connect() # Get connection

        self.npcs.new_job() # Create new order

        self.npcs.run_job(product_id) # Run job

        job_status = self.npcs.check_status("TEST") # Check status

        ### TEST CHECK STATUS ###
        self.assertIsInstance(job_status, str, "Job status should be a string")
        self.assertEqual(job_status, r'{"started":true,"finished":true,"failed":false,"progress":100,"info":"Finished"}')
        ### TEST CHECK STATUS ###
        logTest("Successfully check status of job.", {'connection-id': self.npcs.connection_id, 'orderID': "TEST"},r'{"started":true,"finished":true,"failed":false,"progress":100,"info":"Finished"}', job_status)


    # Test 14: check_status() - INVALID ORDER ID
    def test_check_status_invalid_order_id_fail(self):

        self.npcs.connect() # Get connection

        with self.assertRaises(Exception) as context:
            job_status = self.npcs.check_status("invalidOrderID") # check status

        ### TEST CHECK STATUS FAIL ###  
        self.assertEqual(str(context.exception), "Status check failed.") 
        ### TEST CHECK STATUS FAIL ###
        logTest("Fail checking job status due to invalid order ID.", {'connection-id': self.npcs.connection_id, 'orderID': "invalidOrderID"}, "Status check failed.", str(context.exception))

   # Test 15: check_status() - INVALID CONNECTION ID
    def test_check_status_invalid_connection_id_fail(self):

        self.npcs.connect() # Get connection

        self.npcs.connection_id = "noARealConnectionID"

        with self.assertRaises(Exception) as context:
            job_status = self.npcs.check_status("TEST") # check status

        ### TEST CHECK STATUS FAIL ###  
        self.assertEqual(str(context.exception), "Status check failed.") 
        ### TEST CHECK STATUS FAIL ###
        logTest("Fail checking job status due to invalid connection ID.", {'connection-id':"noARealConnectionID", 'orderID': "TEST"}, "Status check failed.", str(context.exception))

    # Test 16: get_results() - SUCCESS (TXT)
    def test_get_results_txt_success(self):

        self.npcs.connect() # Get connection

        job_results = self.npcs.get_results("TXT", "TEST") # Get results

        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        ### TEST JOB RESULTS ###
        self.assertIsInstance(job_results, str, "Job results should be a string")
        self.assertEqual(job_results, f"Order ID: TEST\nDate: {current_date}\nProduct: TEST\nPD probability vs. MSA/PSP: 62.6%\nMSA probability vs. PSP: 85.6%\nBiomarker levels: pSN=0.26, Putamen=0.19, SCP=0.48, MCP=0.07")
        ### TEST JOB RESULTS ###
        logTest("Successfully retrieve job results in TXT format.", {'connection-id': self.npcs.connection_id, 'orderID': "TEST", 'format': "TXT"}, f"Order ID: TEST\nDate: {current_date}\nProduct: TEST\nPD probability vs. MSA/PSP: 62.6%\nMSA probability vs. PSP: 85.6%\nBiomarker levels: pSN=0.26, Putamen=0.19, SCP=0.48, MCP=0.07", job_results)

    # Test 17: get_results() - SUCCESS (JSON)
    def test_get_results_json_success(self):

        self.npcs.connect() # Get connection

        job_results = self.npcs.get_results("JSON", "TEST") # Get results

        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        expected_result_pt1 = r'{"orderID":"TEST","date":"'
        expected_result_pt2 = r'","product":"TEST","result":{"PDprobability":"62.6","MSAprobability":"85.6","FWpSN":"0.26","FWPutamen":"0.19","FWSCP":"0.48","FWMCP":"0.07"}}'
        expected_result_full = expected_result_pt1 + current_date + expected_result_pt2

        ### TEST JOB RESULTS ###
        self.assertEqual(re.sub(r'\s', '', job_results), expected_result_full)
        try:
            json_object = json.loads(job_results)
            self.assertIsInstance(json_object, dict)
        except json.JSONDecodeError:
            self.fail("Job results must be valid JSON.")
        ### TEST JOB RESULTS ###
        logTest("Successfully retrieve job results in JSON format.", {'connection-id': self.npcs.connection_id, 'orderID': "TEST", 'format': "JSON"}, expected_result_full, re.sub(r'\s', '', job_results))


    # Test 18: get_results() - SUCCESS (XML)
    def test_get_results_xml_success(self):

        self.npcs.connect() # Get connection

        job_results = self.npcs.get_results("XML", "TEST") # Get results

        expected_result_pt1 = r'<?xmlversion="1.0"encoding="UTF-8"standalone="yes"?><neuropacsorderID="TEST"date="'
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        expected_result_pt2 = r'"product="TEST"><resultname="PDprobability"value="62.6"/><resultname="MSAprobability"value="85.6"/><dataname="FWpSN"value="0.26"/><dataname="FWPutamen"value="0.19"/><dataname="FWSCP"value="0.48"/><dataname="FWMCP"value="0.07"/></neuropacs>'
        expected_result_full = expected_result_pt1 + current_date + expected_result_pt2

        ### TEST JOB RESULTS ###
        self.assertEqual(re.sub(r'\s', '', job_results), expected_result_full)
        self.assertIsInstance(job_results, str, "Job results should be a string XML")
        ### TEST JOB RESULTS ###
        logTest("Successfully retrieve job results in XML format.", {'connection-id': self.npcs.connection_id, 'orderID': "TEST", 'format': "XML"}, expected_result_full, re.sub(r'\s', '', job_results))


   # Test 19: get_status() - INVALID RESULT FORMAT
    def test_check_status_invalid_result_format_fail(self):

        self.npcs.connect() # Get connection id

        with self.assertRaises(Exception) as context:
            self.npcs.get_results("noARealFormat", "TEST") # Get results

        ### TEST JOB RESULTS FAIL ###  
        self.assertEqual(str(context.exception), r'Invalid format! Valid formats include: "TXT", "JSON", "XML".') 
        ### TEST JOB RESULTS FAIL ###
        logTest("Fail to check job status due to invalid result format.", {'connection-id': self.npcs.connection_id, 'orderID': "TEST", 'format': "noARealFormat"},r'Invalid format! Valid formats include: "TXT", "JSON", "XML".', str(context.exception))

   # Test 20: get_status() - INVALID ORDER ID
    def test_check_status_invalid_order_id_fail(self):

        self.npcs.connect() # Get connection 

        with self.assertRaises(Exception) as context:
            self.npcs.get_results("TXT", "noARealOrderID") # Get results

        ### TEST JOB RESULTS FAIL ###  
        self.assertEqual(str(context.exception), "Result retrieval failed!") 
        ### TEST JOB RESULTS FAIL ###
        logTest("Fail to check job status due to invalid order ID.", {'connection-id': self.npcs.connection_id, 'orderID': "noARealOrderID", 'format': "TXT"},"Result retrieval failed!", str(context.exception))


   # Test 21: get_status() - INVALID CONNECTION ID
    def test_check_status_invalid_connection_id_fail(self):

        self.npcs.connect() # Get connection

        self.npcs.connection_id = "noARealConnectionID"

        with self.assertRaises(Exception) as context:
            self.npcs.get_results("TXT", "TEST") # Get results

        ### TEST JOB RESULTS FAIL ###  
        self.assertEqual(str(context.exception), "Result retrieval failed!") 
        ### TEST JOB RESULTS FAIL ###
        logTest("Fail to check job status due to invalid connection ID.", {'connection-id': self.npcs.connection_id, 'orderID': "TEST", 'format': "TXT"},"Result retrieval failed!", str(context.exception))










