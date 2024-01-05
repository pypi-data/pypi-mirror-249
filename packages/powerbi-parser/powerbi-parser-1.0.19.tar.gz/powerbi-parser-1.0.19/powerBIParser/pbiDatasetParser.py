import os
import json
from .table import Table
from .relationship import Relationship
from .pbiItemParser import PBIItemParser
from .fields import Field, Measure

class PBIDatasetParser(PBIItemParser):
    def __init__(self, filepath):
        super().__init__(filepath, "Dataset")
        self.filepath = filepath

    def _parseDetail(self):
        f = open(self.filepath + "/model.bim")
        dataset = json.load(f)
        f.close()
        if "compatibilityLevel" not in dataset or "model" not in dataset or type(dataset["model"]) is not dict:
            raise Exception("model.bim file is not consistent")
        self.compatibilityLevel = dataset["compatibilityLevel"]
        self.culture = dataset["model"]["culture"]
        self.cultures = dataset["model"]["cultures"]
        self.tables = []
        self.aliases = []

        for tab in dataset["model"]["tables"]:
            tbl = Table(tab["name"],tab["lineageTag"], tab["annotations"] if "annotations" in tab else None,  tab["partitions"] if "partitions" in tab else None, tab)
            if "columns" in tab:
                for col in tab["columns"]:
                    fld = Field(col["name"], col["lineageTag"], col["annotations"] if "annotations" in col else None, col["formatString"] if "formatString" in col else None,col["dataType"], col["summarizeBy"], col["sourceColumn"] if "sourceColumn" in col else "", col["sourceProviderType"] if "sourceProviderType" in col else "", col["expression"] if "expression" in col else "", col, tbl)
                    if col["name"] in tbl.renamedFields:
                        fld.originalName = tbl.renamedFields[col["name"]]
                    tbl.fields.append(fld)
            if "measures" in tab:
                for col in tab["measures"]:
                    mea = Measure(col["name"], col["lineageTag"], col["annotations"] if "annotations" in col else None, col["formatString"] if "formatString" in col else None, col["expression"] if "expression" in col else "", col, tbl)
                    if col["name"] in tbl.renamedFields:
                        mea.originalName = tbl.renamedFields[col["name"]]
                    tbl.fields.append(mea)
            self.tables.append(tbl)
        self.relations = []
        for rel in dataset["model"]["relationships"]:
            self.relations.append(Relationship(rel, self.tables))
        for culture in self.cultures:
            if "linguisticMetadata" in culture and "content" in culture["linguisticMetadata"]:
                for item, val in culture['linguisticMetadata']['content'].items():
                    if isinstance(val, dict):
                        for n,v in val.items():
                            if "Definition" in v and "Binding" in v["Definition"]:
                                dstName = v['Definition']['Binding']['ConceptualEntity']
                                dstField = v['Definition']['Binding']['ConceptualProperty'] if "ConceptualProperty" in v['Definition']['Binding'] else None
                                self.aliases.append({"srcName": n, "dstEntity": dstName, "dstField": dstField, "type": item})

        self.resolveMeasures()
        self.parsed = True
    
    def resolveMeasures(self):
        for table in self.tables:
            for mea in table.fields:
                if mea.itemType != "calculated":
                    continue
                for refFld in mea.refFields:
                    for t in self.tables:
                        if refFld["fromTable"] != "" and refFld["fromTable"].lower() != t.name.lower():
                            continue
                        for f in t.fields:
                            if f.name.lower() == refFld["fromField"].lower():
                                refFld["field"] = f
                    if "field" not in refFld:
                        print("Unable to resolve measure {}.{}".format(refFld["fromTable"], refFld["fromField"]))