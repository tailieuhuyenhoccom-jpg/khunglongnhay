from PIL import Image

def remove_background_near_color(image_path, output_path, bg_color=(252, 233, 244), tolerance=40):
    image = Image.open(image_path).convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        r, g, b, a = item
        dr = abs(r - bg_color[0])
        dg = abs(g - bg_color[1])
        db = abs(b - bg_color[2])
        if dr <= tolerance and dg <= tolerance and db <= tolerance:
            newData.append((r, g, b, 0))  # Làm trong suốt
        else:
            newData.append(item)

    image.putdata(newData)
    image.save(output_path, "PNG")
    print(f'✅ Đã xử lý và lưu: {output_path}')