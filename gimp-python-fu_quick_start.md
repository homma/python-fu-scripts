Title: 5 分で始める GIMP Python-Fu
Tags: GIMP Python Python-Fu 画像処理

# 3 行まとめ

GIMP の機能拡張用スクリプト (Python-Fu) のショート・チュートリアルです。
Python から GIMP を操作する基本的な方法をご紹介します。
習うより慣れろ式のチュートリアルですので、難易度は低めです。

# まえがき

## GIMP について
GIMP はオープンソースのお絵かきツールです。
分類的には、ピクセル単位で画像を操作するペイント系のツールです。
たくさんの機能が備わっていますが無料で使うことができます。
数年前から Mac OS X でもネイティブに（X11 不要で）動作するようになりました。
Mac にはデフォルトでお絵かきツールが入っていませんので、入れておくと良いアプリの一つです。

このチュートリアルは GIMP 2.8 を前提としています。
2.8 に近いバージョンであれば変更不要で実行できると思います。

## Python-Fu について
GIMP には機能拡張用のライブラリが付属しており、プログラムから GIMP を操作することができるようになっています。
この機能拡張用のライブラリを Python でラッピングしたものが Python-Fu と呼ばれる仕組みです。

Python-Fu を使用すると、Python のスクリプトで GIMP に機能を追加したり、GIMP の操作を自動化することができます。
大量の定型処理やパラメータを少しずつ変更して繰り返しの処理を実行させたい時などに便利です。
例えば、画像の背景に集中線を入れたい場合は、手動で何十本も線を引くよりプログラムで処理した方が簡単です。

## 前提知識
なんでも良いのでお絵かきツールを使ったことがあって、多少でも Python が書ければ十分です。

## この記事について
もしどこかに間違いがあったらごめんなさい。

# GIMP のインストール

