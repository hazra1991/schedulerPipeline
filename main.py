def call_to_check_bld():
    """ Function for checking blood pressure and saving results to google spreadsheet """
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    # call studio flow from Python app

    execution = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions \
        .create(to='+16692419870', from_=main_number)

    steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps \
        .list(limit=20)
    while len(steps) < 12:
        steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
            .executions(execution.sid) \
            .steps \
            .list(limit=20)
        time.sleep(5)
        print(len(steps))
    # sid = execution.sid
    # execution_step = client.studio \
    #                         .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
    #                         .executions('FN76531ee7fcda3617d99bec690d915045') \
    #                         .steps \
    #                         .fetch()

    # call specific Flow and Execution only for understanding and deveopment
    # execution = client.studio \
    #                   .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
    #                   .executions('FN76531ee7fcda3617d99bec690d915045') \
    #                   .fetch()

    last_step_sid = steps[0].sid
    execution_step_context = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps(last_step_sid) \
        .step_context() \
        .fetch()

    UP = execution_step_context.context['flow']['variables'].get('UP')
    DOWN = execution_step_context.context['flow']['variables'].get('DOWN')

    # PUT DATA TO SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), UP, DOWN]
    spreadsheetName = "Ekaterina"
    sheetName = "Blood_Preassure"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    sheet.append_row(new_row)
    time.sleep(5)
def check_new_user(tel=''):
    """ Function for checking type of User (NEW/EXISTING) """
    # check data in spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)
    all_sheet = sheet.get_all_values()
    phone_lst = []
    for a in all_sheet:phone_lst.append(a[0])
    tel_not_plus = str(tel[1:15])
    if tel_not_plus in phone_lst:
        return 'Exist'
    else:
        return 'New'