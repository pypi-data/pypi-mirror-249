import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.dashboard import dashboard_metadata

def initialize_field_analysis():
    api = "/services/data/v57.0/wave/dashboards/"
    field_analysis_df = pd.DataFrame()
    CRMA_Dashboard_details_df = pd.DataFrame()
    CRMA_Dashboard_compact_details_df = pd.DataFrame()
    CRMA_Dashboard_details_df_api_name = 'CRMA_Dashboard_details'
    CRMA_Dashboard_details_df_label_name = 'CRMA Dashboard Details'
    CRMA_Dashboard_compact_details_df_api = 'CRMA_Dashboard_compact_details'
    CRMA_Dashboard_compact_details_df_label = 'CRMA Dashboard compact details'    
    return api,field_analysis_df,CRMA_Dashboard_details_df,CRMA_Dashboard_compact_details_df,CRMA_Dashboard_details_df_api_name,CRMA_Dashboard_details_df_label_name,CRMA_Dashboard_compact_details_df_api,CRMA_Dashboard_compact_details_df_label

def extract_key_value_pairs(df, column_name):
    data = df[column_name]
    types = []
    values = []
    indices = []  # Store the original indices

    for index, item in enumerate(data):
        if isinstance(item, dict):
            for key, value in item.items():
                types.append(key)
                values.append(value)
                indices.append(index)  # Store the original index

    new_df = pd.DataFrame({'Type': types, 'Value': values})
    new_df['OriginalIndex'] = indices  # Create a new index column
    return new_df

def field_analysis(sf,in_dashboard_id_df,in_upload_crma):
    api,field_analysis_df,CRMA_Dashboard_details_df,CRMA_Dashboard_compact_details_df,CRMA_Dashboard_details_df_api_name,CRMA_Dashboard_details_df_label_name,CRMA_Dashboard_compact_details_df_api,CRMA_Dashboard_compact_details_df_label = initialize_field_analysis()
    field_analysis_df = pd.DataFrame()
    CRMA_Dashboard_details_df = pd.DataFrame()
    CRMA_Dashboard_compact_details_df = pd.DataFrame()
    dashboard_df = dashboard_metadata(sf,in_upload_crma)

    for index, row in in_dashboard_id_df.iterrows():

        connector_api = api+row[0]
        while(connector_api is not None):

            # connector_api = "/services/data/v57.0/wave/dashboards/0FKOD00000000GY4AY"
            temp_rest_response = sf.query_more(connector_api, True)
            temp_details = temp_rest_response['state']['steps']
            temp_details_df = pd.DataFrame(temp_details)
            temp_details_transpose_df = temp_details_df.transpose().reset_index()
            temp_details_transpose_df = temp_details_transpose_df.rename(columns={'index':'lens_step_name'})
            temp_details_transpose_df = temp_details_transpose_df.explode('datasets', ignore_index=True)
            temp_details_transpose_df['dashboard_id'] = row[0]
            temp_details_transpose_df = temp_details_transpose_df[['dashboard_id','lens_step_name','type','label','query','datasets']]
            # temp_details_transpose_df = temp_details_transpose_df.join(temp_details_transpose_df.datasets.apply(pd.Series),how='left',lsuffix="_left", rsuffix="_right")
            # temp_details_transpose_df = pd.melt(temp_details_transpose_df, id_vars=['action','node_name', 'parameters'], var_name='node_param', value_name='value')
            # temp_details_transpose_df['datasets'] = temp_details_transpose_df['datasets'].apply(pd.Series)

            # print(row[0])
            temp_compact_dataset_df = temp_details_transpose_df[temp_details_transpose_df['type']=='aggregateflex']
            temp_compact_dataset_df['Dataset_id'] = [x.get('id') for x in temp_compact_dataset_df['datasets']]
            temp_compact_dataset_df['Dataset_label'] = [x.get('label') for x in temp_compact_dataset_df['datasets']]
            temp_compact_dataset_df['Dataset_name'] = [x.get('name') for x in temp_compact_dataset_df['datasets']]
            # # temp_details_transpose_df['Data_Connector_id'] = [x.get('id') for x in temp_details_transpose_df['dataset_1']]
            temp_compact_dataset_df  = temp_compact_dataset_df[['dashboard_id','Dataset_id','Dataset_label','Dataset_name','lens_step_name','label','query']]
            # print(2)

            # dashboard details
            tmp_dashboard_df = dashboard_df[dashboard_df['id']== row[0]][['id','folder_id','folder_name','name','label']].drop_duplicates()
            # print(3)

            tmp_dashboard_df = tmp_dashboard_df.rename(columns={'id': 'Dashboard_id', 'name': 'Dashboard_Name','label': 'Dashboard_Label'})

            # Apply the function to tmp_dataset_all_df
            temp_compact_dataset_query_exploded_df = extract_key_value_pairs(temp_compact_dataset_df, 'query')
            # Merge the two DataFrames based on the "OriginalIndex" column
            temp_compact_dataset_df = temp_compact_dataset_df.merge(temp_compact_dataset_query_exploded_df, left_index=True, right_on='OriginalIndex')
            # Drop the "OriginalIndex" column if not needed
            temp_compact_dataset_df = temp_compact_dataset_df.drop(columns='OriginalIndex')
            # Remove blank value rows
            temp_compact_dataset_df = temp_compact_dataset_df[~temp_compact_dataset_df['Value'].apply(lambda x: isinstance(x, list) and len(x) == 0)]
            temp_compact_dataset_df = temp_compact_dataset_df.merge(tmp_dashboard_df, left_on='dashboard_id',right_on='Dashboard_id').drop(columns = ['Dashboard_id'])
            temp_compact_dataset_df['api'] = connector_api
            
            
            field_analysis_df = pd.concat([field_analysis_df,temp_compact_dataset_df],axis=0)
            key_exists = temp_rest_response.get('nextPageUrl') 
            # print("before if")
            if (key_exists is not None):
                connector_api = temp_rest_response['nextPageUrl']
                # print(api , "inside if)")
            else:
                connector_api = key_exists


    CRMA_Dashboard_details_df = temp_details_transpose_df
    CRMA_Dashboard_compact_details_df = temp_compact_dataset_df
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_Dashboard_details_df,CRMA_Dashboard_details_df_api_name,CRMA_Dashboard_details_df_label_name)
        upload_to_crma(sf,CRMA_Dashboard_compact_details_df,CRMA_Dashboard_compact_details_df_api,CRMA_Dashboard_compact_details_df_label)
    return CRMA_Dashboard_details_df,CRMA_Dashboard_compact_details_df