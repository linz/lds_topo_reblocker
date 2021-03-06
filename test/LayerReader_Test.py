# coding=utf-8
'''
v.0.0.1

lds_topo_reblocker - LayerReader_Test

Copyright 2011 Crown copyright (c)
Land Information New Zealand and the New Zealand Government.
All rights reserved

This program is released under the terms of the new BSD license. See the 
LICENSE file for more information.

Tests on LayerReader class

Created on 30/01/2017

@author: jramsay
'''

import unittest
import inspect
import sys
import re
import os
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../src')))

from Logger import Logger
from LayerReader import LayerReader, initds, SFDS, PGDS

testlog = Logger.setup('test')

def config():
    connstr = "PG: dbname='{d}' host='{h}' port='{p}' user='{u}' password='{x}' active_schema={s}"
    #connstr = "PG: dbname='{d}' user='{u}' password='{x}' active_schema={s}"
    p = {'host':'localhost','database':'','port':5432,'username':'','password':'','schema':'public'}
    #TorL = {'travis':{'host':'127.0.0.1','database':'','port':5432,'username':'','password':'','schema':'public'},
    #        'local' :{'host':'<dev.server>','database':'<dev.db>','port':5432,'username':'','password':'','schema':'<dev.schema>'}}
    #p = TorL['travis' if os.getenv('TRAVIS') else 'local']
    
    with open(os.path.join(os.path.dirname(__file__),"database.yml"), 'r') as dby:
        try:
            p.update(yaml.load(dby)['postgres'])
        except yaml.YAMLError as exc:
            print(exc)
    
    return connstr.format(h=p['host'],d=p['database'],p=p['port'],u=p['username'],x=p['password'],s=p['schema'])


class Test_00_LayerReaderSelfTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_10_selfTest(self):
        #assertIsNotNone added in 3.1
        self.assertNotEqual(testlog,None,'Testlog not instantiated')
        testlog.debug('LayerReader_Test Log')
    
    def test_20_layerReader_Init(self):
        #assertIsNotNone added in 3.1        
        testlog.debug('Test_0.20 LayerReader instantiation test')
        self.assertNotEqual(LayerReader(None,None),None,'LayerReader not instantiated')
        
class Test_40_LayerReader_ConfigTest(unittest.TestCase):    
    '''Test LayerReader functions'''
        
    def setUp(self):
        pgds = PGDS(config())
        self.layerreader = LayerReader(initds(SFDS,'CropRegions.shp'),pgds)
        
    def tearDown(self):
        self.layerreader = None
        
    def test_10_layerReader_Init(self):
        self.assertNotEqual(self.layerreader,None,'LayerReader not instantiated')
    
class Test_10_PGDS(unittest.TestCase):

    def setUp(self):
        self.pgds = PGDS(config())

    def tearDown(self):
        self.pgds = None

    def test_10_pgds_Init(self):
        self.assertNotEqual(self.pgds, None, 'PG DS not instantiated')

    def test_20_pgds_NormalConnect(self):
        self.pgds.connect()
        self.assertNotEqual(self.pgds.cur, None, 'PG Cursor not instantiated')
        self.pgds.disconnect()

    def test_30_pgds_ContextConnect(self):
        with PGDS(config()) as pgds:
            self.assertNotEqual(pgds.cur, None, 'PG context Cursor not instantiated')

    def test_40_pgds_ExecuteTF(self):
        with PGDS(config()) as pgds:
            res = pgds.execute('select 100', False)
            self.assertEqual(res, True, "Execute doesn't return success")

    def test_41_pgds_ExecuteRes(self):
        with PGDS(config()) as pgds:
            res = pgds.execute('select 200', True)
            self.assertEqual(res[0][0], 200, 'Execute returns wrong result')
            
    def test_50_pgds_Read(self):
        with PGDS(config()) as pgds:
            res = pgds.read(None)
            self.assertNotEqual(res,{},'No results from PG read')
            self.assertEqual(list(res.keys())[0][1] ,'new_test_pt', 'Error matching PG layerlist keys')


class Test_20_SFDS(unittest.TestCase):

    DEF_TEST_SHP = '../CropRegions.shp'
    
    def setUp(self):
        self.sfds = SFDS(self.DEF_TEST_SHP)

    def tearDown(self):
        self.sfds = None
        
    def test_10_sfds_Init(self):
        self.assertNotEqual(self.sfds, None, 'SF DS not instantiated')
        
    def test_20_sfds_Read(self):
        with SFDS(self.DEF_TEST_SHP) as sfds:
            res = sfds.read(None)
            self.assertNotEqual(res,{},'No results from SF read')
            self.assertEqual(list(res.keys())[0][1] ,'CropRegions', 'Error matching SF layerlist keys')


# class Test_30_ReadWrite(unittest.TestCase):
#     
#     def test10_s2p(self):
#         with PGDS(config()) as pxds:
#             with SFDS(self.DEF_TEST_SHP) as sfds:
#                 lr = LayerReader(pxds,sfds)   
#             
#     def test20_p2s(self):
#         with SFDS(self.DEF_TEST_SHP) as sfds:
#             with PGDS(config()) as pxds:
#                 lr = LayerReader(pxds,sfds)   


        
if __name__ == "__main__":
    unittest.main()
