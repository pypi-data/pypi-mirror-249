import json
import os
import simpleworkspace.loader as sw
import unittest
from simpleworkspace.settingsproviders import SettingsManager_JSON, SettingsManager_BasicConfig, SettingsTemplate
from configparser import ConfigParser 
from basetestcase import BaseTestCase
from simpleworkspace.utility.time import StopWatch



class CustomTemplate_JSON(SettingsTemplate):
    def __init__(self):
        self.testString1 = "str1"
        self.testString2 = "str2"
        self.testInt = 10
        self.testBool = True
        self.testList = [{"a2": 10, "b2": 100}, "nestedStr"]

class CustomTemplate_BasicConfig(SettingsTemplate):
    def __init__(self):
        self.key1:str = "val1"
        self.key2:str = "val2"


class SettingsProvidersTests(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testSettingsPath = os.path.join(cls.testPath, "settings.anyextension")

    def test_SettingsManagerJSON_Dynamic_LoadsAndSavesCorrect(self):
        settingsManager = SettingsManager_JSON(self.testSettingsPath)
        self.assertEqual(len(settingsManager.Settings.keys()),  0)
        settingsManager.LoadSettings()
        settingsManager.Settings["test1"] = 10
        settingsManager.Settings["test2"] = 20
        settingsManager.SaveSettings()
        savedSettingData = sw.io.file.Read(settingsManager._settingsPath)
        obj = json.loads(savedSettingData)
        self.assertEqual(obj, {"test1": 10, "test2": 20})
        settingsManager = SettingsManager_JSON(settingsManager._settingsPath)
        settingsManager.LoadSettings()
        self.assertEqual(settingsManager.Settings["test1"],  10)
        self.assertEqual(settingsManager.Settings["test2"],  20)

    def test_SettingsManagerJSON_Template_Defaulting_LoadsAndSavesCorrectly(self):
        settingsManager = SettingsManager_JSON[CustomTemplate_JSON](self.testSettingsPath, CustomTemplate_JSON)
        settingsManager.LoadSettings()  # nothing to load, should keep default settings
        self.assertEqual(settingsManager.Settings['testString1']          , "str1")
        self.assertEqual(settingsManager.Settings.testString1             , "str1")
        self.assertEqual(settingsManager.Settings["testInt"]              , 10    )
        self.assertEqual(settingsManager.Settings.testInt                 , 10    )
        self.assertEqual(settingsManager.Settings["testBool"]             , True  )
        self.assertEqual(settingsManager.Settings.testBool                , True  )
        self.assertEqual(settingsManager.Settings["testList"][0]          , {"a2": 10, "b2": 100} )
        self.assertEqual(settingsManager.Settings.testList[0]             , {"a2": 10, "b2": 100} )
        settingsManager.SaveSettings()

        # should still load the default settings that were saved previously
        settingsManager = SettingsManager_JSON[CustomTemplate_JSON](self.testSettingsPath, CustomTemplate_JSON)
        settingsManager.LoadSettings()  # should load same as default settings
        self.assertEqual(settingsManager.Settings.testString1             , "str1")
        self.assertEqual(settingsManager.Settings.testInt                 , 10    )
        self.assertEqual(settingsManager.Settings.testBool                , True  )
        self.assertEqual(settingsManager.Settings.testList[0]             , {"a2": 10, "b2": 100} )

    def test_SettingsManagerJSON_Template_ExistingConfig_LoadsCorrectly(self):
        sw.io.file.Create(self.testSettingsPath, json.dumps({"testInt": 999}))
        settingsManager = SettingsManager_JSON[CustomTemplate_JSON](self.testSettingsPath, CustomTemplate_JSON)
        settingsManager.LoadSettings()  # should load "testInt", should keep default settings for rest
        self.assertEqual(settingsManager.Settings['testString1']          , "str1")
        self.assertEqual(settingsManager.Settings.testString1             , "str1")
        self.assertEqual(settingsManager.Settings["testInt"]              , 999   )
        self.assertEqual(settingsManager.Settings.testInt                 , 999   )
        self.assertEqual(settingsManager.Settings["testBool"]             , True  )
        self.assertEqual(settingsManager.Settings.testBool                , True  )
        self.assertEqual(settingsManager.Settings["testList"][0]          , {"a2": 10, "b2": 100} )
        self.assertEqual(settingsManager.Settings.testList[0]             , {"a2": 10, "b2": 100} )

    def test_SettingsManagerJSON_Template_AssigmentWithDifferentIndexStyles_LoadsAndSavesCorrectly(self):
        settingsManager = SettingsManager_JSON[CustomTemplate_JSON](self.testSettingsPath, CustomTemplate_JSON)
        settingsManager.Settings.testString1 = "newstr1"
        settingsManager.Settings['testString2'] = "newstr2"
        self.assertEqual(settingsManager.Settings.testString1, "newstr1")
        self.assertEqual(settingsManager.Settings['testString1'], "newstr1")
        settingsManager.SaveSettings()

        settingsManager = SettingsManager_JSON[CustomTemplate_JSON](self.testSettingsPath, CustomTemplate_JSON)
        #check defaults before load
        self.assertEqual(settingsManager.Settings.testInt       , 10) 
        self.assertEqual(settingsManager.Settings.testString1   , "str1")
        self.assertEqual(settingsManager.Settings['testString1'], "str1")
        self.assertEqual(settingsManager.Settings.testString2   , "str2")
        self.assertEqual(settingsManager.Settings['testString2'], "str2")
        
        settingsManager.LoadSettings()
        self.assertEqual(settingsManager.Settings.testInt, 10) #should be default
        #these should be saved as new strings
        self.assertEqual(settingsManager.Settings.testString1   , "newstr1")  
        self.assertEqual(settingsManager.Settings['testString1'], "newstr1") #same but different access method
        self.assertEqual(settingsManager.Settings.testString2   , "newstr2")
        self.assertEqual(settingsManager.Settings['testString2'], "newstr2")


    def test_SettingsManagerJSON_Template_ClearSettings_ShouldNotHaveReferences(self):
        settingsManager = SettingsManager_JSON[CustomTemplate_JSON](self.testSettingsPath, CustomTemplate_JSON)
        settingsManager.LoadSettings()

        #try some deep nested lists
        settingsManager.Settings["testList"][0]["a2"] = 20
        settingsManager.Settings.testList[0]["b2"] = 200
        self.assertEqual(settingsManager.Settings["testList"][0]["a2"],  20)
        self.assertEqual(settingsManager.Settings.testList[0]["a2"],  20)
        self.assertEqual(settingsManager.Settings["testList"][0]["b2"],  200)
        self.assertEqual(settingsManager.Settings.testList[0]["b2"],  200)

        settingsManager.ClearSettings() #should restore default value, to ensure not same reference was used
        self.assertEqual(settingsManager.Settings.testInt,  10)
        self.assertEqual(settingsManager.Settings['testInt'],  10)
        self.assertEqual(settingsManager.Settings["testList"][0]["a2"],  10)
        self.assertEqual(settingsManager.Settings.testList[0]["a2"],  10)
        self.assertEqual(settingsManager.Settings["testList"][0]["b2"],  100)
        self.assertEqual(settingsManager.Settings.testList[0]["b2"],  100)

    def test_SettingsManager_BasicConfigParser_ParsesAndSavesProperly(self):
        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        self.assertEqual(len(settingsManager.Settings.keys()), 0)

        settingsManager.Settings["key1"] = "value1"
        settingsManager.Settings["key2"] = "value2"
        settingsManager.SaveSettings()

        outputData = sw.io.file.Read(self.testSettingsPath)
        assert sw.utility.regex.Match("/^key1=value1$/", outputData)
        assert sw.utility.regex.Match("/^key2=value2$/", outputData)

    def test_SettingsManager_BasicConfigParser_HandlesCommentsCorrectly(self):
        # try parse a new file
        configFileData = "\n" #empty line
        configFileData += "# start comment\n"
        configFileData += " # also a comment, since whitespace are stripped\n"
        configFileData += "\n"
        configFileData += "#key1 comment\n"
        configFileData += "key1=value1         # inline comment\n"
        configFileData += "#key2 comment, here we add some spacing to ensure its not affected\n"
        configFileData += "  key2   =    value2     \n" #should be "key2": "value2"
        configFileData += "\n"
        configFileData += "### when you add new settings, they should be added below this comment ###\n"
        sw.io.file.Create(self.testSettingsPath, configFileData)
        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        self.assertEqual(len(settingsManager.Settings.keys()), 2)
        self.assertEqual(settingsManager.Settings["key1"], "value1")
        self.assertEqual(settingsManager.Settings["key2"], "value2")

        #try export the config
        settingsManager.SaveSettings()
        outputLines = sw.io.file.Read(self.testSettingsPath).splitlines()
        self.assertEqual(outputLines[0], "")
        self.assertEqual(outputLines[1], "# start comment")
        self.assertEqual(outputLines[2], "# also a comment, since whitespace are stripped") # here the saved version should have left whitespace stripped
        self.assertEqual(outputLines[3], "")
        self.assertEqual(outputLines[4], "#key1 comment")
        self.assertEqual(outputLines[5], "key1=value1 # inline comment")
        self.assertEqual(outputLines[6], "#key2 comment, here we add some spacing to ensure its not affected")
        self.assertEqual(outputLines[7], "key2=value2") # all whitespaces stripped
        self.assertEqual(outputLines[8], "")
        self.assertEqual(outputLines[9], "### when you add new settings, they should be added below this comment ###")

        #add non existing settings before save to ensure they are added last
        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        self.assertEqual(len(settingsManager.Settings.keys()), 2)
        self.assertEqual(settingsManager.Settings["key1"], "value1")
        self.assertEqual(settingsManager.Settings["key2"], "value2")

        settingsManager.Settings["key3"] = "value3"
        settingsManager.Settings["key4"] = "value4"
        settingsManager.SaveSettings()
        outputLines = sw.io.file.Read(self.testSettingsPath).splitlines()
        self.assertEqual(len(outputLines), 12)
        self.assertEqual(outputLines[0], "")
        self.assertEqual(outputLines[1], "# start comment")
        self.assertEqual(outputLines[2], "# also a comment, since whitespace are stripped") # here the saved version should have left whitespace stripped
        self.assertEqual(outputLines[3], "")
        self.assertEqual(outputLines[4], "#key1 comment")
        self.assertEqual(outputLines[5], "key1=value1 # inline comment")
        self.assertEqual(outputLines[6], "#key2 comment, here we add some spacing to ensure its not affected")
        self.assertEqual(outputLines[7], "key2=value2") # all whitespaces stripped
        self.assertEqual(outputLines[8], "")
        self.assertEqual(outputLines[9], "### when you add new settings, they should be added below this comment ###")
        
        newdata = '\n'.join(outputLines[10:12])
        assert sw.utility.regex.Match("/^key3=value3$/",newdata)
        assert sw.utility.regex.Match("/^key4=value4$/",newdata)

        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        self.assertEqual(len(settingsManager.Settings.keys()), 4)
        self.assertEqual(settingsManager.Settings["key1"], "value1")
        self.assertEqual(settingsManager.Settings["key2"], "value2")
        self.assertEqual(settingsManager.Settings["key3"], "value3")
        self.assertEqual(settingsManager.Settings["key4"], "value4")
        del settingsManager.Settings["key1"]
        del settingsManager.Settings["key3"]

        settingsManager.SaveSettings()
        outputLines = sw.io.file.Read(self.testSettingsPath).splitlines()
        self.assertEqual(len(outputLines), 10)
        self.assertEqual(outputLines[0], "")
        self.assertEqual(outputLines[1], "# start comment")
        self.assertEqual(outputLines[2], "# also a comment, since whitespace are stripped") # here the saved version should have left whitespace stripped
        self.assertEqual(outputLines[3], "")
        self.assertEqual(outputLines[4], "#key1 comment")
        self.assertEqual(outputLines[5], "#key2 comment, here we add some spacing to ensure its not affected")
        self.assertEqual(outputLines[6], "key2=value2") # all whitespaces stripped
        self.assertEqual(outputLines[7], "")
        self.assertEqual(outputLines[8], "### when you add new settings, they should be added below this comment ###")
        self.assertEqual(outputLines[9], "key4=value4")

    def test_SettingsManager_BasicConfigParser_Template_LoadsAndSavesCorrectly(self):
        settingsManager = SettingsManager_BasicConfig[CustomTemplate_BasicConfig](self.testSettingsPath, CustomTemplate_BasicConfig)
        settingsManager.LoadSettings()  # nothing to load, should keep default settings
        self.assertEqual(settingsManager.Settings["key1"] , "val1")
        self.assertEqual(settingsManager.Settings.key2    , "val2")
        settingsManager.SaveSettings()

        outputData = sw.io.file.Read(self.testSettingsPath)
        assert sw.utility.regex.Match("/^key1=val1$/", outputData)
        assert sw.utility.regex.Match("/^key2=val2$/", outputData)

        settingsManager = SettingsManager_BasicConfig[CustomTemplate_BasicConfig](self.testSettingsPath, CustomTemplate_BasicConfig)
        settingsManager.LoadSettings()  # nothing changed, should keep default settings
        self.assertEqual(settingsManager.Settings["key1"] , "val1")
        self.assertEqual(settingsManager.Settings.key2    , "val2")

        settingsManager.Settings["key1"] = "new value1"
        settingsManager.Settings.key2 = "new value2"
        self.assertEqual(settingsManager.Settings["key1"] , "new value1")
        self.assertEqual(settingsManager.Settings.key2    , "new value2")
        settingsManager.SaveSettings()

        settingsManager = SettingsManager_BasicConfig[CustomTemplate_BasicConfig](self.testSettingsPath, CustomTemplate_BasicConfig)
        settingsManager.LoadSettings()  # nothing changed, should keep default settings
        self.assertEqual(settingsManager.Settings["key1"] , "new value1")
        self.assertEqual(settingsManager.Settings.key2    , "new value2")


    @unittest.skip
    def test_SettingsManager_BasicConfigParser_PerformanceTesting(self):
        def CreateDummySettings():
            with open(self.testSettingsPath, "w") as fp:
                fp.write(f"[DEFAULT]\n")
                for i in range(100):
                    fp.write(f"key{i}=value{i}\n")

        sw1 = StopWatch()
        sw2 = StopWatch()
        sw3 = StopWatch()
        sw4 = StopWatch()



        for i in range(100):
            CreateDummySettings()
            sw1.Start()
            settingsManager = SettingsManager_BasicConfig("./out/settings.anyextension")
            settingsManager.LoadSettings()
            sw1.Stop()
            sw2.Start()
            settingsManager.SaveSettings()
            sw2.Stop()

            CreateDummySettings()
            sw3.Start()
            cnf = ConfigParser()
            cnf.read("./out/settings.anyextension")
            sw3.Stop()
            sw4.Start()
            with open("./out/settings.anyextension", "w") as f:
                cnf.write(f)
            sw4.Stop()

        result = f"basicConfig: {sw1.GetElapsedMilliseconds()} - {sw2.GetElapsedMilliseconds()} \n"
        result += f"python ConfigParser: {sw3.GetElapsedMilliseconds()} - {sw4.GetElapsedMilliseconds()} "
        self.assertTrue(False, result) #fail on purpose