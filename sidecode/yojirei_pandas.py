import pandas as pd, operator
from sidecode import drive_file

csvfile = 'yojirei.csv'

#CSVファイルに用字例を追加する関数
def add_yojirei(index, yojirei, tip):
  #ドライブからCSVファイルをダウンロード
  drive_file.dl_csv()
  
  #文字コード"utf_8_sig"でCSVファイルを読み込み
  try:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'utf_8_sig')
  #文字コードエラーを吐いたら文字コード"shift-jis"でCSVファイルを読み込み(外部からCSVファイルを編集された場合の対策)
  except UnicodeDecodeError:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'shift-jis')
  
  #用字例を検索
  try:
    csvdata.at[index, '用字例']
  #指定された語句がCSVファイルに存在しなかったら追加してアップロード
  except KeyError:
    csvdata.loc[index] = [yojirei, tip]
    csvdata_sorted = csvdata.sort_index()
    csvdata_sorted.to_csv(csvfile, encoding = 'utf_8_sig')
    drive_file.ul_csv()
    return '登録しますっての！(ㆁᴗㆁ✿)\nご協力ありがとうございますっての！'
  #ここまでプログラムが進んだら用字例がCSVファイルに存在したということなので、エラーとして以下を返す
  return 'その用字例は既に存在していますっての…(ㆁxㆁ✿)'
  
#CSVファイルに存在する用字例を更新する関数
def update_yojirei(index, yojirei, tip):
  #ドライブからCSVファイルをダウンロード
  drive_file.dl_csv()

  #文字コード"utf_8_sig"でCSVファイルを読み込み
  try:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'utf_8_sig')
  #文字コードエラーを吐いたら文字コード"shift-jis"でCSVファイルを読み込み(外部からCSVファイルを編集された場合の対策)
  except UnicodeDecodeError:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'shift-jis')
  
  #用字例を検索
  try:
    csvdata.at[index, '用字例']
  #指定された語句がCSVファイルに存在しなかったらエラーとして以下を返す
  except KeyError:
    return 'その用字例は未登録ですっての…(ㆁxㆁ✿)'
  #指定された語句がCSVファイルに存在したらCSVを編集、アップロードして返す
  csvdata.loc[index] = [yojirei, tip]
  csvdata.to_csv(csvfile, encoding = 'utf_8_sig')
  drive_file.ul_csv()
  return '更新しますっての！(ㆁᴗㆁ✿)\n' + '【' + yojirei + '】' + tip

#CSVファイルから用字例を削除する関数
def remove_yojirei(index):
  #ドライブからCSVファイルをダウンロード
  drive_file.dl_csv()

  #文字コード"utf_8_sig"でCSVファイルを読み込み
  try:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'utf_8_sig')
  #文字コードエラーを吐いたら文字コード"shift-jis"でCSVファイルを読み込み(外部からCSVファイルを編集された場合の対策)
  except UnicodeDecodeError:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'shift-jis')
  
  #用字例を検索して削除
  try:
    csvdata_removed = csvdata.drop(index)
  #指定された語句がCSVファイルに存在しなかったらエラーとして以下を返す
  except KeyError:
    return 'その用字例は未登録ですっての…(ㆁxㆁ✿)'
  #ここまでプログラムが進んだら用字例を削除できたということなので、アップロードしてリターン
  csvdata_removed.to_csv(csvfile, encoding = 'utf_8_sig')
  drive_file.ul_csv()
  return '\"' + index + '\"を削除しますっての！(ㆁᴗㆁ✿)'

#CSVファイルをソートする関数(外部から編集したときに、気分的にソートしたければこれを使う)
def sort_yojirei():
  #ドライブからCSVファイルをダウンロード
  drive_file.dl_csv()

  #文字コード"utf_8_sig"でCSVファイルを読み込み
  try:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'utf_8_sig')
  #文字コードエラーを吐いたら文字コード"shift-jis"でCSVファイルを読み込み(外部からCSVファイルを編集された場合の対策)
  except UnicodeDecodeError:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'shift-jis')
  #CSVファイルをソートしてアップロード、リターン
  csvdata_sorted = csvdata.sort_index()
  csvdata_sorted.to_csv(csvfile, encoding = 'utf_8_sig')
  drive_file.ul_csv()
  return 'ソートしますっての！(ㆁᴗㆁ✿)'

#CSVファイルから用字例を検索する関数
def search_yojirei(index):
  #ドライブからCSVファイルをダウンロード
  drive_file.dl_csv()

  #文字コード"utf_8_sig"でCSVファイルを読み込み
  try:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'utf_8_sig')
  #文字コードエラーを吐いたら文字コード"shift-jis"でCSVファイルを読み込み(外部からCSVファイルを編集された場合の対策)
  except UnicodeDecodeError:
    csvdata = pd.read_csv(csvfile, sep = ',', header = 0, index_col = 0, encoding = 'shift-jis')

  #用字例を検索
  try:
    yojirei = csvdata.at[index, '用字例']
    tip = csvdata.at[index, '解説/備考']
  #指定された語句がCSVファイルに存在しなかったらエラーとして以下を返す
  except KeyError:
    return 'その用字例は未登録ですっての…(ㆁxㆁ✿)'
  #ここまでプログラムが進んだら用字例を取得できているということなので、以下を返す
  return '【' + yojirei + '】' + tip