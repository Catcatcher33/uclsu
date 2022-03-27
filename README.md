# Script to update UCL Society membership list
Because downloading the Student Union membership list and manually copy pasting everything into your drive just for a simple newsletter is a massive pain.

## Usage
1. Create OAuth 2.0 credentials in the [Google Cloud API Console](https://developers.google.com/identity/protocols/oauth2).
2. Create a .env file with the necessary [sheet data](https://developers.google.com/sheets/api/guides/concepts) in the same directory:
```python
SPREADSHEET_ID = # spreadsheet ID (str)
SHEET_ID =  # sheet ID (int)
RANGE =  # range(str). Follows the A1 notation.
``` 
3. Download membership list from [Students' Union website](https://studentsunionucl.org/clubs-societies/graphic-novels-and-comics-society)
4. Run command
```
python3 update_newsletter_list.py <file_name>.csv
```
