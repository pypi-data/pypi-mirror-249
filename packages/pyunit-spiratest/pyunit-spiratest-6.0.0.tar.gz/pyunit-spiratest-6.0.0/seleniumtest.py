from selenium import selenium
import unittest
import sys, time
import spiratestextension

#	A sample Selenium test using the ability to return results back to SpiraTest
#
#	Author		Inflectra Corporation
#	Version		1.5.1
#
class TestSeleniumSample(unittest.TestCase):

    seleniumHost = 'localhost'
    seleniumPort = str(4444)
    browserStartCommand = "*firefox"
    browserURL = "http://www.google.com"

    def setUp(self):
        print "Using selenium server at " + self.seleniumHost + ":" + self.seleniumPort
        self.selenium = selenium(self.seleniumHost, self.seleniumPort, self.browserStartCommand, self.browserURL)
        self.selenium.start()

    def testGoogle__4(self):
        selenium = self.selenium
        selenium.open("http://www.google.com/webhp?hl=en")
        
        #Verifies that the title matches
        self.assertEqual ("Google", selenium.get_title())
        selenium.type("q", "Selenium OpenQA")
        
        #Verifies that it can find the Selenium website
        self.assertEqual("Selenium OpenQA", selenium.get_value("q"))
        selenium.click("btnG")
        selenium.wait_for_page_to_load("5000")
        self.assertEqual("Selenium OpenQA - Google Search", selenium.get_title())
        
    def tearDown(self):
        self.selenium.stop()
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestSeleniumSample)
testResult = unittest.TextTestRunner(verbosity=2).run(suite)
spiraTestExtension = spiratestextension.SpiraTestExtension()
spiraTestExtension.projectId = 1
spiraTestExtension.url = "http://localhost/Spira"
spiraTestExtension.userName = "administrator"
spiraTestExtension.apiKey = "{B9050F75-C5E6-4244-8712-FBF20061A976}"
spiraTestExtension.recordResults(TestSeleniumSample, testResult, -1, -1, "Selenium")

