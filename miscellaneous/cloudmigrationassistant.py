
# coding: utf-8

# # Cloud Migration Assistant
# 
# ## Description:
# This code will evaluate the data entered as part of MAC assessment to analyze the requirement for migrating your applciations or databases into cloud. The script will give the recommended resources along with configuration and display the estimated cost of usage on a month/ annual basis.
# 
# ## Features:
# 
# <table align="center">
#     <tr>
#         <th>
#             <p ALIGN=LEFT>Feature</P>
#         </th>
#         <th>
#             <p ALIGN=LEFT>Category</P>
#         </th>
#         <th>
#             <p ALIGN=LEFT>Status</P>
#         </th>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Automatically collect Pricing Information of Google Cloud Platform services & their SKU</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Data Ingestion</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Completed</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Automatically collect various attribute values available for each service</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Data Ingestion</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>In Progress</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Collect data from MAC Assessment</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Data Ingestion</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Not Started</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Automatically map requirement to Google Cloud Platform services based on attributes</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Recommendation Engine</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Not Started</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Automatically estimate per Google Cloud Platform service cost for Monthly/ Annual Billing</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Recommendation Engine</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Not Started</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Responsive User Interface for MAC Assessment Data Entry</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>User Interface</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Not Started</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>Responsive User Interface for Services Recommendation and Cost Estimation</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>User Interface</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Not Started</P>
#         </td>
#     </tr>
# </table>
# 
# ## Authors:
# |Name|Role|Contact|
# |------|------|------|
# |Kshitij Lipare|Developer|[kshitij_lipare@syntelinc.com](kshitij_lipare@syntelinc.com)|
# 
# 
# ## Requirements:
# 1. Install the latest version of [Python](https://www.python.org/downloads/) (3.x) on your environment or upgrade if necessary
# 2. Create a [Google Cloud Platform account](https://console.cloud.google.com) or sign-in if already present
# 3. [Enable Billing API](https://console.cloud.google.com/apis/library/cloudbilling.googleapis.com) from your Google Cloud Console to make calls to the Cloud Billing Catalog API 
# 4. [Learn about Using API Keys in GCP](https://cloud.google.com/docs/authentication/api-keys), add restrictions if necessary
# 5. Install the [Google Cloud Platform SDK](https://cloud.google.com/sdk/docs/) on your environment or upgrade if necessary & understand the [gcloud format reference guide](https://cloud.google.com/sdk/gcloud/reference/#--format)
# 6. Install the [google-api-python-client](http://github.com/google/google-api-python-client) & Learn about [Using the Python Client Library](https://cloud.google.com/compute/docs/tutorials/python-guide)

# ## Check if necessary Modules are installed
# If packages are not installed then install them automatically

# In[ ]:


# Mention all the necessary packages in list pkgs
pkgs = ['json', 'requests', 'time', 'pandas', 'IPython', 'google-api-python-client']

# Start Module Installation Check
import pip
import time
import imp
import subprocess as sbp

print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'Checking installation of pip')
get_ipython().system('python -m pip install --upgrade pip')
for package in pkgs:
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'Checking installation of module: ' + package)
        imp.find_module(package)
        found = True
    except ImportError:
        found = False
    if found == False:
        print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'Not found module: ' + package)
        print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'Installing module: ' + package)
        sbp.run("pip3 install --upgrade " + package, shell=True)
        print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'Completed Installation of module: ' + package)
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'Check completed for module: ' + package)
print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'All necessary module are installed')


# ## Import required modules
# The links redirect to the individual modules documentation pages.
# 1. [json](https://docs.python.org/2/library/json.html) - This module is used to parse the JSON objects. It can encode/ decode the text objects to and from JSON objects
# 2. [requests](https://pypi.org/project/requests/) - This module is used to make API requests to given endpoints.
# 3. [time](https://docs.python.org/2/library/time.html) - This module is used for various time-related functions 
# 4. [pandas](https://pypi.org/project/pandas/) - This module is used to create and wor kwith datastructures
# 5. [IPython](https://pypi.org/project/ipython/) - This module is used to parse data in dataframes to be displayed in html format

