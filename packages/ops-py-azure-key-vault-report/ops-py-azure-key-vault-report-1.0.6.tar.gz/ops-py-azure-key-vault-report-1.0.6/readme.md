# azure-key-vault-report

---

## Description
Generates a plain text report of secrets in the specified Key Vault.   
A json payload (MS Teams) with the report included as a html table may also be generated.   

Then table is generated and sorted (from top to bottom) by:   
- the oldest `Expiration` date, then by
- the oldest `Last Updated` date

The table also contains a `Comment` columns, which may include info about:
- Days to when the secret will expire
- Days since the secret expired
- Info if the secret has no expiration date set
- Days since the Secret was last updated

The generate_report method accepts the following argument
- `expire_threshold` : `int`  
Ignore to report the record if days till the secret will expire are more than specified value.  
**NOTE:** Secrets expiring **today** or has **already expired** will always be reported.  
Default: `None`
- `ignore_no_expiration` : `bool`  
Report all records if set to `False`. If set to `True` only secrets with `Expiration Date` set will be reported.  
Default: `True`
- `include_all` : `bool`  
If set to `True` all records are included in the output.  
Default: `False`   
- `teams_json` : `bool`  
  If set to `True` a json payload with the report as html table will also be generated.    
  Default: `False`   

The raw list, which is used to generate the report, is fetched by invoking the following shell command as subprocess:  
`az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT`

The default MS Team base payload   
```
{
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": "0076D7",
  "summary": "-",
  "sections": [
    {
      "activityTitle": "<VAULT NAME>",
      "activitySubtitle": "",
      "activityImage": "",
      "facts": [],
      "markdown": true
    },
    {
      "startGroup": true,
      "text": ""
    }
  ]
}
```   
`activityTitle` and `facts` will be generated and added. 


---

## Installation
`pip install ops-py-azure-key-vault-report`

---

## Usage

Example code:
```
from azure_key_vault_report import azure_key_vault_report

name = "kv-super-secrets"
kv_report = azure_key_vault_report.AzureKeyVaultReport(name)
kv_report.az_cmd()
kv_report.parse_results()
kv_report.generate_report()
kv_report.set_report_footer()
report = kv_report.get_report()
print(report)
---------------------------------------------------------------------------------------------------------------------------------------------
 Secret Name                                       | Last Updated      | Expiration        | Comment
---------------------------------------------------------------------------------------------------------------------------------------------
 st-verySecretSecret                               | 2022-02-16        | 2022-09-09        | Expired 451 days ago. Updated 656 days ago.
 superSecret                                       | 2023-10-31        | 2024-06-25        | Will expire in 204 days. Updated 34 days ago.
---------------------------------------------------------------------------------------------------------------------------------------------
 Secrets updated in the last year.........: 26
 Secrets NOT updated in the last year.....: 14
 Secrets NOT updated for the last 2 years.: 36
 Secrets missing Expiration Date..........: 74
 Total number of secrets..................: 76
---------------------------------------------------------------------------------------------------------------------------------------------


kv_report.generate_report(include_all=True)
kv_report.set_report_footer()
report = kv_report.get_report()
print(report)
---------------------------------------------------------------------------------------------------------------------------------------------
 Secret Name                                       | Last Updated      | Expiration        | Comment
---------------------------------------------------------------------------------------------------------------------------------------------
 st-verySecretSecret                               | 2022-02-16        | 2022-09-09        | Expired 451 days ago. Updated 656 days ago.
 superSecret                                       | 2023-10-31        | 2024-06-25        | Will expire in 204 days. Updated 34 days ago.
 ohhSooSecret                                      | 2020-12-15        |                   | Has no expiration date. Updated 1084 days ago.
 ThisWIllAlwaysBeMySecret                          | 2021-01-13        |                   | Has no expiration date. Updated 1055 days ago.
 ForgotMySecret                                    | 2021-02-04        |                   | Has no expiration date. Updated 1033 days ago.
 ...
 ---------------------------------------------------------------------------------------------------------------------------------------------
 Secrets updated in the last year.........: 26
 Secrets NOT updated in the last year.....: 14
 Secrets NOT updated for the last 2 years.: 36
 Secrets missing Expiration Date..........: 148
 Total number of secrets..................: 76
---------------------------------------------------------------------------------------------------------------------------------------------


kv_report.generate_report(expire_threshold=90)
kv_report.set_report_footer()
report = kv_report.get_report()
print(report)
---------------------------------------------------------------------------------------------------------------------------------------------
 Secret Name                                       | Last Updated      | Expiration        | Comment
---------------------------------------------------------------------------------------------------------------------------------------------
 st-verySecretSecret                               | 2022-02-16        | 2022-09-09        | Expired 451 days ago. Updated 656 days ago.
---------------------------------------------------------------------------------------------------------------------------------------------
 Secrets updated in the last year.........: 26
 Secrets NOT updated in the last year.....: 14
 Secrets NOT updated for the last 2 years.: 36
 Secrets missing Expiration Date..........: 148
 Total number of secrets..................: 76
---------------------------------------------------------------------------------------------------------------------------------------------
```

### MS Teams payload
```
import json
from azure_key_vault_report import azure_key_vault_report

name = "kv-super-secrets"
kv_report = azure_key_vault_report.AzureKeyVaultReport(name)
kv_report.az_cmd()
kv_report.parse_results()
kv_report.generate_report(teams_json=True)
report = kv_report.get_json_output()
payload = json.dumps(report)
print(payload)

{"@type": "MessageCard", "@context": "http://schema.org/extensions", "themeColor": "0076D7", "summary": "-", "sections": [{"activityTitle":...
```
