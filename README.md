# sap-odata-source

SAP OData microservice connector for Sesam.io powered apps.

Supports:
- Basic Authentication
- JSON streaming of response messages
- Snapshot paging
- Odata $expand
- Delta import

## Environment variables

`SERVICE_URL` - base url to the Odata Service API

`AUTH_TYPE` - Authentication method (Default: "Basic")

`USERNAME` - Username to authenticate with the Odata Service

`PASSWORD` - Password to authenticate with the Odata Service

`LOG_LEVEL` - Default 'INFO'. Ref: https://docs.python.org/3/howto/logging.html#logging-levels

## URL parameters

Default since property for which to evaluate delta import is `lastModifiedDateTime`.

Supply `since_property=<last modified date property>` in pipe.source.url to override the default:

```
"url": "PerPerson?since_property=<last modified date property>"
```

## Example system config
```
{
  "_id": "sap-odata-source",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "AUTH_TYPE": "basic",
      "LOG_LEVEL": "INFO",
      "PASSWORD": "$SECRET(sap-password)",
      "SERVICE_URL": "https://<service_url>/odata/v2/",
      "SINCE_PROPERTY": "lastModifiedDateTime",
      "USERNAME": "$SECRET(sap-username)"
    },
    "image": "gamh/sap-odata-source:1.0",
    "port": 5000
  },
  "verify_ssl": true
}
```

## Example pipe config
```
{
  "_id": "sap-odata-source-perperson",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "sap-odata-source",
    "is_since_comparable": true,
    "supports_since": true,
    "url": "PerPerson"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"],
        ["add", "_id", "_S.personIdExternal"],
        ["add", "rdf:type",
          ["ni", "successfactors", "PerPerson"]
        ]
      ]
    }
  }
}
```

## Example response from SAP to the Microservice
```
{
  "d": {
    "results": [
      {
        "__metadata": {
          "uri": "https://<service_url>/odata/v2/PerPerson('test01')",
          "type": "SFOData.PerPerson"
        },
        "personIdExternal": "test01",
        "placeOfBirth": null,
        "lastModifiedDateTime": "/Date(1587072082000+0000)/",
        "lastModifiedBy": "adminPM",
        "createdDateTime": "/Date(1587072082000+0000)/",
        "dateOfBirth": "/Date(166838400000)/",
        "perPersonUuid": "F674BA4105E24E299485FD660935F2DF",
        "createdOn": "/Date(1587079282000)/",
        "lastModifiedOn": "/Date(1587079282000)/",
        "countryOfBirth": null,
        "createdBy": "adminPM",
        "personId": "467",
        "personalInfoNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personalInfoNav"
          }
        },
        "emergencyContactNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/emergencyContactNav"
          }
        },
        "personEmpTerminationInfoNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personEmpTerminationInfoNav"
          }
        },
        "phoneNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/phoneNav"
          }
        },
        "employmentNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/employmentNav"
          }
        },
        "countryOfBirthNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/countryOfBirthNav"
          }
        },
        "personRerlationshipNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personRerlationshipNav"
          }
        },
        "nationalIdNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/nationalIdNav"
          }
        },
        "userAccountNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/userAccountNav"
          }
        },
        "personTypeUsageNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personTypeUsageNav"
          }
        },
        "emailNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/emailNav"
          }
        },
        "homeAddressNavDEFLT": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01')/homeAddressNavDEFLT"
          }
        }
      },
      {
        "__metadata": {
          "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')",
          "type": "SFOData.PerPerson"
        },
        "personIdExternal": "test01_d0",
        "placeOfBirth": null,
        "lastModifiedDateTime": "/Date(1587072081000+0000)/",
        "lastModifiedBy": "adminPM",
        "createdDateTime": "/Date(1587072081000+0000)/",
        "dateOfBirth": "/Date(293760000000)/",
        "perPersonUuid": "61C27B6410744754A1BE0FC843454AC3",
        "createdOn": "/Date(1587079281000)/",
        "lastModifiedOn": "/Date(1587079281000)/",
        "countryOfBirth": null,
        "createdBy": "adminPM",
        "personId": "468",
        "personalInfoNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personalInfoNav"
          }
        },
        "emergencyContactNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/emergencyContactNav"
          }
        },
        "personEmpTerminationInfoNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personEmpTerminationInfoNav"
          }
        },
        "phoneNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/phoneNav"
          }
        },
        "employmentNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/employmentNav"
          }
        },
        "countryOfBirthNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/countryOfBirthNav"
          }
        },
        "personRerlationshipNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personRerlationshipNav"
          }
        },
        "nationalIdNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/nationalIdNav"
          }
        },
        "userAccountNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/userAccountNav"
          }
        },
        "personTypeUsageNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personTypeUsageNav"
          }
        },
        "emailNav": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/emailNav"
          }
        },
        "homeAddressNavDEFLT": {
          "__deferred": {
            "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/homeAddressNavDEFLT"
          }
        }
      }
    ]
  }
}
```

