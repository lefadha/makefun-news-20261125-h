from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
im = Image.open('entry.png').convert('RGB')
for tag, pic in (('300', im.resize((300,300), Image.LANCZOS).resize((1024,1024), Image.LANCZOS)),
                 ('full', im)):
    res, _ = ocr(pic)
    print('==', tag, len(res or []))
    for r in (res or []):
        print('  %.2f  %s' % (r[2], r[1][:72]))
