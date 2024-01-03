import json
import re
import uuid

class FieldInterface:
    def __init__(self, name, lineageTag, annotations, formatString, fieldItem, table):
        self.raw = fieldItem
        self.name = name
        self.tableName = table.name
        self.table = table
        self.itemType = "field"
        if lineageTag == "":
            lineageTag = str(uuid.uuid1())
        self.lineageTag = lineageTag
        self.annotations = annotations
        self.formatString = formatString
        self.originalName = name
        description = self.raw["description"] if "description" in self.raw else ""
        self.displayFolder = self.raw["displayFolder"] if "displayFolder" in self.raw else ""
        if isinstance(description, list):
            self.description = "\n".join(description)
        else:
            self.description = description

    def toJSON(self):
        tmptbl = self.table
        del self.table
        tmpRaw = self.raw
        del self.raw
        tmpField = None
        if hasattr(self, "field"):
            tmpField = self.field
            if self.field:
                self.field = self.tableName+"."+tmpField.name
        output = json.dumps(self, default=lambda o: o.__dict__)
        self.table = tmptbl
        self.raw = tmpRaw
        self.field = tmpField
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.name
    def __str__(self):
        return "{}.{}".format(self.table, self.name)

class Field(FieldInterface):
    def __init__(self, name, lineageTag, annotations, formatString, dataType, summarizeBy, sourceColumnName, sourceProviderType, fieldItem, table):
        super().__init__(name, lineageTag, annotations, formatString, fieldItem, table)
        self.dataType = dataType
        self.summarizeBy = summarizeBy
        self.sourceColumnName = sourceColumnName
        self.sourceProviderType = sourceProviderType

class Measure(FieldInterface):
    def __init__(self, name, lineageTag, annotations, formatString, expression, fieldItem, table):
        super().__init__(name, lineageTag, annotations, formatString, fieldItem, table)
        self.itemType = "calculated"
        if isinstance(expression, list):
            self.expression = "\n".join(expression)
        else:
            self.expression = expression
        self.refFields = []
        matches = re.findall('(([\w_\.]*)\[([\w ]+)\])', self.expression)
        if matches:
            #raise Exception("{} uses two fields".format(self))
            #if len(matches) > 1:
            #    print("{} uses two fields".format(self))
            for match in matches:
                refFld = {"fromTable" : match[1], "fromField": match[2]}
                if match[1].lower() == '' or table.name.lower() == match[1].lower():
                    for field in table.fields:
                        if field.name.lower() == match[2].lower():
                            refFld["field"] = field
                    
                self.refFields.append(refFld)