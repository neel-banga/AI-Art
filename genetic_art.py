def save_image(data, path):
    image = Image.fromarray(data)
    image.save(path)