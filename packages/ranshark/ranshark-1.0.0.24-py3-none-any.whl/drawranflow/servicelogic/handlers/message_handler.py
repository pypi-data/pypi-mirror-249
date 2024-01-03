import logging
import numpy as np
import pandas as pd
from drawranflow.models import Identifiers, UploadedFile
from .utils import get_gnb_id, get_trgt_gnb_id
from django.db import IntegrityError, transaction


def split_values(row):
    row = str(row).strip()
    if pd.notna(row) and str(row).lower() != 'nan':
        values = str(row).split(',')
        return values[1] if len(values) > 1 else values[0]
    else:
        return np.nan


# Define reusable functions here
def filter_dataframe_by_protocol(df, protocol):
    return df[df['frame.protocols'].apply(lambda x: protocol.lower() in x.lower() if isinstance(x, str) else False)]


def update_identifiers_df(identifiers_df, condition_df, column_name):
    identifiers_df.at[condition_df.index, column_name] = condition_df.iloc[0][column_name]


def bulk_update_identifiers(identifiers_df):
    batch_size = 100  # You can adjust this based on your needs
    identifiers_to_update = []
    with transaction.atomic():
        for _ , row in identifiers_df.iterrows():
            try:
                c_rnti_value = row.get('c_rnti', None)
                if pd.isnull(c_rnti_value):
                    c_rnti_value = '00000'

                identifier_object, created = Identifiers.objects.get_or_create(
                        c_rnti=c_rnti_value,
                        gnb_du_ue_f1ap_id=row.get('gnb_du_ue_f1ap_id', None),
                        gnb_cu_ue_f1ap_id=row.get('gnb_cu_ue_f1ap_id', None),
                        gnb_cu_cp_ue_e1ap_id=row.get('gnb_cu_cp_ue_e1ap_id', None),
                        gnb_cu_up_ue_e1ap_id=row.get('gnb_cu_up_ue_e1ap_id', None),
                        ran_ue_ngap_id=row.get('ran_ue_ngap_id', None),
                        amf_ue_ngap_id=row.get('amf_ue_ngap_id', None),
                        xnap_src_ran_id=row.get('xnap_src_ran_id', None),
                        xnap_trgt_ran_id=row.get('xnap_trgt_ran_id', None),
                        pci=row.get('pci', None),
                        cucp_f1c_ip=row.get('cucp_f1c_ip', None),
                        du_f1c_ip=row.get('du_f1c_ip', None),
                        gnb_id=row.get('gnb_id', None),
                        uploaded_file_id=row['uploadedFiles_id'],
                        frame_time=row.get('frame_time', None),
                        tmsi=row.get('tmsi', None),
                        plmn = row.get('plmn', None),
                    )
                logging.debug(f"identifier_object created :{identifier_object}")


                if not created:
                    identifiers_to_update.append(identifier_object)

            except IntegrityError as e:
                logging.error(f"IntegrityError occurred during get_or_create: {e}")
            except Exception as e:
                logging.error(f"Error occurred during get_or_create: {e}")

            # Bulk update in batches
            if len(identifiers_to_update) >= batch_size:
                try:
                    Identifiers.objects.bulk_update(
                        identifiers_to_update,
                        fields=['c_rnti', 'gnb_du_ue_f1ap_id', 'gnb_cu_ue_f1ap_id', 'amf_ue_ngap_id', 'ran_ue_ngap_id',
                                'frame_time', 'cucp_f1c_ip', 'du_f1c_ip', 'gnb_id','plmn','tmsi']
                    )
                    identifiers_to_update = []
                except Exception as e:
                    logging.error(f"Error occurred during bulk update: {e}")

        # Final bulk update for any remaining objects
        if identifiers_to_update:
            try:
                Identifiers.objects.bulk_update(
                    identifiers_to_update,
                    fields=['c_rnti', 'gnb_du_ue_f1ap_id', 'gnb_cu_ue_f1ap_id', 'amf_ue_ngap_id', 'ran_ue_ngap_id',
                            'frame_time', 'cucp_f1c_ip', 'du_f1c_ip', 'gnb_id','plmn','tmsi']
                )
            except Exception as e:
                logging.error(f"Error occurred during final bulk update: {e}")


