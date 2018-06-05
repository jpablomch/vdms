from threading import Thread
import sys
import os
import urllib
import time
import json
import unittest
import numpy as np
import vdms # Yeah, baby

hostname = "localhost"
port = 55557

class TestFindDescriptors(unittest.TestCase):

    def create_set_and_insert(self, set_name, dims, total):
        db = vdms.VDMS()
        db.connect(hostname, port)

        all_queries = []

        # Add Set
        descriptor_set = {}
        descriptor_set["name"] = set_name
        descriptor_set["dimensions"] = dims

        query = {}
        query["AddDescriptorSet"] = descriptor_set

        all_queries.append(query)

        response, img_array = db.query(all_queries)
        response = json.loads(response)
        self.assertEqual(response[0]["AddDescriptorSet"]["status"], 0)

        all_queries = []
        descriptor_blob = []

        class_counter = -1
        for i in xrange(0,total-1):
            if ((i % 4) == 0):
                class_counter += 1

            x = np.ones(dims)
            x[2] = 2.34 + i*20
            x = x.astype('float32')
            descriptor_blob.append(x.tobytes())

            descriptor = {}
            descriptor["set"] = set_name
            descriptor["label"] = "class" + str(class_counter)

            props = {}
            props["myid"] = i + 200
            descriptor["properties"] = props

            query = {}
            query["AddDescriptor"] = descriptor

            all_queries.append(query)

        response, img_array = db.query(all_queries, [descriptor_blob])

        # Check success
        response = json.loads(response)
        # print vdms.aux_print_json(response)
        for x in xrange(0,total-1):
            self.assertEqual(response[x]["AddDescriptor"]["status"], 0)

    def test_findDescByConstraints(self):

        # Add Set
        set_name = "features_128d_4_findbyConst"
        dims = 128
        total = 100
        self.create_set_and_insert(set_name, dims, total)

        db = vdms.VDMS()
        db.connect(hostname, port)

        all_queries = []

        finddescriptor = {}
        finddescriptor["set"] = set_name

        constraints = {}
        constraints["myid"] = ["==", 205]
        finddescriptor["constraints"] = constraints

        results = {}
        results["list"] = ["myid",]
        finddescriptor["results"] = results

        query = {}
        query["FindDescriptor"] = finddescriptor

        all_queries = []
        all_queries.append(query)

        response, img_array = db.query(all_queries)

        # Check success
        response = json.loads(response)
        # print vdms.aux_print_json(response)
        self.assertEqual(response[0]["FindDescriptor"]["status"], 0)
        self.assertEqual(response[0]["FindDescriptor"]["returned"], 1)
        self.assertEqual(response[0]["FindDescriptor"]
                                    ["entities"][0]["myid"], 205)


    def test_findDescByConst_get_id(self):

        # Add Set
        set_name = "features_128d_4_findDescriptors_id"
        dims = 128
        total = 100
        self.create_set_and_insert(set_name, dims, total)

        db = vdms.VDMS()
        db.connect(hostname, port)

        all_queries = []

        finddescriptor = {}
        finddescriptor["set"] = set_name

        constraints = {}
        constraints["myid"] = ["==", 205]
        finddescriptor["constraints"] = constraints

        results = {}
        results["list"] = ["myid", "_label", "_id"]
        finddescriptor["results"] = results

        query = {}
        query["FindDescriptor"] = finddescriptor

        all_queries = []
        all_queries.append(query)

        response, img_array = db.query(all_queries)

        # Check success
        response = json.loads(response)
        # print vdms.aux_print_json(response)
        self.assertEqual(response[0]["FindDescriptor"]["status"], 0)
        self.assertEqual(response[0]["FindDescriptor"]["returned"], 1)
        self.assertEqual(response[0]["FindDescriptor"]
                                    ["entities"][0]["myid"], 205)

    def test_findDescByBlob(self):

        # Add Set
        set_name = "findwith_blob"
        dims = 128
        total = 100
        self.create_set_and_insert(set_name, dims, total)

        db = vdms.VDMS()
        db.connect(hostname, port)

        kn = 3

        all_queries = []

        finddescriptor = {}
        finddescriptor["set"] = set_name

        results = {}
        results["list"] = ["myid", "_id", "_distance"]
        results["blob"] = True
        finddescriptor["results"] = results
        finddescriptor["k_neighbors"] = kn

        query = {}
        query["FindDescriptor"] = finddescriptor

        all_queries = []
        all_queries.append(query)

        descriptor_blob = []
        x = np.ones(dims)
        x[2] = 2.34 + 30*20
        x = x.astype('float32')
        descriptor_blob.append(x.tobytes())

        response, blob_array = db.query(all_queries, [descriptor_blob])

        self.assertEqual(len(blob_array), kn)
        self.assertEqual(descriptor_blob[0], blob_array[0])

        # Check success
        response = json.loads(response)
        # print vdms.aux_print_json(response)
        self.assertEqual(response[0]["FindDescriptor"]["status"], 0)
        self.assertEqual(response[0]["FindDescriptor"]["returned"], kn)

        self.assertEqual(response[0]["FindDescriptor"]
                                    ["entities"][0]["_distance"], 0)
        self.assertEqual(response[0]["FindDescriptor"]
                                    ["entities"][1]["_distance"], 400)
        self.assertEqual(response[0]["FindDescriptor"]
                                    ["entities"][2]["_distance"], 400)