## Example JSON stream from the Microservice to Sesam
```
[
  {
    "__metadata": {
      "type": "SFOData.PerPerson",
      "uri": "https://<service_url>/odata/v2/PerPerson('test01')"
    },
    "countryOfBirth": null,
    "countryOfBirthNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/countryOfBirthNav"
      }
    },
    "createdBy": "adminPM",
    "createdDateTime": "2020-04-16T21:21:22+0000",
    "createdOn": "2020-04-16T23:21:22+0000",
    "dateOfBirth": "1975-04-16T00:00:00+0000",
    "emailNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/emailNav"
      }
    },
    "emergencyContactNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/emergencyContactNav"
      }
    },
    "employmentNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/employmentNav"
      }
    },
    "homeAddressNavDEFLT": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/homeAddressNavDEFLT"
      }
    },
    "lastModifiedBy": "adminPM",
    "lastModifiedDateTime": "2020-04-16T21:21:22+0000",
    "lastModifiedOn": "2020-04-16T23:21:22+0000",
    "nationalIdNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/nationalIdNav"
      }
    },
    "perPersonUuid": "F674BA4105E24E299485FD660935F2DF",
    "personEmpTerminationInfoNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personEmpTerminationInfoNav"
      }
    },
    "personId": "467",
    "personIdExternal": "test01",
    "personRerlationshipNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personRerlationshipNav"
      }
    },
    "personTypeUsageNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personTypeUsageNav"
      }
    },
    "personalInfoNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/personalInfoNav"
      }
    },
    "phoneNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/phoneNav"
      }
    },
    "placeOfBirth": null,
    "userAccountNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01')/userAccountNav"
      }
    }
  },
  {
    "__metadata": {
      "type": "SFOData.PerPerson",
      "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')"
    },
    "countryOfBirth": null,
    "countryOfBirthNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/countryOfBirthNav"
      }
    },
    "createdBy": "adminPM",
    "createdDateTime": "2020-04-16T21:21:21+0000",
    "createdOn": "2020-04-16T23:21:21+0000",
    "dateOfBirth": "1979-04-24T00:00:00+0000",
    "emailNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/emailNav"
      }
    },
    "emergencyContactNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/emergencyContactNav"
      }
    },
    "employmentNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/employmentNav"
      }
    },
    "homeAddressNavDEFLT": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/homeAddressNavDEFLT"
      }
    },
    "lastModifiedBy": "adminPM",
    "lastModifiedDateTime": "2020-04-16T21:21:21+0000",
    "lastModifiedOn": "2020-04-16T23:21:21+0000",
    "nationalIdNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/nationalIdNav"
      }
    },
    "perPersonUuid": "61C27B6410744754A1BE0FC843454AC3",
    "personEmpTerminationInfoNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personEmpTerminationInfoNav"
      }
    },
    "personId": "468",
    "personIdExternal": "test01_d0",
    "personRerlationshipNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personRerlationshipNav"
      }
    },
    "personTypeUsageNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personTypeUsageNav"
      }
    },
    "personalInfoNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/personalInfoNav"
      }
    },
    "phoneNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/phoneNav"
      }
    },
    "placeOfBirth": null,
    "userAccountNav": {
      "__deferred": {
        "uri": "https://<service_url>/odata/v2/PerPerson('test01_d0')/userAccountNav"
      }
    }
  }
]
```