# In[ ]:


import json
import requests
import time
import pandas as pd
from IPython.display import display, HTML


# ## Parameter Binding
# 
# <table align="left">
#     <tr>
#         <th>
#             <p ALIGN=LEFT>Parameter Name</P>
#         </th>
#         <th>
#             <p ALIGN=LEFT>Parameter Category</P>
#         </th>
#         <th>
#             <p ALIGN=LEFT>Parameter Description</P>
#         </th>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_api_key</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Gets the API Key generated through Google Cloud Console by navigating to <a href="https://console.cloud.google.com/apis/credentials?">APIs
#                     &amp; Services→Credentials</a></P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>output_path</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Mention the Path where you want to keep the extracted files (Path to be delimitted by `\\`</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>refresh_data</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>If True this will carry out the functions for Ingesting the Data from GCP sites through APIs & SDKs</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>app_managed_infra</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Do you want the Application Infrastructure on Cloud to be Managed?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>app_cpu</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>How much CPU cores are required for your Application Infrastructure on Cloud?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>app_ram</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>How much RAM (GB) are required for your Application Infrastructure on Cloud?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>app_ha</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Does your Application Infrastructure on Cloud require High Availability?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>app_regn</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>What is the preferred region for your Application Infrastructure on Cloud?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>db_managed_infra</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Do you want the Database Infrastructure on Cloud to be Managed?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>db_cpu</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>How much CPU cores are required for your Database Infrastructure on Cloud?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>db_ram</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>How much RAM (GB) are required for your Database Infrastructure on Cloud?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>db_ha</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Does your Database Infrastructure on Cloud require High Availability?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>db_regn</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Input</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>What is the preferred region for your Database Infrastructure on Cloud?</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>db_decision_matrix</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>DataFrame</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Contains the list of GCP Database & Storage attributes ['DBNAME','MANAGED','STRUCTURED','ANALYTICS','RDBMS','NOSQLKV','NOSQLDC','HA','HZSCALE','MOBILESDK','LLATENCY']</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_service_list</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>DataFrame</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Contains the list of GCP Public Servies ['serviceId', 'displayName']</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_service</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>DataFrame</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Contains the list of GCP Public Servies SKU ['gcp_service_SKU_NAME' , 'gcp_service_SKU_ID' , 'gcp_service_SKU_DESCRIPTION' , 'gcp_service_SKU_SVC_DISPLAY_NAME' , 'gcp_service_SKU_SVC_FAMILY' , 'gcp_service_SKU_GROUP' , 'gcp_service_SKU_USAGE' , 'gcp_service_SKU_REGION' , 'gcp_service_SKU_TIME' , 'gcp_service_SKU_SUMMARY' , 'gcp_service_SKU_UNIT' , 'gcp_service_SKU_UNIT_DESCRIPTION' , 'gcp_service_SKU_UNIT_DISPLAY_QUANTITY' , 'gcp_service_SKU_CONVERSION_RATE' , 'gcp_service_SKU_START_AMOUNT' , 'gcp_service_SKU_CURRENCY_CODE' , 'gcp_service_SKU_UNITS' , 'gcp_service_SKU_NANOS']</P>
#         </td>
#     </tr>    <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_gce_mc_typ</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>DataFrame</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Contains the list of GCP Compute Engine Machine Types ['id','name','description','zone','guestCpus','isSharedCpu','memoryMb','imageSpaceGb','maximumPersistentDisks','maximumPersistentDisksSizeGb']</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_gcs_tier</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>DataFrame</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Contains the list of GCP Cloud SQL Tiers ['tier','available_regions','ram','disk']</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_service_list_file</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Output</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Name of the GCP Public Service List file that will be extracted by this script</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_public_service_sku_list_file</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Output</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Name of the GCP Public Service SKU List file that will be extracted by this script</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_gce_mc_typ_list_file</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Output</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Name of the GCP Compute Engine Machine Type List file that will be extracted by this script</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>gcp_gcs_tier_list_file</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Output</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Name of the GCP Cloud SQL Tier List file that will be extracted by this script</P>
#         </td>
#     </tr>
#     <tr>
#         <td>
#             <p ALIGN=LEFT>recm_app_instance</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>Output</P>
#         </td>
#         <td>
#             <p ALIGN=LEFT>This gives the most compatible Isntance Type for your supporting your Application Workload on GCP</P>
#         </td>
#     </tr>
# </table>

