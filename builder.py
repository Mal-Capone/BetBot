"""
A Builder page to construct the html elements of the templates
just a way to keep the app.py code to a minimum and handle most
operations away from the main app.py
"""

def results_form(region='all', outcomes=2):
    o = [
        {'opt': 2, 'sel': 'selected' if outcomes == 2 else ''},
        {'opt': 3, 'sel': 'selected' if outcomes == 3 else ''}
        ]
    r = [
        {'opt': 'UK', 'val': 'uk', 'sel': 'selected' if region == 'uk' else ''},
        {'opt': 'EU', 'val': 'eu', 'sel': 'selected' if region == 'eu' else ''},
        {'opt': 'AU', 'val': 'au', 'sel': 'selected' if region == 'au' else ''},
        {'opt': 'US', 'val': 'us', 'sel': 'selected' if region == 'us' else ''},
        {'opt': 'ALL..', 'val': 'eu,uk,au,us', 'sel': 'selected' if len(region) >= 3 else ''}
    ]
    return o, r

def results_header():
    return """      
    <div class="container-table100">
        <div class="wrap-table100">
            <div class="table100 ver4 m-b-110">
                <div class="table100-head">
                    <table>
                        <caption>Results From UBO Bot</caption>
                        <thead>
                            <tr class="row100 head">
                                {HEADER_ROW}
                            </tr>
                        </thead>
                    </table>
                </div>
                <div class="table100-body js-pscroll ps ps--active-y">
                    <table>
                        <tbody>
                            {ROW_DATA}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """

def results(response):
    try:
        columns = ['sport','league','start_date','start_time','team_a','team_a_average_price','team_b','team_b_average_price']
        headings = ['Sport','League','Start Date','Start Time','Team A','Avg A','Team B','Avg B']
        header_row ,data_row, data_rows = '','',''
        i = 0
        for cell in headings:
            i += 1
            header_row += f'<th class="cell100 column col{i}">{cell}</th>'
        row = '<tr class="row100 body">{CELLS}</tr>'
        i = 0
        for game in response['all_games']:
            for key, value in game.__dict__.items():
                if key.lower() in columns:
                    i += 1
                    data_row += f'<td class="cell100 column col{i}" style="">{str(value).title()}</td>'
            data_rows += row.format(CELLS=data_row)
            data_row = ''
            i = 0
        output = results_header().format(HEADER_ROW=header_row, ROW_DATA=data_rows)
        with open('templates/resultsview.html','w', encoding='utf-8') as file:
            file.write(output)
        return True
    except Exception as ex:
        return False

