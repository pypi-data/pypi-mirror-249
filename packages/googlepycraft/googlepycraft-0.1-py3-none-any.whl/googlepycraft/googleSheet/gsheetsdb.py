# Import necessary libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd

# Define a class for interacting with Google Sheets as a database
class gsheetsdb:
    def __init__(self, credentials_path='', sheet_url='') -> None:
        """
        Initialize the gsheetsdb class.

        :param credentials_path: Path to the Google Sheets service account credentials JSON file.
        :param sheet_url: URL of the Google Sheets document.
        """
        self.credentials_path = credentials_path
        self.sheet_url = sheet_url

    def read_sheet(self, key=None, number_of_rows=None, start_index=None, end_index=None):
        """
        Read data from Google Sheets.

        :param key: The column name to filter data by.
        :param number_of_rows: The number of rows to retrieve.
        :param start_index: The starting index of the rows to retrieve.
        :param end_index: The ending index of the rows to retrieve.
        :return: List of dictionaries representing the specified data.
        """
        try:
            # Set up authentication and authorization
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_url(self.sheet_url)

            # Get the first (default) sheet
            sheet = spreadsheet.sheet1

            # Get all values from the sheet
            all_values = sheet.get_all_values()

            # Create a list of dictionaries representing each row
            rows_as_dicts = []
            headers = all_values[0]

            # Convert rows to dictionaries
            for row in all_values[1:]:
                row_dict = dict(zip(headers, row))
                rows_as_dicts.append(row_dict)

            # Extract specified key, number_of_rows, and rows within the specified range
            if start_index is not None and end_index is not None:
                rows_within_range = rows_as_dicts[start_index:end_index]
            else:
                rows_within_range = rows_as_dicts

            if number_of_rows is not None:
                rows_to_return = rows_within_range[:number_of_rows]
            else:
                rows_to_return = rows_within_range

            # Print or return the specified data
            for row in rows_to_return:
                if key is not None:
                    if key in row:
                        value = row[key]
                        print(f"{key}: {value}")
                    else:
                        print(f"{key}: Not found in row")

            return rows_to_return

        except gspread.exceptions.APIError as e:
            print(f"APIError: {e.response}")
            raise

    def in_pd(self):
        """
        Convert data from Google Sheets to a Pandas DataFrame.

        :return: Pandas DataFrame.
        """
        sheet = self.read_sheet()
        if not sheet:
            pass

        # Convert the list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(sheet)
        return df

    def in_json(self, target_key=None, num_rows=None, start_index=None, end_index=None):
        """
        Convert data from Google Sheets to JSON.

        :param target_key: The specific key to include in the JSON output.
        :param num_rows: The number of rows to include in the JSON output.
        :param start_index: The starting index of the rows to include in the JSON output.
        :param end_index: The ending index of the rows to include in the JSON output.
        :return: JSON representation of the specified data.
        """
        sheet = self.read_sheet()

        if not sheet or not isinstance(sheet, list):
            return None  # or handle the case where sheet is empty or not a list

        if start_index is not None and end_index is not None:
            sheet = sheet[start_index:end_index]

        if target_key is None and num_rows is not None:
            return json.dumps(sheet[:num_rows])

        trimmed_sheet = []
        for row in sheet:
            if target_key is not None and target_key in row:
                trimmed_sheet.append({target_key: row[target_key]})
            elif target_key is None:
                trimmed_sheet.append(row)

        return json.dumps(trimmed_sheet)