# In[ ]:


gcp_api_key = 'AIzaSyCpJJA9i21CidHuHntRE7bAijJxOL-E_vk'
output_path = 'D:\\'
refresh_data = False
app_managed_infra = False
app_cpu = 2
app_ram = 7.5
app_ha = False
app_regn = 'us-central1-a'
db_managed_infra = True
db_cpu = 4
db_ram = 16
db_ha = True
db_regn = 'us-central1-b'
gcp_service_list_file = 'GCP_Service_List.csv'
gcp_public_service_sku_list_file = 'GCP_Service_Price_List.csv'
gcp_gce_mc_typ_list_file = 'GCP_Compute_Engine_Machine_Type_List.csv'
gcp_gcs_tier_list_file = 'GCP_Cloud_SQL_Tier_List.csv'


# ## Database & Storage Selection Decision Matrix
# This matrix helps identify the right database offering in Google Cloud Platform depending upon the requirements. For description about the database and storage offerings see: [Choosing a Storage Option](https://cloud.google.com/storage-options/). Below decision tree is the basis for Database & Storage Selection Matrix.![title](https://cloud.google.com/images/storage-options/flowchart.svg)
# 
# |Database/ Storage|Managed|Structured|Analytics|RDBMS|NOSQL (Key-Value)|NOSQL (Document Type)|High Availability|Horizontal Scaling|Mobile SDK|Low Latency|
# |------|------|
# |[Persistent Disk](https://cloud.google.com/persistent-disk/)|||||||Y|||Y|
# |[Cloud Storage](https://cloud.google.com/storage/)|Y||||||||||
# |[Cloud Storage for Firebase](https://firebase.google.com/docs/storage/)|Y||||||||Y||
# |[Cloud SQL](https://cloud.google.com/sql/)|Y|Y||Y|||Y||||
# |[Cloud Spanner](https://cloud.google.com/spanner/)|Y|Y||Y||||Y|||
# |[Cloud BigTable](https://cloud.google.com/bigtable/)|Y|Y|Y||Y|||Y||Y|
# |[BigQuery](https://cloud.google.com/bigquery/)|Y|Y|Y|||||Y|||
# |[Cloud DataStore](https://cloud.google.com/datastore/)|Y|Y||||Y||Y||Y|
# |[Cloud FireStore for Firebase](https://firebase.google.com/docs/firestore/)|Y|Y||||Y||Y|Y|Y|
# |[MySQL](https://www.mysql.com/)||Y||Y|||Y||||
# |[PostgreSQL](https://www.postgresql.org/)||Y||Y|||Y||||
# |[SQL Server](https://www.microsoft.com/en-us/sql-server/)||Y||Y|||Y||||
# |[Oracle](https://www.oracle.com/database/)||Y||Y|||Y||||
# |[DB2](https://www.ibm.com/analytics/us/en/db2/)||Y||Y|||Y||||

# In[ ]:


#Those database attributes which fulfill the criteria are stored as 1 and those that do not are stored as 0 in a nested list format
dm = [[ 'PERSISTENTDISK' , '0' , '0' , '0' , '0' , '0' , '0' , '1' , '0' , '0' , '1' ],[ 'STORAGE' , '1' , '0' , '0' , '0' , '0' , '0' , '0' , '0' , '0' , '0' ],[ 'STORAGEFIREBASE' , '1' , '0' , '0' , '0' , '0' , '0' , '0' , '0' , '1' , '0' ],[ 'SQL' , '1' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '0' , '0' ],[ 'SPANNER' , '1' , '1' , '0' , '1' , '0' , '0' , '0' , '1' , '0' , '0' ],[ 'BIGTABLE' , '1' , '1' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '1' ],[ 'BIGQUERY' , '1' , '1' , '1' , '0' , '0' , '0' , '0' , '1' , '0' , '0' ],[ 'DATASTORE' , '1' , '1' , '0' , '0' , '0' , '1' , '0' , '1' , '0' , '1' ],[ 'FIRESTORE' , '1' , '1' , '0' , '0' , '0' , '1' , '0' , '1' , '1' , '1' ],[ 'MYSQL' , '0' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '0' , '0' ],[ 'POSTGRESQL' , '0' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '0' , '0' ],[ 'SQLSERVER' , '0' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '0' , '0' ],[ 'ORACLE' , '0' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '0' , '0' ],[ 'DB2' , '0' , '1' , '0' , '1' , '0' , '0' , '1' , '0' , '0' , '0' ]]
db_decision_matrix = pd.DataFrame(dm, columns=[ 'DBNAME' , 'MANAGED' , 'STRUCTURED' , 'ANALYTICS' , 'RDBMS' , 'NOSQLKV' , 'NOSQLDC' , 'HA' , 'HZSCALE' , 'MOBILESDK' , 'LLATENCY' ])


# ## Listing public services from the catalog
# Get a list of all public services including relevant metadata about each service.
# For description about API Method see : [services.list](https://cloud.google.com/billing/reference/rest/v1/services/list) documentation

# In[ ]:


# This Function builds the GCP Public Service list end point and send an API Request to collect list of services
def get_gcp_service_list( gcp_api_key ):
    gcp_ep_service_list = 'https://cloudbilling.googleapis.com/v1/services?key=' + gcp_api_key
    r = requests.get(gcp_ep_service_list)

    # Check Success of the Request
    if r.status_code == 200:
        print('[{0}] Successful'.format(r.status_code))
        print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'GET Request successful for Listing GCP public services.\n\t\t\tThe `serviceid` for each service is displayed below:')

        # UnNest the JSON object and faltten the data from arrays/ lists into DataFrame
        gcp_service_list = pd.DataFrame(json.loads(r.content.decode('utf-8'))['services'])[['serviceId', 'displayName']]
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(r.status_code, r.content))
        print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GET Request failed for Listing GCP public services')
        print('\t Refer https://restfulapi.net/http-status-codes/ to understand the responses \n')
    return gcp_service_list;


# ## Getting the list of SKUs for each service
# Get a list of SKU for all public services including relevant metadata about each service SKU.
# For description about API Method see : [services.skus.list](https://cloud.google.com/billing/reference/rest/v1/services.skus/list) documentation

# In[ ]:


# This Function builds the GCP Public Service SKU list end point and send an API Request to collect SKU data for each service
def get_gcp_service_sku_list( gcp_api_key, gcp_service_list ):
    # Create a Blank DataFrame structure
    gcp_service = pd.DataFrame(columns=['gcp_service_SKU_NAME' , 'gcp_service_SKU_ID' , 'gcp_service_SKU_DESCRIPTION' , 'gcp_service_SKU_SVC_DISPLAY_NAME' , 'gcp_service_SKU_SVC_FAMILY' , 'gcp_service_SKU_GROUP' , 'gcp_service_SKU_USAGE' , 'gcp_service_SKU_REGION' , 'gcp_service_SKU_TIME' , 'gcp_service_SKU_SUMMARY' , 'gcp_service_SKU_UNIT' , 'gcp_service_SKU_UNIT_DESCRIPTION' , 'gcp_service_SKU_UNIT_DISPLAY_QUANTITY' , 'gcp_service_SKU_CONVERSION_RATE' , 'gcp_service_SKU_START_AMOUNT' , 'gcp_service_SKU_CURRENCY_CODE' , 'gcp_service_SKU_UNITS' , 'gcp_service_SKU_NANOS'])

    # Loop over the GCP Public Service list
    for serviceid in gcp_service_list['serviceId']:

        # Get the GCP Public Service Name
        dn = gcp_service_list[gcp_service_list.serviceId == serviceid]
        dn = dn['displayName']

        # Build the GCP Public Service SKU list end point and send an API Request to collect SKU data for each service
        gcp_ep_service_sku_list = 'https://cloudbilling.googleapis.com/v1/services/' + serviceid + '/skus?key=' + gcp_api_key
        r = requests.get(gcp_ep_service_sku_list)

        # Check Success of the Request
        if r.status_code == 200:
            print('[{0}] Successful'.format(r.status_code))
            print(time.strftime('%Y-%m-%d %H:%M:%S\t') + 'GET Request successful for GCP public service' + dn.to_string(index=False, header=False) + ' SKUs.')

            # Decode the Response into JSON object
            gcp_service_sku_list = json.loads(r.content.decode('utf-8'))

            # UnNest the JSON object and faltten the data from arrays/ lists into a DataFrame
            for a in gcp_service_sku_list['skus']:
                gcp_service_SKU_NAME = a['name']
                gcp_service_SKU_ID = a['skuId']
                gcp_service_SKU_DESCRIPTION = a['description']
                gcp_service_SKU_SVC_DISPLAY_NAME = a['category']['serviceDisplayName']
                gcp_service_SKU_SVC_FAMILY = a['category']['resourceFamily']
                gcp_service_SKU_GROUP = a['category']['resourceGroup']
                gcp_service_SKU_USAGE = a['category']['usageType']
                gcp_service_SKU_SERVICE_REGION = a['serviceRegions']
                for gcp_service_SKU_REGION in gcp_service_SKU_SERVICE_REGION:
                    for b in a['pricingInfo']:
                        gcp_service_SKU_TIME = b['effectiveTime']
                        gcp_service_SKU_SUMMARY = b['summary']
                        gcp_service_SKU_UNIT = b['pricingExpression']['usageUnit']
                        gcp_service_SKU_UNIT_DESCRIPTION = b['pricingExpression']['usageUnitDescription']
                        gcp_service_SKU_UNIT_DISPLAY_QUANTITY = b['pricingExpression']['displayQuantity']
                        gcp_service_SKU_CONVERSION_RATE = b['currencyConversionRate']
                        for c in b['pricingExpression']['tieredRates']:
                            gcp_service_SKU_START_AMOUNT = c['startUsageAmount']
                            gcp_service_SKU_CURRENCY_CODE = c['unitPrice']['currencyCode']
                            gcp_service_SKU_UNITS = c['unitPrice']['units']
                            gcp_service_SKU_NANOS = c['unitPrice']['nanos']
                            ################################################## Need to add aggregationInfo ############################################################
                            x = [[gcp_service_SKU_NAME , gcp_service_SKU_ID , gcp_service_SKU_DESCRIPTION , gcp_service_SKU_SVC_DISPLAY_NAME , gcp_service_SKU_SVC_FAMILY , gcp_service_SKU_GROUP , gcp_service_SKU_USAGE , gcp_service_SKU_REGION , gcp_service_SKU_TIME , gcp_service_SKU_SUMMARY , gcp_service_SKU_UNIT , gcp_service_SKU_UNIT_DESCRIPTION , gcp_service_SKU_UNIT_DISPLAY_QUANTITY , gcp_service_SKU_CONVERSION_RATE , gcp_service_SKU_START_AMOUNT , gcp_service_SKU_CURRENCY_CODE , gcp_service_SKU_UNITS , gcp_service_SKU_NANOS]]
                            y = pd.DataFrame(x, columns=['gcp_service_SKU_NAME' , 'gcp_service_SKU_ID' , 'gcp_service_SKU_DESCRIPTION' , 'gcp_service_SKU_SVC_DISPLAY_NAME' , 'gcp_service_SKU_SVC_FAMILY' , 'gcp_service_SKU_GROUP' , 'gcp_service_SKU_USAGE' , 'gcp_service_SKU_REGION' , 'gcp_service_SKU_TIME' , 'gcp_service_SKU_SUMMARY' , 'gcp_service_SKU_UNIT' , 'gcp_service_SKU_UNIT_DESCRIPTION' , 'gcp_service_SKU_UNIT_DISPLAY_QUANTITY' , 'gcp_service_SKU_CONVERSION_RATE' , 'gcp_service_SKU_START_AMOUNT' , 'gcp_service_SKU_CURRENCY_CODE' , 'gcp_service_SKU_UNITS' , 'gcp_service_SKU_NANOS'])
                            gcp_service = gcp_service.append(y, ignore_index = True)
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(r.status_code, r.content))
            print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GET Request failed for Listing GCP public services')
            print('\t Refer https://restfulapi.net/http-status-codes/ to understand the responses \n')
    return gcp_service;