## ダウンロード
お使いの OS 用のバイナリを [ここ](https://www.gimp.org/downloads/) からダウンロードしてインストールしてください。

- https://www.gimp.org/downloads/

## GIMP の起動
Mac OS X の場合は初めてアプリを起動する時にセキュリティチェックがかかります。
Ctrl-クリックで起動するとチェックを回避できますが、自己責任で実行してください。
それ以外にも、初期化処理などで初回の起動は少し時間が掛かります。

# Python-Fu スクリプトを実行する
今回は Python-Fu コンソールから Python-Fu スクリプトを実行する方法をご紹介します。

## コンソールの表示
GIMP のメニューから、フィルター >> Python-Fu >> コンソール を選択すると、Python-Fu のコンソールが開いて Python のプロンプトが表示されます。

このプロンプトが表示された状態で GIMP のライブラリはロード済みです。
Python から GIMP の機能を使う際に追加の作業は必要ありません。
いきなりライブラリの関数を呼び出して GIMP を操作することが可能です。

## プログラムの入力と実行
Python-Fu の機能を実感していただくためのサンプル・スクリプトを用意しました。

この下のコードをまるっとコピーして、Python-Fu コンソールにペーストしてみてください。
一番下の main() まで入力が終わると、新しいウィンドウが開いて画像が表示されるはずです。
まずはお試しください。

```` python
# Python-Fu のサンプル・スクリプト
# GIMP の Python-Fu コンソールにコピペして実行してください

# 画像データの作成
## 指定したサイズで画像データを作成する
### width : 画像データの幅 (px)
### height : 画像データの高さ (px)
def create_image(width, height):
  # 画像データを生成
  return gimp.Image(width, height, RGB)

# レイヤーの追加
## 指定した名前のレイヤーを新規に作成し、画像データに挿入する
### image : レイヤーを追加する画像データ
### name : 新規に作成するレイヤーの名前（文字列）
def add_layer(image, name):
  # レイヤーの作成に必要なパラメータ
  width   = image.width
  height  = image.height
  type    = RGB_IMAGE
  opacity = 100
  mode    = NORMAL_MODE
  
  # パラメータをもとにレイヤーを作成
  layer = gimp.Layer(image, name, width, height, type, opacity, mode)
  
  # レイヤーを背景色で塗りつぶす（GIMP のデフォルトの挙動に合わせています）
  layer.fill(1)
  
  # 画像データの 0 番目の位置にレイヤーを挿入する
  position = 0
  image.add_layer(layer, position)
  
  return layer

# ペンシルツールで線を描く
## 配列に格納した座標列を結ぶ線を描画領域にペンシルツールで描く
### drawable : 描画領域（レイヤーなど）
### lines : 描画される線の座標列を格納した配列
def draw_pencil_lines(drawable, lines):
  # ペンシルツールで線を描画する
  pdb.gimp_pencil(drawable, len(lines), lines)

# ペンシルツールで矩形を描く
## 左上、右下座標をもとに描画領域に矩形を描く
### drawable : 描画領域（レイヤーなど）
### x1 : 左上の X 座標
### y1 : 左上の Y 座標
### x2 : 右下の X 座標
### y2 : 右下の Y 座標
def draw_rect(drawable, x1, y1, x2, y2):
  lines = [x1, y1, x2, y1, x2, y2, x1, y2, x1, y1]
  draw_pencil_lines(drawable, lines)

# エアブラシで線を描く
## 配列に格納した座標列を結ぶ線を描画領域にエアブラシで描く
### drawable : 描画領域（レイヤーなど）
### pressure : 筆圧 (0-100)
### lines : 描画される線の座標列を格納した配列
def draw_airbrush_lines(drawable, pressure, lines):
  # エアブラシで線を描画する
  pdb.gimp_airbrush(drawable, pressure, len(lines), lines)

# 文字列を描画する
## 指定した描画領域に文字列を描画します
### drawable : 描画領域（レイヤーなど）
### x : 文字列を描画する位置の X 座標
### y : 文字列を描画する位置の Y 座標
### size : フォントサイズ
### str : 描画する文字列
def draw_text(drawable, x, y, size, str):
  image = drawable.image
  border = -1
  antialias = True
  size_type = PIXELS
  fontname = '*'
  floating_sel = pdb.gimp_text_fontname(image, drawable, x, y, str, border,
                 antialias, size, size_type, fontname)
  pdb.gimp_floating_sel_anchor(floating_sel)

# 描画する色を変更する
## パレットの前景色を変更して描画色を設定する
### r : 赤要素 (0-255)
### g : 緑要素 (0-255)
### b : 青要素 (0-255)
### a : 透明度 (0-1.0)
def set_color(r, g, b, a):
  color = (r, g, b, a)
  pdb.gimp_context_set_foreground(color)

# 描画する線の太さを変える
## ブラシのサイズを変更して線の太さを設定する
### width : 線の太さ
def set_line_width(width):
  pdb.gimp_context_set_brush_size(width)

# 画像の表示
## 新しいウィンドウを作成し、画像データを表示する
### image : 表示する画像データ
def display_image(image):
  gimp.Display(image)

def main():
  image = create_image(640, 400)
  layer = add_layer(image, "背景")
  draw_rect(layer, 390, 210, 490, 310)
  draw_text(layer, 200, 180, 20, "こんにちは")
  lines = [110,90, 120,180, 130,110, 140,150]
  draw_airbrush_lines(layer, 75, lines)
  set_color(255,0,0,1.0)  # Red
  set_line_width(1)
  draw_rect(layer, 420, 240, 520, 340)
  display_image(image)

main()
````

問題が発生しなければ、新しいウィンドウが作成されて、画像が表示されたはずです。

ここまで 5 分でできましたでしょうか。
ソフトウェアのインストールとコピペだけですので、つまずきそうな難しい部分はなかったのではないかと思います。

続いて、いま実行したスクリプトの処理の中身を解説していきます。

# プログラムの解説

## プログラム全体の構成

上記のスクリプトでは、まず画像データを作成・加工するのに必要な補助関数を定義しています。
プログラム内に画像データを確保する関数、レイヤーを作成する関数、図形の描画に必要な関数、文字列を書き込むための関数、作成した画像を表示するための関数などです。

それらの補助関数が完成したら、main() 関数の中で補助関数を順番に呼び出して、実際に画像を作成・表示しています。

以下、プログラムの構成通り、補助関数の実装から詳しく見ていきたいと思います。

## 画像イメージの作成
GIMP で画像を作成する際は、まず画像データを作成します。

画像データはレイヤーの入れ物です。
図形などの画像は画像データに直接格納されるのではなく、その中のレイヤーに格納されます。
画像データを保存すると画像ファイルになります。

画像データの作成には幅、高さ、画像タイプなどの設定情報が必要となります。
幅と高さはピクセル単位で指定します。
画像タイプは RGB, GRAY, INDEXED などを指定できます。

画像データは Python-Fu の gimp.Image() 関数で作成します。
スクリプト冒頭の以下の部分が画像データを作成する関数です。

```` python
# 画像データの作成
## 指定したサイズで画像データを作成する
### width : 画像データの幅 (px)
### height : 画像データの高さ (px)
def create_image(width, height):
  # 画像データを生成
  return gimp.Image(width, height, RGB)
````

create_image 関数は以下のように呼び出します。

```` python
image = create_image(640, 400)
````

これを実行すると、幅 640 ピクセル、高さ 400 ピクセル、RGB カラーの画像データが作成されます。

## レイヤーの追加
次に、画像データにレイヤーを追加します。
画像はレイヤーに描き込まれますので、最低でも一つのレイヤーが必要です。

レイヤーを作成する Python-Fu の関数は gimp.Layer() です。
gimp.Layer() の引数には、画像データ、レイヤー名、レイヤーの幅、高さ、画像タイプ、不透明度、モードを渡します。

レイヤーを作成したら、背景色で塗りつぶします。
これは GIMP アプリの GUI からレイヤーを作成するときの挙動に合わせました。
GIMP でレイヤーを追加するとデフォルトで背景色で塗りつぶすような動きになっています。

続いて、gimp.Image.add_layer() 関数を使ってレイヤーを画像データに紐付けします。
引数の position は上から何番目の位置にレイヤーを追加するかを指定するパラメータです。

レイヤーを追加する関数の実装は以下の通りです。

```` python
# レイヤーの追加
## 指定した名前のレイヤーを新規に作成し、画像データに挿入する
### image : レイヤーを追加する画像データ
### name : 新規に作成するレイヤーの名前（文字列）
def add_layer(image, name):
  # レイヤーの作成に必要なパラメータ
  width   = image.width
  height  = image.height
  type    = RGB_IMAGE
  opacity = 100
  mode    = NORMAL_MODE
  
  # パラメータをもとにレイヤーを作成
  layer = gimp.Layer(image, name, width, height, type, opacity, mode)
  
  # レイヤーを背景色で塗りつぶす（GIMP のデフォルトの挙動に合わせています）
  layer.fill(1)
  
  # 画像データの 0 番目の位置にレイヤーを挿入する
  position = 0
  image.add_layer(layer, position)
  
  return layer
````

add_layer() 関数は main() 関数の中で以下のように呼び出されています。

```` python
layer = add_layer(image, "背景")
````

これが実行されると、「背景」という名前のレイヤーが作成され、画像データに追加されます。

## 線を描く
レイヤーを作成しましたので、絵を描き始める準備が整いました。
画像処理の基本として、まず最初に線を描く方法を用意します。

Python-Fu で画像を加工する際は、GIMP のアプリで絵を描く時と同じように GIMP 内のペンやブラシなどのツールを使用します。
ここではペンシルツールを使って線を描く関数を定義します。

Python-Fu に用意されている pdb.gimp_pencil() 関数を使用するとペンシルツールで線を引くことができます。
pdb.gimp_pencil() 関数の引数は、レイヤーなどの描画領域、線が経由する座標の数、線が経由する座標を格納した配列です。

わざわざ座標の数を引数で渡しているのは、この gimp_pencil() が C の関数のラッパーになっているからだと思われます。
C では配列の要素数を調べる方法がないので、明示的に関数に教えてあげる必要があります。

```` python
# ペンシルツールで線を描く
## 配列に格納した座標列を結ぶ線を描画領域にペンシルツールで描く
### drawable : 描画領域（レイヤーなど）
### lines : 描画される線の座標列を格納した配列
def draw_pencil_lines(drawable, lines):
  # ペンシルツールで線を描画する
  pdb.gimp_pencil(drawable, len(lines), lines)
````

draw_pencil_lines() 関数は次の draw_rect() 関数で呼び出されます。

## 矩形を描く
続いて、矩形、つまり四角形を描く関数を用意します。
矩形の描画は Python-Fu の関数ではなく、先ほど作成した draw_pencil_lines() 関数を使用します。

以下のコードでは、線を描く draw_pencil_lines() 関数に四角形の四辺をなぞる配列を渡して矩形を描かせています。

```` python
# ペンシルツールで矩形を描く
## 左上、右下座標をもとに描画領域に矩形を描く
### drawable : 描画領域（レイヤーなど）
### x1 : 左上の X 座標
### y1 : 左上の Y 座標
### x2 : 右下の X 座標
### y2 : 右下の Y 座標
def draw_rect(drawable, x1, y1, x2, y2):
  lines = [x1, y1, x2, y1, x2, y2, x1, y2, x1, y1]
  draw_pencil_lines(drawable, lines)
````

draw_rect() 関数は以下のように呼び出されています。

```` python
draw_rect(layer, 390, 210, 490, 310)
````

これを実行すると、デフォルトの色、デフォルトの線幅を使って矩形が描画されます。
描画する際の色や線幅を変更する方法は後ほど説明します。

## エアブラシツールで線を描く
ペンシルツールの代わりにエアブラシを使って線を描く関数も用意します。
エアブラシは pdb.gimp_airbrush() 関数で利用できます。
pdb.gimp_airbrush() の引数は pdb.gimp_pencil() とほぼ同じですが、筆圧を指定するパラメータが追加されています。

```` python
# エアブラシで線を描く
## 配列に格納した座標列を結ぶ線を描画領域にエアブラシで描く
### drawable : 描画領域（レイヤーなど）
### pressure : 筆圧 (0-100)
### lines : 描画される線の座標列を格納した配列
def draw_airbrush_lines(drawable, pressure, lines):
  # エアブラシで線を描画する
  pdb.gimp_airbrush(drawable, pressure, len(lines), lines)
````

draw_airbrush_lines() 関数は main() 関数の中で以下のように呼び出されています。
まず描きたい線のパスを配列にまとめ、それを引数にして関数を呼び出しています。
筆圧は 75 を指定しています。

```` python
lines = [110,90, 120,180, 130,110, 140,150]
draw_airbrush_lines(layer, 75, lines)
````

## 日本語の文字列を描画する
画像の中に文字でメッセージを入れたい時は、pdb.gimp_text_fontname() 関数を使用します。
描画したい文字列の他にフォントサイズやアンチエイリアス処理を行うかなどのパラメータを指定します。
draw_text() 関数は pdb.gimp_text_fontname() をラップした関数で、必要最低限の情報を与えるだけで文字列を描画できるようにしてあります。

```` python
# 文字列を描画する
## 指定した描画領域に文字列を描画します
### drawable : 描画領域（レイヤーなど）
### x : 文字列を描画する位置の X 座標
### y : 文字列を描画する位置の Y 座標
### size : フォントサイズ
### str : 描画する文字列
def draw_text(drawable, x, y, size, str):
  image = drawable.image
  border = -1
  antialias = True
  size_type = PIXELS
  fontname = '*'
  floating_sel = pdb.gimp_text_fontname(image, drawable, x, y, str, border,
                 antialias, size, size_type, fontname)
  pdb.gimp_floating_sel_anchor(floating_sel)
````

draw_text() 関数の呼び出し方は以下の通りです。
描画領域、文字を書く位置の X 座標、Y 座標、フォントサイズ、描画したい文字列を引数に渡して実行しています。

```` python
draw_text(layer, 200, 180, 20, "こんにちは")
````

## 色を変更する
図形や文字列を描画する際の色は GIMP のカラーパレットで前景色に設定されているものが使用されます。
カラーパレットの前景色を設定する関数は pdb.gimp_context_set_foreground() で、色データは R, G, B, A のタプルで表現されています。

ここでは分かりやすいように set_color という別名を付け、RGBA の各要素を別々に引数で渡すようにしています。

```` python
# 描画する色を変更する
## パレットの前景色を変更して描画色を設定する
### r : 赤要素 (0-255)
### g : 緑要素 (0-255)
### b : 青要素 (0-255)
### a : 透明度 (0-1.0)
def set_color(r, g, b, a):
  color = (r, g, b, a)
  pdb.gimp_context_set_foreground(color)
````

main() 関数の中ではこの関数を使って赤色の設定をしています。

```` python
set_color(255,0,0,1.0)  # Red
````

## 線の太さを変更する
ペンシルツールやエアブラシの太さを指定する関数は pdb.gimp_context_set_bursh_size() 関数です。
以下のコードでは、機能が分かりやすいように set_line_width() という別名を付けています。

```` python
# 描画する線の太さを変える
## ブラシのサイズを変更して線の太さを設定する
### width : 線の太さ
def set_line_width(width):
  pdb.gimp_context_set_brush_size(width)
````

1 ピクセル幅の線を引きたい場合はこのように引数に 1 を指定します。

```` python
set_line_width(1)
````

## 画像の表示
画像の加工が完了したら、画像データをデスクトップに表示します。
gimp.Display() 関数の引数に画像データを指定して実行すると、新しいウィンドウが作成され、画像が表示されます。

先ほどと同じように、ここでも分かりやすい別名をつけています。

```` python
# 画像の表示
## 新しいウィンドウを作成し、画像データを表示する
### image : 表示する画像データ
def display_image(image):
  gimp.Display(image)
````

display_image() 関数の呼び出し方は以下の通りです。

```` python
display_image(image)
````

## main() 関数
以下が main() 関数です。
これまで定義してきた関数の呼び出しを一箇所にまとめています。

Python の場合は main() 関数がプログラムのエントリーポイントと決められてはいませんので、単に一般的な慣習に従って main という名前をつけています。

```` python
def main():
  image = create_image(640, 400)
  layer = add_layer(image, "背景")
  draw_rect(layer, 390, 210, 490, 310)
  draw_text(layer, 200, 180, 20, "こんにちは")
  lines = [110,90, 120,180, 130,110, 140,150]
  draw_airbrush_lines(layer, 75, lines)
  set_color(255,0,0,1.0)  # Red
  set_line_width(1)
  draw_rect(layer, 420, 240, 520, 340)
  display_image(image)

main()
````

以上でプログラムの解説は終了です。
ブラシやパレットなど、GIMP のアプリの仕組みを使う点が一般的な画像処理ライブラリとの大きな違いでした。
何らかのお絵かきツールを使ったことがある人でしたら難しいところはないのではないかと思います。

# ここからどうするか
まずは上記のプログラムを改造して、色や線幅を変えてみたり、図形の形を変えてみたり、エアブラシツールの筆圧を変えてみて、どう動きが変わるのかを見てみてください。

そのあとは API リファレンスなどをご覧いただいてもっと面白いコードをたくさん作っていただければと思います。
また Python の help() や dir() なども役に立つことがあるかもしれません。

今回は説明しませんでしたが、作成したスクリプトをプラグインとして GIMP に組み込むこともできます。
ある程度スクリプトの作成に慣れたら是非試してみてください。

## リファレンス

- [API リファレンス](http://developer.gimp.org/api/2.0/)
 - http://developer.gimp.org/api/2.0/

- [GIMP Python Documentation](https://www.gimp.org/docs/python/)
 - https://www.gimp.org/docs/python/

- [Writing GIMP Scripts and Plug-Ins](http://gimpbook.com/scripting/)
 - http://gimpbook.com/scripting/

- プロシージャーブラウザ（pdb のリファレンス）
 - メニューバー >> ヘルプ >> プロシージャーブラウザを選択すると起動します

## help() と dir()
Python に組み込みの help() や dir() を使うと Python オブジェクトの詳細を確認することができます。
以下に使用例をご紹介します。

help() 関数を使用すると、Python オブジェクトのヘルプを見ることができます。

```` python
>>> help(gimp)
Help on module gimp:

NAME
    gimp - This module provides interfaces to allow you to write gimp plugins

FILE
    /Users/.../Applications/GIMP/GIMP.app/Contents/Resources/lib/gimp/2.0/python/gimp.so

CLASSES
    __builtin__.object
        Display
        Image
        Item
            Drawable
                Channel
                Layer
                    GroupLayer
            Vectors
        Parasite
        PixelFetcher
        PixelRgn
        Tile
    exceptions.RuntimeError(exceptions.StandardError)
        error
    VectorsStroke(__builtin__.object)
        VectorsBezierStroke
...
````

dir() 関数を使用すると、Python オブジェクトのメンバーを確認することができます。

```` python
>>> for i in dir(gimp.Layer):
...   print i
... 
ID
__class__
__cmp__
__delattr__
__doc__
__format__
__getattribute__
__hash__
__init__
__new__
__reduce__
__reduce_ex__
__repr__
__setattr__
__sizeof__
__str__
__subclasshook__
add_alpha
add_mask
apply_mask
attach_new_parasite
bpp
children
copy
create_mask
edit_mask
fill
...
````

# まとめ
以上、GIMP 拡張用のスクリプト・インターフェイスの Python-Fu を使い始める手順を解説しました。
お役に立ちましたら幸いです。

__おしまい__
