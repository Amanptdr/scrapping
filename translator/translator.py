# import openpyxl
# from googletrans import Translator

# excel_file = "web_scraped_page_1_12_test.xlsx"
# workbook = openpyxl.load_workbook(excel_file)
# sheet = workbook.active
# translator = Translator()

# # Specify the column containing the text to be translated
# source_column = "A"
# target_column = "B"

# # Iterate through rows and translate the text
# for row in sheet.iter_rows(min_row=2, values_only=True):
#     source_text = row[0]  # Assuming source text is in the first column
#     try:
#         translation = translator.translate(source_text, src='auto', dest='en')
#         translated_text = translation.text
#         row[1] = translated_text  # Assuming the translated text goes in the second column
#     except Exception as e:
#         print(f"Translation error: {e}")

# workbook.save("translated_excel_file.xlsx")
# workbook.close()
from googletrans import Translator
translator = Translator()  # initalize the Translator object
df=['How are you doing today', 'Good morning, How are you ','I hope you are doing great']
translations = translator.translate(df,src='en', dest='hi')
for translation in translations:  # print every translation
    print(translation)