# ## Get GCP Compute Engine Machine Types
# Get the list of machine types, available regions & comfigurations for GCP Compute Engine instances. For description about the SDK see: [Machine Types](https://cloud.google.com/compute/docs/machine-types) documentation

# In[ ]:


# This Function executes the gcloud command from GCP SDK for python to get the list of google compute engine machine types
def get_gcp_gce_machine_types():
    x=[]
    # Execute the gcloud command from GCP SDK for python to get the list of google compute engine machine types
    gcp_compute_mc_typ = get_ipython().getoutput('gcloud compute machine-types list --format="csv[no-heading][separator=;](id,name,description,zone,guestCpus,isSharedCpu,memoryMb,imageSpaceGb,maximumPersistentDisks,maximumPersistentDisksSizeGb)"')
    # Loop through the list of machine types stored in variable and split the values by ';'
    for y in gcp_compute_mc_typ:
        y = y.split(";")
        x.append(y)
    # Create a DataFrame to list of machine type values in proper array
    gcp_compute_mc_typ = pd.DataFrame(x,columns=['id','name','description','zone','guestCpus','isSharedCpu','memoryMb','imageSpaceGb','maximumPersistentDisks','maximumPersistentDisksSizeGb'])
    return gcp_compute_mc_typ;


# ## Get GCP Cloud SQL Tiers
# Get the list of machine types, available regions & comfigurations for Cloud SQL instances. For description about the SDK see: [Cloud SQL Tiers](https://cloud.google.com/sdk/gcloud/reference/sql/tiers/) documentation

# In[ ]:


# This Function executes the gcloud command from GCP SDK for python to get the list of google cloud sql tiers
def get_gcp_gcs_tiers():
    x=[]
    # Execute the gcloud command from GCP SDK for python to get the list of google cloud sql tiers
    gcp_gcs_tier = get_ipython().getoutput('gcloud sql tiers list --format="csv[no-heading][separator=;](\'tier\',\'available_regions\',\'ram\',\'disk\')"')
    # Loop through the list of tiers stored in variable and split the values by ';'
    for y in gcp_gcs_tier:
        y = y.split(";")
        x.append(y)
    # Create a DataFrame to list of tier values in proper array
    gcp_gcs_tier = pd.DataFrame(x,columns=['tier','available_regions','ram','disk'])
    return gcp_gcs_tier;


# ## This is where the Magic Starts!
# Call the functions for Data Ingestion

# In[ ]:


