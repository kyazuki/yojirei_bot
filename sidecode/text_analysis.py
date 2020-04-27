import re
from sidecode import yojirei_pandas

#コマンド一覧
order_add = '追加'
order_remove = '削除'
order_update = '更新'
order_sort = 'ソート'
order = [0, 0, 0, 0]

#例外一覧
class callMultiCommandsError(Exception):
  #複数コマンドを指定されたときに発生する例外
  pass
class commandSyntaxError(Exception):
  #構文の形式が不正なときに発生する例外
  pass

#テキストを引数にとり、どのコマンドかを判断して返す関数
def mode_analysis(text):
  #引数のテキストに各コマンド名が含まれていたら、対応する配列位置に出現回数を記録
  order[0] = order_add in text
  order[1] = order_remove in text
  order[2] = order_update in text
  order[3] = order_sort in text

  #配列内の数値合計が1より大きい場合は、複数コマンドが含まれているためエラー
  if sum(order) > 1:
    raise callMultiCommandsError

  #コマンドによって返り値を分岐
  if order[0]:
    return 1 #追加
  elif order[1]:
    return 2 #削除
  elif order[2]:
    return 3 #更新
  elif order[3]:
    return 4 #ソート
  else:
    return 0 #検索

#テキスト文から、"1:"などの不要部分を省いて語句/説明のみ返す関数
def match_to_text(match_object, start, end, mode = 0):
  #追加,更新の場合(1:"語句"のようになるため、先頭を3字、後ろを1字省く)
  if mode == 1:
    return match_object[start + 3 : end - 1]
  #削除,検索の場合("語句"のようになるため、先頭と後ろを1字ずつ省く)
  else:
    return match_object[start + 1 : end - 1]

#テキストとコマンド値を引数にとり、リプライ文を返す関数
def execute(mode, text):
  #追加,更新の場合
  if mode == 1 or mode == 3:
    #テキストから語句/説明が含まれる箇所を抜き出す
    index_match = re.search(r'1:"(.*?)"', text)
    yojirei_match = re.search(r'2:"(.*?)"', text)
    tip_match = re.search(r'3:"(.*?)"', text)
    
    #正しく抜き出せないときはエラー
    if index_match == yojirei_match == tip_match == None:
      raise commandSyntaxError

    #各箇所から語句/説明のみを抜き出し
    index = match_to_text(text, *index_match.span(), 1)
    yojirei = match_to_text(text, *yojirei_match.span(), 1)
    tip = match_to_text(text, *tip_match.span(), 1)

    #CSV処理にまわす
    if mode == 1: return yojirei_pandas.add_yojirei(index, yojirei, tip)
    else: return yojirei_pandas.update_yojirei(index, yojirei, tip)
  
  #削除の場合
  elif mode == 2:
    #テキストから語句が含まれる箇所を抜き出す
    index_match = re.search(r'"(.*?)"', text)

    #正しく抜き出せないときはエラー
    if index_match == None:
      raise commandSyntaxError
    
    #語句のみを抜き出し
    index = match_to_text(text, *index_match.span())

    #CSV処理にまわす
    return yojirei_pandas.remove_yojirei(index)
  
  #ソートの場合
  elif mode == 4:
    #CSV処理にまわす
    return yojirei_pandas.sort_yojirei()
  
  #検索の場合
  else:
    #テキストから語句が含まれる箇所を抜き出す
    index_match = re.search(r'"(.*?)"', text)

    #正しく抜き出せないときはエラー
    if index_match == None:
      raise commandSyntaxError
    
    #語句のみを抜き出し
    index = match_to_text(text, *index_match.span())

    #CSV処理にまわす
    return yojirei_pandas.search_yojirei(index)