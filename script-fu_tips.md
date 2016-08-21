# はじめに
- GIMP の Python-Fu の Tips をまとめます
- 間違っていたらごめんなさい

# 参考資料
- https://www.gimp.org/docs/python/
- http://gimpbook.com/scripting/

# プロシージャブラウザ（pdb のリファレンス）
- ヘルプ >> プロシージャーブラウザ

- プロシージャブラウザの中身はウェブで公開されていないみたい
- pdb 以外の関数については調べられないみたい

# Python-Fu を使用する準備

## コンソールの起動
- メニュー >> フィルター >> Python-Fu >> コンソール

# Python の Tips

## 存在しているメソッドや変数を調べる
- dir(gimp)
- dir(pdb)

# GIMP API の Tips

## pdb について
- Python から GIMP を操作する際に、pdb の関数を使う方法とオブジェクト指向的な方法の二種類があります

- pdb は GIMP に昔から付属していた Scheme の関数をそのまま Python から呼び出せるようにした感じです
- pdb を使用するメリットは
 - プロシージャブラウザで詳細説明が見られる
 - Undo / Redo に対応している

- オブジェクト指向的な方は、pdb を Python のオブジェクトでラップしたもののようです
- pdb よりも簡潔なコードを書くことができます
- リファレンスやヘルプが用意されていないので、引数に何を渡すべきか調べながら使う必要があります
- Undo / Redo に対応していないようです

## 画像

### 画像の一覧を取得する
````
images = gimp.image_list()
````

### 画像を作成する

#### gimp.Image()
````
width = 256
height = 128
type = RGB
image = gimp.Image(width, height, type)
````

#### pdb.gimp_image_new()
````
width = 256
height = 128
type = 0
image = pdb.gimp_image_new(width, height, type)
````

## レイヤー

### レイヤーを作成する

#### gimp.Layer()

````
image = gimp.image_list()[0]
name = ""
width = image.width
height = image.height
type = RGB_IMAGE
opacity = 100
mode = NORMAL_MODE
layer = gimp.Layer(image, name, width, height, type, opacity, mode)

# レイヤーの追加
l_position = 0
image.add_layer(layer, l_position)
````

#### pdb.gimp_layer_new()
````
image = gimp.image_list()[0]
width = image.width
height = image.height
type = RGB_IMAGE
name = ""
opacity = 100
mode = NORMAL_MODE
layer = pdb.gimp_layer_new(image, width, height, type, name, opacity, mode)

レイヤーの追加
layer_position = 0
pdb.gimp_image_add_layer(image, layer, layer_position)
````

#### gimp.Image.new_layer()
- 画像オブジェクトのメソッドでレイヤーを作成する
- オプションは不明

````
image.new_layer(...)
````

### 画像を表示する

#### gimp.Display()
````
gimp.Display(image)
````
#### pdb.gimp_display_new()
````
pdb.gimp_display_new(image)
````

## 色

### 前景色、背景色に設定されている色を取得する
- gimp.get_foreground() で前景色を確認します
- gimp.get_background() で背景色を確認します

````
fore_color = gimp.get_foreground()
print fore_color
# => RGB (1.0, 0.0, 0.0, 1.0)
````

### 使用する色を設定する : gimp_palette_set_XX
- pdb.gimp_palette_set_foreground() で前景色を設定します
- pdb.gimp_palette_set_background() で背景色を設定します

````
def set_color(r, g, b, a):
  color = (r, g, b, a)
  pdb.gimp_palette_set_foreground(color)

set_color(0,0,0,1.0)
````

## 画像の編集

### 線を引く
-　pdb.gimp_pencil() で線を引きます
- 汎用グラフィックライブラリではなく GIMP を操作するライブラリなので、draw_line() 的な関数は用意されていないようです

### 塗りつぶす

#### gimp.Layer.fill()
- 前景色で塗りつぶす場合は引数を 0 に、背景色で塗りつぶす場合は 1 にします

````
layer.fill(0)
````

#### gimp_edit_fill
- pdb.gimp_edit_fill() で指定したレイヤーを塗りつぶします
- 前景色で塗りつぶす場合は第二引数を 0 に、背景色で塗りつぶす場合は 1 にします

````
pdb.gimp_edit_fill(layer, 0)
````

### フォントの一覧を調べる

````python
def list_fonts():
  pdb.gimp_fonts_get_list("")

list_fonts()
````