# Call the Function to get GCP Public Service List if the Refresh Data Flag is True
if refresh_data == True:
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'Get GCP Public Service List')
    gcp_service_list = get_gcp_service_list( gcp_api_key )
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Public Service List loaded Successfully')

    # Call the Function to get GCP Public Service SKU List
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'Get GCP Public Service SKU List')
    gcp_service = get_gcp_service_sku_list( gcp_api_key, gcp_service_list )
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Public Service SKU List loaded Successfully')

    # Call the Function to get GCP Compute Engine Machine Type List
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'Get GCP Compute Engine Machine Type List')
    gcp_gce_mc_typ = get_gcp_gce_machine_types()
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Compute Engine Machine Type List loaded Successfully')

    # Call the Function to get GCP Cloud SQL Tier List
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'Get GCP Cloud SQL Tier List')
    #gcp_gcs_tier = get_gcp_gcs_tiers()
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Cloud SQL Tier List loaded Successfully')
else:
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'Fetching Local Cached data for GCP Public Services & their SKUs')
    gcp_service_list =pd.read_csv(output_path + gcp_service_list_file)
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Public Service List loaded Successfully')
    gcp_service = pd.read_csv(output_path + gcp_public_service_sku_list_file)
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Public Service SKU List loaded Successfully')
    gcp_gce_mc_typ = pd.read_csv(output_path + gcp_gce_mc_typ_list_file)
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Compute Engine Machine Type List loaded Successfully')
    #gcp_gcs_tier = pd.read_csv(output_path + gcp_gcs_tier_list_file)
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'GCP Cloud SQL Tier List loaded Successfully')
        
#display(HTML(gcp_gce_mc_typ.to_html()))


# ### Application Infrastructure Recommendation Engine
# Based on the input parameters and data collected from Google Cloud Platform APIs & SDKs, select the best possible service type by following the below criteria for hosting your Application:
# 1. Is the requirement for a Managed Instance/ Service?
# 2. Is the Service available in the selected region?
# 3. Are CPU & RAM requirement matching with any of the available Instances?

# In[ ]:


# This function drills down the Google Compute Engine Machine Types by mapping them to the Application Workload Requirements
gcp_gce_mc_typ=pd.read_csv(output_path + gcp_gce_mc_typ_list_file)
def eval_app( gcp_gce_mc_typ, app_regn, app_cpu, app_ram ):
    gcp_app_instance = gcp_gce_mc_typ[(gcp_gce_mc_typ.zone == app_regn) & (gcp_gce_mc_typ.guestCpus == app_cpu) & (gcp_gce_mc_typ.memoryMb == app_ram)]
    return gcp_app_instance;
recm_app_instance = eval_app( gcp_gce_mc_typ, app_regn, app_cpu, app_ram )
recm_app_instance = recm_app_instance['name']
print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'The Instance type for Supporting your Application workload on GCP is' + recm_app_instance.to_string(index=False, header=False))


# ### Database & Storage Infrastructure Recommendation Engine
# Based on the input parameters and data collected from Google Cloud Platform APIs & SDKs, select the best possible service type by following the below criteria for hosting your Data:
# 1. Is the requirement for a Managed Instance/ Service?
# 2. Is the Service available in the selected region?
# 3. Are CPU & RAM requirement matching with any of the available Instances?
# 4. Is the Data requirement fulfilled by any of the available Service?

# In[ ]:


# This function drills down the Google Cloud SQL Tiers by mapping them to the Data & Storage Workload Requiremetns
def eval_db():
    return;


# ## Extract the Collected Data
# See the output path for all extracted files. Refer Parameter Binding for the same.

# In[ ]:


# Extract the final output of GCP Public Service SKU List in a CSV file on Local Path
gcp_service_list.to_csv(output_path + gcp_service_list_file)
print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'The ' + gcp_service_list_file + ' file has been extracted')

# Extract the final output of GCP Public Service SKU List in a CSV file on Local Path
gcp_service.to_csv(output_path + gcp_public_service_sku_list_file)
print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'The ' + gcp_public_service_sku_list_file + ' file has been extracted')

# Extract the final output of GCP Compute Engine Machine Type List in a CSV file on Local Path
gcp_gce_mc_typ.to_csv(output_path + gcp_gce_mc_typ_list_file)
print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'The ' + gcp_gce_mc_typ_list_file + ' file has been extracted')

# Extract the final output of GCP Cloud SQL Tier List in a CSV file on Local Path
gcp_gcs_tier.to_csv(output_path + gcp_gcs_tier_list_file)
print(time.strftime('%Y-%m-%d %H:%M:%S ') + 'The ' + gcp_gcs_tier_list_file + ' file has been extracted')

