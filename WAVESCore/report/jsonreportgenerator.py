#!/usr/bin/env python

from WAVESCore.report.reportgenerator import ReportGenerator
import json

class JSONReportGenerator(ReportGenerator):
    """
    This class allow generating reports in JSON format.
    The root dictionary contains 4 dictionaries :
    - classifications : contains the description and references of a vulnerability type.
    - vulnerabilities : each key is matching a vulnerability class. Value is a list of found vulnerabilities.
    - anomalies : same as vulnerabilities but used only for error messages and timeouts (items of less importance).
    - infos : several informations about the scan.
    """

    def __init__(self):
        # Use only one dict for vulnerability and anomaly types
        self.__flawTypes = {}

        self.__vulns = {}
        self.__anomalies = {}

        self.__infos = {}

    def setReportInfo(self, target, scope=None, date_string="", version=""):
        """Set the informations about the scan"""
        self.__infos["target"] = target
        self.__infos["date"] = date_string
        self.__infos["version"] = version
        if scope:
            self.__infos["scope"] = scope

    def generateReport(self, filename):
        """
        Generate a JSON report of the vulnerabilities and anomalies which have
        been previously logged with the log* methods.
        """
        report_dict = {"classifications": self.__flawTypes,
                       "vulnerabilities": self.__vulns,
                       "anomalies": self.__anomalies,
                       "infos": self.__infos
                       }
        f = open(filename, "w")
        try:
            json.dump(report_dict, f, indent=2)
        finally:
            f.close()

    # Vulnerabilities
    def addVulnerabilityType(self, name,
                             description="",
                             solution="",
                             references={}):
        """Add informations on a type of vulnerability"""
        if name not in self.__flawTypes:
            self.__flawTypes[name] = {'desc': description,
                                      'sol': solution,
                                      'ref': references}
        if name not in self.__vulns:
            self.__vulns[name] = []

    def logVulnerability(self,
                         category=None,
                         level=0,
                         request=None,
                         parameter="",
                         info=""):
        """
        Store the informations about a found vulnerability.
        """

        vuln_dict = {"method": request.method,
                     "path": request.file_path,
                     "info": info,
                     "level": level,
                     "parameter": parameter,
                     "http_request": request.http_repr,
                     "curl_command": request.curl_repr,
                     }
        if category not in self.__vulns:
            self.__vulns[category] = []
        self.__vulns[category].append(vuln_dict)

    # Anomalies
    def addAnomalyType(self, name,
                       description="",
                       solution="",
                       references={}):
        """Register a type of anonomaly"""
        if name not in self.__flawTypes:
            self.__flawTypes[name] = {'desc': description,
                                      'sol': solution,
                                      'ref': references}
        if name not in self.__anomalies:
            self.__anomalies[name] = []

    def logAnomaly(self,
                   category=None,
                   level=0,
                   request=None,
                   parameter="",
                   info=""):
        """
        Store the informations about an anomaly met during the attack."
        """

        anom_dict = {"method": request.method,
                     "path": request.file_path,
                     "info": info,
                     "level": level,
                     "parameter": parameter,
                     "http_request": request.http_repr,
                     "curl_command": request.curl_repr,
                     }
        if category not in self.__anomalies:
            self.__anomalies[category] = []
        self.__anomalies[category].append(anom_dict)