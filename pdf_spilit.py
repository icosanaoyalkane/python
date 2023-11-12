# PRG1：ライブラリ設定
import fitz
import os

# PRG2：画像の保存先フォルダを設定
filename = r"C:\Users\1002789-Z100.GLOBAL\Desktop\NG23040006.pdf"
dir_name = filename.split('.pdf')[0]
print(dir_name)
img_dir = os.path.join(os.getcwd(),dir_name) 
print(img_dir)

if os.path.isdir(img_dir) == False:
    os.mkdir(img_dir)
    print("mkdir")

print("PRG2 is done")

# PRG3：PDFファイルを読み込む
doc = fitz.open(filename)

print("PRG3 is done")
# PRG4：画像情報を格納するリストを作成
images = []
print("PRG4 is done")
# PRG5：１ページずつ画像データを取得
for page in range(len(doc)):
    images.append(doc[page].get_images())
print("PRG5 is done")
# PRG6：ページ内の画像情報を順番に処理
for pageNo, image in enumerate(images):
    # PRG7：ページ内の画像情報を処理する
    if image != []:
        for i in range(len(image)):
            # PRG8：画像情報の取得
            xref = image[i][0]
            smask = image[i][1]
            if image[i][8] == 'FlateDecode':
                ext = 'png'
            elif image[i][8] == 'DCTDecode':
                ext = 'jpeg'

            # PRG9：マスク情報の取得と画像の再構築
            pix = fitz.Pixmap(doc.extract_image(xref)["image"])
            if smask > 0:
                mask = fitz.Pixmap(doc.extract_image(smask)["image"])
                pix = fitz.Pixmap(pix, 0) 
                pix = fitz.Pixmap(pix, mask)

            # PRG10：画像を保存
            img_name = os.path.join(img_dir, f'image{pageNo+1}_{i}.{ext}')
            pix.save(img_name)

print("All done")
