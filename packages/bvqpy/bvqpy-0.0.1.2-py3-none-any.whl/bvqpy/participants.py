import pandas as pd
import numpy as np
from bvqpy.connect import connect


def participants(con):
    """
    Retrieve and update local and/or remote data from formr

    This function generates a data frame with the information of all participants
    that have participated or are candidates to participate in any of the
    versions of BVQ.

    Parameters
    ----------
    con: Connection to formr and Google Spreadsheets, as returned by `connect`

    Returns
    -------
    DataFrame: A data frame with all participants that have participated or are candidates to participate in any of the versions of BVQ Each row corresponds to a questionnaire response and each column represents a variable.

    See also
    --------
    connect: Connect to formr and Google Spreadsheets
    """

    ss = "164DMKLRO0Xju0gdfkCS3evAq9ihTgEgFiuJopmqt7mo"

    p = con.open_by_key(ss).sheet1.get_all_records()
    p = pd.DataFrame(p)
    p = p.replace(r'^\s*$', np.nan, regex=True)
    p['include'] = p['include'].astype('bool')
    p = p.dropna(subset=['code'])
    p = p[p['include']]
    p = p[['id', 'code', 'time', 'date_birth', 'date_sent',
           'version', 'randomisation', 'call']]
    p = p.rename(columns={"id": "child_id",
                          "code": "response_id",
                          "randomisation": "version_list"})
    p['response_id'] = p['response_id'].str.replace('BL', '').astype('int')
    p['version'] = p['version'].str.replace('bl-', '')
    p.sort_values(['response_id'], ascending=False)
    return p
