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
                <div class="row">
                    <div class="col-md px-2 pl-2">
                        <h3 style="padding-left:10px;">Arbitage Games Found</h3>
                    </div>
                </div>
                <div class="table100-head-arb">
                    <table>
                        <thead>
                            <tr class="row100 head">
                                {ARB_HEADER_ROW}
                            </tr>
                        </thead>
                    </table>
                </div>
                <div class="table100-body js-pscroll ps ps--active-y">
                    <table>
                        <tbody>
                            {ARB_ROW_DATA}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """

def results(response):
    try:
        arbitage_games = []
        columns = ['sport','league','start_date','start_time','team_a','team_a_average_price','team_b','team_b_average_price']
        headings = ['Sport','League','Date','Time','Team A','Avg A','Team B','Avg B']
        header_row ,data_row, data_rows = '','',''
        i = 0
        for cell in headings:
            i += 1
            header_row += f'<th class="cell100 column col{i}">{cell}</th>'
        row = '<tr class="row100 body">{CELLS}</tr>'
        i = 0
        for game in response['all_games']:
            style = ''
            if game.arbitage_available:
                style = "color:green !important; font-weight:bold !important;"
                arbitage_games.append(game)
            for key, value in game.__dict__.items():
                if key.lower() in columns:
                    i += 1
                    data_row += f'<td class="cell100 column col{i}" style="{style}">{str(value).title()}</td>'
            data_rows += row.format(CELLS=data_row)
            data_row = ''
            i = 0
        arb_header, arb_rows = arb_results(arbitage_games)
        output = results_header().format(HEADER_ROW=header_row, ROW_DATA=data_rows,ARB_HEADER_ROW=arb_header, ARB_ROW_DATA=arb_rows)
        with open('templates/resultsview.html','w', encoding='utf-8') as file:
            file.write(output)
        return True
    except Exception as ex:
        return False
def arb_results(arbitage_games):
    """
    <th class="cell100 column arb-col1">Game</th>
    <th class="cell100 column arb-col2">Date</th>
    <th class="cell100 column arb-col3">Time</th>
    <th class="cell100 column arb-col4">Left Bookeeper</th>
    <th class="cell100 column arb-col5">Price</th>
    <th class="cell100 column arb-col6">Right Bookeeper</th>
    <th class="cell100 column arb-col7">Price</th>
    <th class="cell100 column arb-col8">Link</th>
    :param arbitage_games: List of Game() Objects which have arbitage oppertunities
    :return:
    """
    try:
        columns = ['','start_date','start_time','arbitage_left_bookeeper','arbitage_left_price','arbitage_right_bookeeper','arbitage_right_price','']
        headings = ['Game','Date','Time','Left Bet','Price','Right Bet','Price','Link']
        header_row ,data_row, data_rows = '','',''
        row = '<tr class="row100 body">{CELLS}</tr>'
        i = 0
        for cell in headings:
            i += 1
            if cell == 'Game':
                header_row += f'<th class="cell100 column arb-col{i}">{cell}</th>'
            else:
                header_row += f'<th class="cell100 column arb-col{i}">{cell}</th>'
        i = 0
        style = ''
        for game in arbitage_games:
            style = ''
            for key, value in game.__dict__.items():
                if key.lower() == 'game':
                    i += 1
                    data_row += f'<td class="cell100 column arb-col{i}" style="{style}">{str(game.sport + " : " + game.team_a + " vs " + game.team_b).title()}</td>'
                elif key.lower() in columns:
                    i += 1
                    data_row += f'<td class="cell100 column arb-col{i}" style="{style}">{str(value).title()}</td>'
                elif key.lower() == 'link':
                    i += 1
                    data_row += f'<td class="cell100 column arb-col{i}" style="{style}"><a href="#">https://www.linktobookerper.com<a/></td>'
            data_rows += row.format(CELLS=data_row)
            data_row = ''
            i = 0
        return header_row, data_rows
    except Exception as ex:
        return None, None

