# Quarter View の 2D Pixel Image を作成する際のガイド線を引くスクリプト

config = {
  'width': 80,
  'height': 80,
  'box_width': 32,
  'box_height': 16,
  'guideline_color': (200,200,200,1.0),
  'guideline_width': 1,
  'white': (255,255,255,1.0),
  'black': (0,0,0,1.0),
  'transparent': (255,255,255,0.0),
  'pencil': 'gimp-pencil'
}

# メイン処理
def main():
  width = config['width']
  height = config['height']
  
  image = create_image(width, height)
  layer = add_layer(image, "ガイド線")
  draw_guide_line(layer, width, height)
  add_layer(image, "メイン")
  display_image(image)
  initialize()

# ツールや画面の初期設定
def initialize():
  # 描画色を黒にする
  set_color(config['black'])
  set_line_width(1)

### Quarter View に関するルーティン ###

# Quarter View のガイドラインの描画
def draw_guide_line(layer, width, height):
  set_color(config['white'])
  layer.fill(FOREGROUND_FILL)
  
  set_color(config['guideline_color'])
  set_line_width(config['guideline_width'])
  
  box_w = config['box_width']
  box_h = config['box_height']
  
  for x in range(width / box_w + 1):
    for y in range(height / box_h + 1):
      draw_rhombus(layer, x * box_w, y * box_h, box_w, box_h)

# Quarter View のガイドラインとなる菱形の描画
def draw_rhombus(layer, x, y, w, h):
  points = [[x, y + h/2], [x + w/2, y], [x + w, y + h/2], [x + w/2, y + h]]
  lines = [
           [points[0][0], points[0][1], points[1][0], points[1][1]],
           [points[1][0], points[1][1], points[2][0], points[2][1]],
           [points[2][0], points[2][1], points[3][0], points[3][1]],
           [points[3][0], points[3][1], points[0][0], points[0][1]]
          ]
  for i in range(len(lines)):
    draw_pencil_line(layer, lines[i])

# 画像データの作成
## 指定したサイズで画像データを作成する
### width : 画像データの幅 (px)
### height : 画像データの高さ (px)
def create_image(width, height):
  # 画像データを生成
  return gimp.Image(width, height, RGB)

### GIMP 関連のプリミティブなルーティン ###

# レイヤーの追加
## 指定した名前で、透明のレイヤーを新規に作成し、画像データに挿入する
### image : レイヤーを追加する画像データ
### name : 新規に作成するレイヤーの名前（文字列）
def add_layer(image, name):
  # レイヤーの作成に必要なパラメータ
  width   = image.width
  height  = image.height
  type    = RGBA_IMAGE
  opacity = 100
  mode    = NORMAL_MODE
  
  # パラメータをもとにレイヤーを作成
  layer = gimp.Layer(image, name, width, height, type, opacity, mode)
  
  # 画像データの 0 番目の位置にレイヤーを挿入する
  position = 0
  image.add_layer(layer, position)
  
  return layer

# ペンシルツールで線を描く
## 配列に格納した座標列を結ぶ線を描画領域にペンシルツールで描く
### drawable : 描画領域（レイヤーなど）
### lines : 描画される線の座標列を格納した配列
def draw_pencil_line(drawable, points):
  # ペンシルツールで線を描画する
  pdb.gimp_pencil(drawable, len(points), points)

# 描画ツールを変更する
## 描画ツールを変更する
### method : 変更先の描画ツール名
def set_paint_method(method):
  pdb.gimp_context_set_paint_method(method)

# 描画する色を変更する
## パレットの前景色を変更して描画色を設定する
### color : (r, g, b, a)
### r : 赤要素 (0-255)
### g : 緑要素 (0-255)
### b : 青要素 (0-255)
### a : 透明度 (0-1.0)
def set_color(color):
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

main()

