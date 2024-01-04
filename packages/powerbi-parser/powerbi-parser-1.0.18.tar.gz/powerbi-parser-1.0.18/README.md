# Python Power BI Parser
Parse Power BI files to browse dataset and report data, either from desktop or versionned workspace on GIT

## Purpose
Parse Power BI files to extract useful content

## How to Use
Easy steps:
- `pip install powerbi-parser `
- Add in the file you want `from powerBIParser import PowerBIParser` 
```
parser = PowerBIParser("filepath of the PBI sources")
    parser.parse()
    for dataset in parser.datasets:
        print (dataset.name)
    for report in parser.reports:
        print (report.name)
```

## License

This library is licensed under Apache 2.0. Full license text is available in
[LICENSE](https://github.com/Resousse/python-powerbi-parser/tree/main/LICENSE).