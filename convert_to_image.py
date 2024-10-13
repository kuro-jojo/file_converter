def convert_to_image(
    file_type: str, output_type: str, file_path: str, output_file: str
) -> int:
    import os

    if not os.path.exists(file_path):
        print(f"{file_path} not found")
        return -1

    file_name = (
        file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
    )
    output_path = file_path.removesuffix(file_name)
    file_extension = file_name.split(".")[-1]

    if not output_file:
        output_file = file_name.removesuffix(file_extension) + output_type

    if not output_file.endswith(output_type):
        output_file = output_file + "." + output_type

    output_file = output_path + output_file

    match file_type:
        case "png" | "jpg" | "jpeg" | "gif":
            if file_extension == output_type:
                print("The converted type must be different from the original type")
                return -1
            return from_image(file_path, output_file)
        case "pdf":
            return from_pdf(
                file_path, output_path, file_name.removesuffix(".pdf"), output_type
            )

    return -1


def from_image(image_file: str, output_file: str) -> int:
    from PIL import Image

    image_extensions = ["png", "jpg", "jpeg", "gif"]

    if image_file.split(".")[-1] not in image_extensions:
        print("Image file must be one of the following types: ", image_extensions)
        return -1

    try:
        with Image.open(image_file) as im:
            image = im.convert("RGB")
            image.save(output_file)
    except FileNotFoundError:
        print("Image file not found")
        return -1

    return 0


def from_pdf(
    pdf_file: str, output_path: str, file_name_without_ext: str, output_type: str
) -> int:
    from pdf2image import convert_from_path
    from PIL import Image

    images = convert_from_path(pdf_file)
    if not images:
        print("No images created")
        return -1

    try:
        if len(images) == 1:
            images[0].save(f"{output_path}{file_name_without_ext}.{output_type}")
        else:
            for i, image in enumerate(images):
                image.save(f"{output_path}{file_name_without_ext}_{i+1}.{output_type}")
    except FileNotFoundError:
        print("Image file not found")
        return -1

    return 0
