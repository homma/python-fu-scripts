
# サンプルスクリプト

## 新しい画像を作成する

````
# 画像の作成
i_width = 256
i_height = 128
i_type = RGB
image = gimp.Image(i_width, i_height, i_type)

# レイヤーの作成
# image = gimp.image_list()[0]
l_name = ""
l_width = image.width
l_height = image.height
l_type = RGB_IMAGE
l_opacity = 100
l_mode = NORMAL_MODE
layer = gimp.Layer(image, l_name, l_width, l_height, l_type, l_opacity, l_mode)

# レイヤーの追加
l_position = 0
image.add_layer(layer, l_position)

# 画像の表示
gimp.Display(image)
````

## 新しい画像を作成する (pdb を使用する場合)
- pdb.gimp_image_new() で新しい画像を作成します
- pdb.gimp_layer_new() で新しいレイヤーを作成します
- pdb.gimp_image_add_layer() で画像にレイヤーを関連付けます
- pdb.gimp_display_new() で新しいウィンドウを開いて画像を表示します

````
# 画像の作成
i_width = 256
i_height = 128
i_type = 0
image = pdb.gimp_image_new(i_width, i_height, i_type)

# レイヤーの作成
# image = gimp.image_list()[0]
l_width = image.width
l_height = image.height
l_type = RGB_IMAGE
l_name = ""
l_opacity = 100
l_mode = NORMAL_MODE
layer = pdb.gimp_layer_new(image, l_width, l_height, l_type,
  l_name, l_opacity, l_mode)

# レイヤーの追加
l_position = 0
pdb.gimp_image_add_layer(image, layer, l_position)

# 画像の表示
pdb.gimp_display_new(image)
````

## ファイルから画像を読み込む

## 画像に線を引く
- pdb.gimp_pencil() で線を引きます

````
# 画像を取得
image = gimp.image_list()[0]

# アクティブなレイヤーを取得
layer = image.active_layer

# 線を引く
pdb.gimp_pencil(layer, 2, [10,10, 20,20])

````

## 画像を前景色で塗りつぶす
- gimp.image_list() で画像のリストを取得します
- gimp.Image.active_layer 変数に格納されているアクティブなレイヤーを取得します
- gimp.Layer.fill() でレイヤーを塗りつぶします

- gimp.Layer.fill() で塗りつぶすと Undo できないようです
- Undo が可能なようにしたい場合は、代わりに pdb.gimp_edit_fill() を使用します

````
# 画像を取得
image = gimp.image_list()[0]

# アクティブなレイヤーを取得
layer = image.active_layer

# 前景色 (0) で塗りつぶす (Undo 不可)
layer.fill(0)

# 前景色 (0) で塗りつぶす (Undo 可能)
# pdb.gimp_edit_fill(layer, 0)
````
