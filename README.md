# sap-odata-source
SAP OData connector for Sesam.io powered apps

Supports:
- Basic Authentication
- JSON streaming of response messages
- Snapshot paging
- odata $expand

## Environment variables

`SERVICE_URL` - base url to the Odata Service API

`AUTH` - Authentication method (Default: "Basic")

`USERNAME` - Username to authenticate with the Odata Service

`PASSWORD` - Password to authenticate with the Odata Service

`LOG_LEVEL` - Default 'INFO'. Ref: https://docs.python.org/3/howto/logging.html#logging-levels


## Example System Config
```
{
  "_id": "successfactors",
  "type": "system:url",
  "name": "SAP SuccessFactors OData",
  "authentication": "basic",
  "password": "$SECRET(successfactors-password)",
  "url_pattern": "https://api2preview.sapsf.eu/odata/v2/%s",
  "username": "$SECRET(successfactors-username)",
  "verify_ssl": false
}

```

## Example pipe
```
{
  "_id": "successfactors-perperson",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "successfactors",
    "url": "PerPerson?$format=json"
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

## Example response from sap to the MS
```
{
  "d": {
    "results": [
      {
        "__metadata": {
          "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')",
          "type": "SFOData.FOEventReason"
        },
        "externalCode": "1",
        "startDate": "/Date(-2208988800000)/",
        "emplStatus": "998",
        "implicitPositionAction": null,
        "lastModifiedDateTime": "/Date(1587059032000+0000)/",
        "endDate": "/Date(253402214400000)/",
        "lastModifiedBy": "adminPM",
        "createdDateTime": "/Date(1587059032000+0000)/",
        "description": null,
        "createdOn": "/Date(1587066232000)/",
        "lastModifiedOn": "/Date(1587066232000)/",
        "createdBy": "adminPM",
        "name": "New Hire",
        "event": "1051",
        "status": "A",
        "emplStatusNav": {
          "__deferred": {
            "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')/emplStatusNav"
          }
        }
      },
      {
        "__metadata": {
          "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')",
          "type": "SFOData.FOEventReason"
        },
        "externalCode": "2",
        "startDate": "/Date(-2208988800000)/",
        "emplStatus": "998",
        "implicitPositionAction": null,
        "lastModifiedDateTime": "/Date(1587059032000+0000)/",
        "endDate": "/Date(253402214400000)/",
        "lastModifiedBy": "adminPM",
        "createdDateTime": "/Date(1587059032000+0000)/",
        "description": null,
        "createdOn": "/Date(1587066232000)/",
        "lastModifiedOn": "/Date(1587066232000)/",
        "createdBy": "adminPM",
        "name": "New Hire",
        "event": "1051",
        "status": "A",
        "emplStatusNav": {
          "__deferred": {
            "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')/emplStatusNav"
          }
        }
      },
      {
        ...
      }
    ]
  }
}
```

## Example response from MS to Sesam
```
{
    "__metadata": {
        "type": "SFOData.FOEventReason",
        "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')"
    },
    "createdBy": "adminPM",
    "createdDateTime": "/Date(1587059032000+0000)/",
    "createdOn": "/Date(1587066232000)/",
    "description": null,
    "emplStatus": "998",
    "emplStatusNav": {
        "__deferred": {
            "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')/emplStatusNav"
        }
    },
    "endDate": "/Date(253402214400000)/",
    "event": "1051",
    "externalCode": "1",
    "implicitPositionAction": null,
    "lastModifiedBy": "adminPM",
    "lastModifiedDateTime": "/Date(1587059032000+0000)/",
    "lastModifiedOn": "/Date(1587066232000)/",
    "name": "New Hire",
    "startDate": "/Date(-2208988800000)/",
    "status": "A"
}
```
```
{
    "__metadata": {
        "type": "SFOData.FOEventReason",
        "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')"
    },
    "createdBy": "adminPM",
    "createdDateTime": "/Date(1587059032000+0000)/",
    "createdOn": "/Date(1587066232000)/",
    "description": null,
    "emplStatus": "998",
    "emplStatusNav": {
        "__deferred": {
            "uri": "https://api2preview.sapsf.eu/odata/v2/FOEventReason(externalCode='HIRNEW',startDate=datetime'1900-01-01T00:00:00')/emplStatusNav"
        }
    },
    "endDate": "/Date(253402214400000)/",
    "event": "1051",
    "externalCode": "2",
    "implicitPositionAction": null,
    "lastModifiedBy": "adminPM",
    "lastModifiedDateTime": "/Date(1587059032000+0000)/",
    "lastModifiedOn": "/Date(1587066232000)/",
    "name": "New Hire",
    "startDate": "/Date(-2208988800000)/",
    "status": "A"
}

```