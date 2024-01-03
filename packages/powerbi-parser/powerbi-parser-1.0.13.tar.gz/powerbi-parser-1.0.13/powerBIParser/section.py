from .fields import Field
import json
import re
from .fields import Measure

class ReportField:
    def __init__(self, containerItem, dataset):
        if dataset is None:
            return
        self.containerJs = json.loads(containerItem["config"])
        self.name = self.containerJs["name"]
        self.fields = []
        if not "singleVisual" in self.containerJs:
            #raise Exception("Missing single Visual")
            if "singleVisualGroup" not in self.containerJs:
                print ("Missing single Visual in {}".format(self.name))
            return
        self.visualType = self.containerJs["singleVisual"]["visualType"]
        
        if not "projections" in self.containerJs["singleVisual"] or not self.containerJs["singleVisual"]["projections"]:
            if "objects" in self.containerJs["singleVisual"] and ("values" not in self.containerJs["singleVisual"]["objects"]or len(self.containerJs["singleVisual"]["objects"]["values"]) > 10):
                return
            raise Exception("Missing projection")
        
        for proj in self.containerJs["singleVisual"]["projections"]:
            for val in self.containerJs["singleVisual"]["projections"][proj]:
                queryRef = val["queryRef"]
                m = re.search('(([\w_\.]*)\.([\w ]+))', queryRef)
                if not m:
                    raise Exception("Unable to find match in : ".format(queryRef))
                tableStr = m.group(2)
                fieldStr = m.group(3)
                targetField = None
                measure = m.group(0) != queryRef
                for table in dataset.tables:
                    if table.name.lower() == tableStr.lower():
                        for field in table.fields:
                            if field.name.lower() == fieldStr.lower():
                                targetField = Measure(fieldStr, "", "", "", queryRef if measure else "", val, table)
                                targetField.refFields.append(field)
                if targetField is None or len(targetField.refFields) == 0:
                    #raise Exception("{} is missing in dataset {}".format(queryRef, dataset.name))
                    print ("{} is missing in dataset {}".format(queryRef, dataset.name))
                    return
                self.fields.append(targetField)
    def __repr__(self):
        return type(self).__name__+" = "+self.displayName

class Section:
    def __init__(self, sectionItem, dataset):
        self.raw = sectionItem
        self.name = sectionItem["name"]
        self.displayName = sectionItem["displayName"]
        self.containers = []
        for container in sectionItem["visualContainers"]:
            self.containers.append(ReportField(container, dataset))
        
    def toJSON(self):
        tmpRaw = self.raw
        del self.raw
        output = json.dumps(self, default=lambda o: 
                          o.__dict__ if Section == type(o) or not hasattr(o, "toJSON")else o.toJSON(), indent=4)
        self.raw = tmpRaw
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.displayName