# Script to update UCL Society membership list
Because downloading the Student Union membership list and manually copy pasting everything into your drive just for a simple newsletter is a massive pain.

## Usage
1. Create OAuth 2.0 credentials in the [Google Cloud API Console](https://developers.google.com/identity/protocols/oauth2) and insert them into a credentials.json and token.json file.
2. Create a virtual environment and add the libraries from the `requirements.txt` file.
3. Create a .env file with the necessary [sheet data](https://developers.google.com/sheets/api/guides/concepts) in the same directory:
```python
SPREADSHEET_ID = # spreadsheet ID (str)
SHEET_ID =  # sheet ID (int)
RANGE =  # range(str). Follows the A1 notation.
``` 
4. Download membership list from [Students' Union website](https://studentsunionucl.org/clubs-societies/).
5. Run command:
```
python3 upload.py <file_name>.csv
```