def update_identifiers(identifiers_df, match_df, column_name, actualcolumn, identifier_row, index):
    try:
        logging.debug(f"update_identifiers: {identifier_row['c_rnti']} - {column_name} - {actualcolumn}")
        new_value = match_df.iloc[0][actualcolumn]
        identifiers_df.at[index, column_name] = str(new_value)
        logging.debug(f"Updated {column_name} to {new_value}")
        return new_value
    except IndexError:
        logging.warning(f"IndexError during identifier update.")
        return None
    except Exception as e:
        logging.error(f"Error occurred during identifier update: {e}")
        return None


def find_messages(df, condition, additional_condition=None):
    try:
        if additional_condition is None:
            return df[condition]
        else:
            return df[condition & additional_condition]
    except Exception as e:
        print(f"Error occurred during message retrieval: {e}")
        return pd.DataFrame()


def message_handler(df, item_id):
    global f1ap_ue_ctxt_req, f1ap_ue_ctxt_res, ngap_path_swith_req, ngap_path_swith_res
    try:
        upload_table = UploadedFile.objects.get(id=item_id)
        logging.error(f"Initial analysis started, {upload_table.filename}")

        f1ap_df = filter_dataframe_by_protocol(df, 'f1ap')
        ngap_df = filter_dataframe_by_protocol(df, 'ngap')
        e1ap_df = filter_dataframe_by_protocol(df, 'e1ap')
        xnap_df = filter_dataframe_by_protocol(df, 'xnap')
        f1ap_df.loc[:, 'f1ap.GNB_DU_UE_F1AP_ID'] = f1ap_df['f1ap.GNB_DU_UE_F1AP_ID'].apply(split_values)

        # Find RRC Setup, Reestablishment, and Setup Request messages
        rrc_setup_df = f1ap_df[f1ap_df['_ws.col.info'] == 'RRC Setup']
        rrc_reestablish_res_df = f1ap_df[f1ap_df['_ws.col.info'] == 'RRC Reestablishment']
        rrc_setup_request_df = f1ap_df[
            (f1ap_df['_ws.col.info'] == 'RRC Setup Request') & ~f1ap_df['f1ap.C_RNTI'].isnull()]
        rrc_reestablish_df = f1ap_df[
            (f1ap_df['_ws.col.info'] == 'RRC Reestablishment Request') & ~f1ap_df['f1ap.C_RNTI'].isnull()]

        combined_df = pd.concat([rrc_setup_request_df, rrc_reestablish_df])
        combined_df.loc[:, 'f1ap.nRCellIdentity'] = combined_df['f1ap.nRCellIdentity'].map(get_gnb_id)
       # combined_df.loc[:, 'nr-rrc.ng_5G_S_TMSI_Part1'] = combined_df['nr-rrc.ng_5G_S_TMSI_Part1'].map(get_tmsi)

        service_request_df = ngap_df[
            ((ngap_df['_ws.col.info'] == 'Service request')
             | (ngap_df['_ws.col.info'] == 'Registration request')
             | (ngap_df['_ws.col.info'] == 'Tracking area update request')) & ~ngap_df['ngap.RAN_UE_NGAP_ID'].isnull()
            ]

        ngap_initial_messages_df = ngap_df[
            ((ngap_df['_ws.col.info'] == 'InitialContextSetupRequest') |

             (ngap_df['_ws.col.info'] == 'Registration Reject') |
             (ngap_df['_ws.col.info'].str.contains('Registration reject')) |
             (ngap_df['_ws.col.info'] == 'PDU Session Setup Request')) &
            ~ngap_df['ngap.RAN_UE_NGAP_ID'].isnull() &
            ~ngap_df['ngap.AMF_UE_NGAP_ID'].isnull()
            ]

        e1ap_bctxt_mesg_df = e1ap_df[(e1ap_df['_ws.col.info'] == 'BearerContextSetupRequest')
                                     & ~e1ap_df['e1ap.GNB_CU_CP_UE_E1AP_ID'].isnull()]

        e1ap_bctxt_resp_messages_df = e1ap_df[
            (e1ap_df['_ws.col.info'] == 'BearerContextSetupResponse') |
            (e1ap_df['_ws.col.info'] == 'BearerContextSetupFailure') &
            ~e1ap_df['e1ap.GNB_CU_CP_UE_E1AP_ID'].isnull() &
            ~e1ap_df['e1ap.GNB_CU_UP_UE_E1AP_ID'].isnull()
            ]
        xnap_handover_df = xnap_df[
            (xnap_df['_ws.col.info'] == 'HandoverRequest') &
            ~xnap_df['xnap.NG_RANnodeUEXnAPID_src'].isnull() &
            xnap_df['xnap.NG_RANnodeUEXnAPID_dst'].isnull()
            ]

        xnap_handover_ack_df = xnap_df[
            (xnap_df['_ws.col.info'] == 'HandoverRequestAcknowledge') &
            ~xnap_df['xnap.NG_RANnodeUEXnAPID_src'].isnull() &
            ~xnap_df['xnap.NG_RANnodeUEXnAPID_dst'].isnull()
            ]
        # Define the column mapping
        column_name_mapping = {
            'f1ap.C_RNTI': 'c_rnti',
            'f1ap.GNB_DU_UE_F1AP_ID': 'gnb_du_ue_f1ap_id',
            'f1ap.GNB_CU_UE_F1AP_ID': 'gnb_cu_ue_f1ap_id',
            'nr-rrc.pdcch_DMRS_ScramblingID': 'pci',
            'frame.time': 'frame_time',
            'ngap.RAN_UE_NGAP_ID': 'ran_ue_ngap_id',
            'ngap.AMF_UE_NGAP_ID': 'amf_ue_ngap_id',
            'ip.src': 'du_f1c_ip',
            'ip.dst': 'cucp_f1c_ip',
            'xnap.NG_RANnodeUEXnAPID_src': 'xnap_src_ran_id',
            'xnap.NG_RANnodeUEXnAPID_dst': 'xnap_trgt_ran_id',
            'e1ap.GNB_CU_CP_UE_E1AP_ID': 'gnb_cu_cp_ue_e1ap_id',
            'e1ap.GNB_CU_UP_UE_E1AP_ID': 'gnb_cu_up_ue_e1ap_id',
            'f1ap.nRCellIdentity': 'gnb_id',
            'nr-rrc.ng_5G_S_TMSI_Part1': 'tmsi',
            'f1ap.pLMN_Identity': 'plmn',
        }


        identifiers_df = combined_df[list(column_name_mapping.keys())].copy()
        # Map 'xnap.NR_Cell_Identity' to 'gnb_id' in xnap_df
        xnap_handover_df.loc[:, 'xnap.NR_Cell_Identity'] = xnap_handover_df['xnap.NR_Cell_Identity'].map(get_trgt_gnb_id).astype(str)
        # xnap_df['gnb_id'] = xnap_df['xnap.NR_Cell_Identity'].map(get_trgt_gnb_id).to_string()
        # Handle HO calls
        unique_gnb_values = combined_df['f1ap.nRCellIdentity'].unique().tolist()
        unique_gnb_values_str = [str(value) for value in unique_gnb_values]

        logging.debug(f"unique_gnb_values: {unique_gnb_values_str}")
        # Filter xnap_df based on unique_gnb_values
        xnap_df_filtered = xnap_handover_df[xnap_handover_df['xnap.NR_Cell_Identity'].isin(unique_gnb_values_str)]

        logging.debug(f"xnap_df_filtered  {xnap_df_filtered}")

        # Append filtered xnap_df to identifiers_df
        if not xnap_df_filtered.empty:
            identifiers_df = identifiers_df.append(xnap_df_filtered[[
                'f1ap.C_RNTI',
                'f1ap.GNB_DU_UE_F1AP_ID',
                'f1ap.GNB_CU_UE_F1AP_ID',
                'nr-rrc.pdcch_DMRS_ScramblingID',
                'ip.src',
                'ip.dst',
                'frame.time',
                'ngap.RAN_UE_NGAP_ID',
                'ngap.AMF_UE_NGAP_ID',
                'xnap.NG_RANnodeUEXnAPID_src',
                'xnap.NG_RANnodeUEXnAPID_dst',
                'e1ap.GNB_CU_CP_UE_E1AP_ID',
                'e1ap.GNB_CU_UP_UE_E1AP_ID',
                'f1ap.nRCellIdentity',
                'xnap.NR_Cell_Identity'
            ]])


            f1ap_ue_ctxt_req = f1ap_df[f1ap_df['_ws.col.info'] == 'UEContextSetupRequest']
            f1ap_ue_ctxt_res = f1ap_df[f1ap_df['_ws.col.info'] == 'UEContextSetupResponse']
            ngap_path_swith_req = ngap_df[ngap_df['_ws.col.info'] == 'PathSwitchRequest']
            ngap_path_swith_res = ngap_df[ngap_df['_ws.col.info'] == 'PathSwitchRequestAcknowledge']

        # Copy relevant columns from combined_df to identifiers_df
        identifiers_df.rename(columns=column_name_mapping, inplace=True)
        if not xnap_df_filtered.empty:
            # Map 'xnap.NR_Cell_Identity' to 'gnb_id'
            identifiers_df['gnb_id'] = identifiers_df['gnb_id'].combine_first(identifiers_df['xnap.NR_Cell_Identity'])

            # Drop 'xnap.NR_Cell_Identity' column if you don't need it anymore
            identifiers_df.drop(columns=['xnap.NR_Cell_Identity'], inplace=True)
        # Save to Identifiers table
        identifiers_df['uploadedFiles_id'] = item_id
        identifiers_to_update = []

        for index, identifier_row in identifiers_df.iterrows():
            try:
                logging.debug(f"identifier_row: {identifier_row}")
                identifier_time = identifier_row['frame_time']
                identifier_crnti = identifier_row['c_rnti']
                identifier_du_ip = identifier_row['du_f1c_ip']
                identifier_cucp_ip = identifier_row['cucp_f1c_ip']
                if identifier_crnti is not None and not pd.isnull(identifier_crnti):

                    matching_rrc_reestablish_res = find_messages(rrc_reestablish_res_df,
                                                                 (rrc_reestablish_res_df[
                                                                      'frame.time'] >= identifier_time) &
                                                                 (rrc_reestablish_res_df[
                                                                      'frame.time'] <= identifier_time
                                                                  + pd.Timedelta('1s')) &
                                                                 (rrc_reestablish_res_df[
                                                                      'ip.src'] == identifier_cucp_ip) &
                                                                 (rrc_reestablish_res_df[
                                                                      'ip.dst'] == identifier_du_ip) &
                                                                 (rrc_reestablish_res_df['f1ap.GNB_DU_UE_F1AP_ID'] ==
                                                                  identifier_row['gnb_du_ue_f1ap_id']))

                    gnb_cu_ue_f1ap_id = update_identifiers(identifiers_df, matching_rrc_reestablish_res,
                                                           'gnb_cu_ue_f1ap_id', 'f1ap.GNB_CU_UE_F1AP_ID',
                                                           identifier_row,
                                                           index)

                    matching_rrc_setup = find_messages(
                        rrc_setup_df,
                        (rrc_setup_df['frame.time'] >= identifier_time) &
                        (rrc_setup_df['frame.time'] <= identifier_time + pd.Timedelta('1s')) &
                        (rrc_setup_df['ip.src'] == identifier_cucp_ip) &
                        (rrc_setup_df['ip.dst'] == identifier_du_ip) &
                        (rrc_setup_df['f1ap.GNB_DU_UE_F1AP_ID'] == identifier_row['gnb_du_ue_f1ap_id'])
                    )

                    gnb_cu_ue_f1ap_id = update_identifiers(identifiers_df, matching_rrc_setup,
                                                           'gnb_cu_ue_f1ap_id', 'f1ap.GNB_CU_UE_F1AP_ID',
                                                           identifier_row,
                                                           index)

                    logging.debug(f"gnb_cu_ue_f1ap_id: {gnb_cu_ue_f1ap_id}")

                    matching_ngap_setup = find_messages(
                        service_request_df,
                        (service_request_df['frame.time'] >= identifier_row['frame_time']) &
                        (service_request_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('3s')) &
                        (service_request_df['ngap.RAN_UE_NGAP_ID'] == gnb_cu_ue_f1ap_id)
                    )

                    # Update ran_ue_ngap_id in the Identifier DataFrame
                    ran_ue_ngap_id = update_identifiers(identifiers_df, matching_ngap_setup, 'ran_ue_ngap_id',
                                                        'ngap.RAN_UE_NGAP_ID', identifier_row, index)

                    # Find NGAP Initial Context Setup messages
                    matching_ngap_ictxt_setup = find_messages(ngap_initial_messages_df,
                                                              (ngap_initial_messages_df['frame.time'] >= identifier_row[
                                                                  'frame_time']) &
                                                              (ngap_initial_messages_df['frame.time'] <= identifier_row[
                                                                  'frame_time'] + pd.Timedelta('2s')) &
                                                              (ngap_initial_messages_df[
                                                                   'ngap.RAN_UE_NGAP_ID'] == ran_ue_ngap_id))

                    # Update amf_ue_ngap_id using the update_identifiers function
                    amf_ue_ngap_id = update_identifiers(identifiers_df, matching_ngap_ictxt_setup, 'amf_ue_ngap_id',
                                                        'ngap.AMF_UE_NGAP_ID', identifier_row, index)

                    matching_e1ap_setup = find_messages(e1ap_bctxt_mesg_df,
                                                        (e1ap_bctxt_mesg_df['frame.time'] >= identifier_row[
                                                            'frame_time']) &
                                                        (e1ap_bctxt_mesg_df['frame.time'] <= identifier_row[
                                                            'frame_time'] + pd.Timedelta('2s')) &
                                                        (e1ap_bctxt_mesg_df[
                                                             'e1ap.GNB_CU_CP_UE_E1AP_ID'] == gnb_cu_ue_f1ap_id))

                    # Update gnb_cu_cp_ue_e1ap_id using the update_identifier_and_log function

                    gnb_cu_cp_ue_e1ap_id = update_identifiers(identifiers_df, matching_e1ap_setup,
                                                              'gnb_cu_cp_ue_e1ap_id',
                                                              'e1ap.GNB_CU_CP_UE_E1AP_ID', identifier_row, index)

                    matching_e1ap_resp_setup = find_messages(e1ap_bctxt_resp_messages_df,
                                                             (e1ap_bctxt_resp_messages_df['frame.time'] >=
                                                              identifier_row[
                                                                  'frame_time']) &
                                                             (e1ap_bctxt_resp_messages_df['frame.time'] <=
                                                              identifier_row[
                                                                  'frame_time'] + pd.Timedelta('10s')) &
                                                             (e1ap_bctxt_resp_messages_df[
                                                                  'e1ap.GNB_CU_CP_UE_E1AP_ID'] == gnb_cu_cp_ue_e1ap_id))

                    # Update gnb_cu_up_ue_e1ap_id using the update_identifier_and_log function
                    update_identifiers(identifiers_df, matching_e1ap_resp_setup, 'gnb_cu_up_ue_e1ap_id',
                                       'e1ap.GNB_CU_UP_UE_E1AP_ID', identifier_row, index)

                    matching_xnap_req_setup = find_messages(xnap_handover_df,
                                                            (xnap_handover_df['frame.time'] >= identifier_row[
                                                                'frame_time']) &
                                                            (xnap_handover_df['frame.time'] <= identifier_row[
                                                                'frame_time'] + pd.Timedelta(minutes=5)) &
                                                            (xnap_handover_df[
                                                                 'xnap.NG_RANnodeUEXnAPID_src'] == gnb_cu_ue_f1ap_id))

                    # Update xnap_src_ran_id using the update_identifier_and_log function
                    xnap_src_ran_id = update_identifiers(identifiers_df, matching_xnap_req_setup, 'xnap_src_ran_id',
                                                         'xnap.NG_RANnodeUEXnAPID_src', identifier_row, index)
                    matching_xnap_resp_setup = find_messages(xnap_handover_ack_df,
                                                             (xnap_handover_ack_df['frame.time'] >= identifier_row[
                                                                 'frame_time']) &
                                                             (xnap_handover_ack_df[
                                                                  'xnap.NG_RANnodeUEXnAPID_src'] == xnap_src_ran_id))

                    # Update xnap_trgt_ran_id using the update_identifier_and_log function
                    update_identifiers(identifiers_df, matching_xnap_resp_setup, 'xnap_trgt_ran_id',
                                       'xnap.NG_RANnodeUEXnAPID_dst', identifier_row, index)
                else:
                    xnap_src_ran_id = identifier_row['xnap_src_ran_id']
                    # Update gnb_cu_cp_ue_e1ap_id
                    matching_e1ap_setup = find_messages(
                        e1ap_bctxt_mesg_df,
                        (e1ap_bctxt_mesg_df['frame.time'] >= identifier_row['frame_time']) &
                        (e1ap_bctxt_mesg_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('1s'))
                    )
                    gnb_cu_cp_ue_e1ap_id = update_identifiers(
                        identifiers_df, matching_e1ap_setup,
                        'gnb_cu_cp_ue_e1ap_id', 'e1ap.GNB_CU_CP_UE_E1AP_ID', identifier_row, index
                    )
                    matching_e1ap_resp_setup = find_messages(
                        e1ap_bctxt_resp_messages_df,
                        (e1ap_bctxt_resp_messages_df['frame.time'] >= identifier_row['frame_time']) &
                        (e1ap_bctxt_resp_messages_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta(
                            '10s')) &
                        (e1ap_bctxt_resp_messages_df['e1ap.GNB_CU_CP_UE_E1AP_ID'] == gnb_cu_cp_ue_e1ap_id)

                    )
                    gnb_cu_cp_ue_e1ap_id = update_identifiers(
                        identifiers_df, matching_e1ap_resp_setup,
                        'gnb_cu_up_ue_e1ap_id', 'e1ap.GNB_CU_UP_UE_E1AP_ID', identifier_row, index
                    )
                    # Update gnb_cu_ue_f1ap_id
                    matching_f1ap_req_setup = find_messages(
                        f1ap_ue_ctxt_req,
                        (f1ap_ue_ctxt_req['frame.time'] >= identifier_row['frame_time']) &
                        (f1ap_ue_ctxt_req['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('1s'))
                    )
                    gnb_cu_ue_f1ap_id = update_identifiers(
                        identifiers_df, matching_f1ap_req_setup,
                        'gnb_cu_ue_f1ap_id', 'f1ap.GNB_CU_UE_F1AP_ID', identifier_row, index
                    )
                    # Update gnb_du_ue_f1ap_id

                    matching_f1ap_res = find_messages(
                        f1ap_ue_ctxt_res,
                        (f1ap_ue_ctxt_res['frame.time'] >= identifier_row['frame_time']) &
                        (f1ap_ue_ctxt_res['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('1s')) &
                        (f1ap_ue_ctxt_res['f1ap.GNB_CU_UE_F1AP_ID'] == gnb_cu_ue_f1ap_id)

                    )

                    update_identifiers(
                        identifiers_df, matching_f1ap_res,
                        'gnb_du_ue_f1ap_id', 'f1ap.GNB_DU_UE_F1AP_ID', identifier_row, index
                    )
                    # Update xnap_trgt_ran_id
                    matching_xnap_resp_setup = find_messages(
                        xnap_handover_ack_df,
                        (xnap_handover_ack_df['frame.time'] >= identifier_row['frame_time']) &
                        (xnap_handover_ack_df['xnap.NG_RANnodeUEXnAPID_src'] == xnap_src_ran_id) &
                        (xnap_handover_ack_df['xnap.NG_RANnodeUEXnAPID_dst'] == gnb_cu_ue_f1ap_id)

                    )
                    update_identifiers(
                        identifiers_df, matching_xnap_resp_setup,
                        'xnap_trgt_ran_id', 'xnap.NG_RANnodeUEXnAPID_dst', identifier_row, index
                    )

                    # Update ran_ue_ngap_id
                    matching_ngap_req = find_messages(
                        ngap_path_swith_req,
                        (ngap_path_swith_req['frame.time'] >= identifier_row['frame_time']) &
                        (ngap_path_swith_req['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('20s')) &
                        (ngap_path_swith_req['ngap.RAN_UE_NGAP_ID'] == gnb_cu_ue_f1ap_id)
                    )

                    ran_ue_ngap_id = update_identifiers(
                        identifiers_df, matching_ngap_req,
                        'ran_ue_ngap_id', 'ngap.RAN_UE_NGAP_ID', identifier_row, index
                    )

                    matching_ngap_res = find_messages(
                        ngap_path_swith_res,
                        (ngap_path_swith_res['frame.time'] >= identifier_row['frame_time']) &
                        (ngap_path_swith_res['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('20s')) &
                        (ngap_path_swith_res['ngap.RAN_UE_NGAP_ID'] == ran_ue_ngap_id)
                    )

                    update_identifiers(
                        identifiers_df, matching_ngap_res,
                        'amf_ue_ngap_id', 'ngap.AMF_UE_NGAP_ID', identifier_row, index
                    )

            except Exception as e:
                logging.error(f"Error occurred during row processing: {e}")
        bulk_update_identifiers(identifiers_df)
        logging.error(f"Initial analysis has been completed, {upload_table.filename}")

    except Exception as e:
        logging.error("Error - Message Handler", e)

