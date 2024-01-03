import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from ..file import is_file_in_directory, is_file_with_name_in_directory


class settingsPlugCover:
    "插件封面配置"

    def __init__(
        self,
        input_image_path,
        output_image_path,
        title,
        text,
        title_font_path,
        text_font_path,
        title_font_size,
        text_font_size,
        title_color,
        text_color,
        text_spacing,
        title_spacing,
        title_x,
        title_y,
        text_x,
        text_y,
        align,
    ):
        self.input_image_path = input_image_path
        self.output_image_path = output_image_path
        self.title = title
        self.text = text
        self.title_font_path = title_font_path
        self.text_font_path = text_font_path
        self.title_font_size = title_font_size
        self.text_font_size = text_font_size
        self.title_color = title_color
        self.text_color = text_color
        self.text_spacing = text_spacing
        self.title_spacing = title_spacing
        self.title_x = title_x
        self.title_y = title_y
        self.text_x = text_x
        self.text_y = text_y
        self.align = align


def settings_plug_cover(settings):
    "设置生成插件封面"
    # 打开原始图片
    img = Image.open(settings.input_image_path)

    # 创建绘图对象
    draw = ImageDraw.Draw(img)

    # 添加标题
    title_font = ImageFont.truetype(settings.title_font_path, settings.title_font_size)
    title_text_color = settings.title_color

    # 添加标题
    draw.text(
        (settings.title_x, settings.title_y),
        settings.title,
        fill=title_text_color,
        font=title_font,
        align=settings.align,
    )

    # 添加描述
    text_font = ImageFont.truetype(settings.text_font_path, settings.text_font_size)
    text_text_color = settings.text_color

    # 添加文字
    draw.text(
        (settings.text_x, settings.text_y),
        settings.text,
        fill=text_text_color,
        font=text_font,
        align=settings.align,
    )

    # 保存处理后的图片
    img.save(settings.output_image_path)


def plug_cover(
    script_dir="",
    file_name="cover",
    title_name="title",
    text_name="text",
    title_font_size=65,
    text_font_size=45,
    title_color=(0, 0, 0),
    text_color=(111, 111, 111),
    title_x=350,
    title_y=30,
    text_x=350,
    text_y=180,
    align="left",
    rmtree=False,
):
    "生成插件封面"

    input_image_path = os.path.join(script_dir, "static")
    output_image_path = os.path.join("cover")

    if not is_file_with_name_in_directory(
        os.path.join(input_image_path, "font"), "title"
    ):
        print(f"执行前需在 {input_image_path}/font 中放入名为 title 的字体文件")
        return
    if not is_file_with_name_in_directory(
        os.path.join(input_image_path, "font"), "text"
    ):
        print(f"执行前需在 {input_image_path}/font 中放入名为 text 的字体文件")
        return
    if not is_file_in_directory(
        os.path.join(input_image_path, "image"), "cover_background.png"
    ):
        print(f"执行前需在 {input_image_path}/image 中放入名为 cover_background.png 的字体文件")
        return

    if not os.path.exists(input_image_path):
        os.makedirs(input_image_path)

    if os.path.exists(output_image_path) and rmtree:
        shutil.rmtree(output_image_path)
    if not os.path.exists(output_image_path):
        os.makedirs(output_image_path)

    settings = settingsPlugCover(
        input_image_path=os.path.join(
            input_image_path, "image", "cover_background.png"
        ),
        output_image_path=os.path.join(output_image_path, file_name + ".png"),
        title=title_name,
        text=text_name,
        title_font_path=os.path.join(script_dir, "static", "font", "title.ttf"),
        text_font_path=os.path.join(script_dir, "static", "font", "text.ttf"),
        title_font_size=title_font_size,
        text_font_size=text_font_size,
        title_color=title_color,
        text_color=text_color,
        text_spacing=30,
        title_spacing=-15,
        title_x=title_x,
        title_y=title_y,
        text_x=text_x,
        text_y=text_y,
        align=align,
    )

    # 调用函数并传递参数对象
    settings_plug_cover(settings)
    print(f"图片 {title_name} 处理完成")


class settingsPlugCoverCenter:
    "插件封面配置"

    def __init__(
        self,
        input_image_path,
        output_image_path,
        title,
        text,
        title_font_path,
        text_font_path,
        title_font_size,
        text_font_size,
        title_color,
        text_color,
        text_spacing,
        title_spacing,
    ):
        self.input_image_path = input_image_path
        self.output_image_path = output_image_path
        self.title = title
        self.text = text
        self.title_font_path = title_font_path
        self.text_font_path = text_font_path
        self.title_font_size = title_font_size
        self.text_font_size = text_font_size
        self.title_color = title_color
        self.text_color = text_color
        self.text_spacing = text_spacing
        self.title_spacing = title_spacing


def settings_plug_cover_center(settings):
    "生成插件封面"
    # 打开原始图片
    img = Image.open(settings.input_image_path)

    # 创建绘图对象
    draw = ImageDraw.Draw(img)

    # 添加标题
    title_font = ImageFont.truetype(settings.title_font_path, settings.title_font_size)
    title_text_color = settings.title_color

    # 获取标题文本尺寸
    title_bbox = draw.textbbox((0, 0), settings.title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    # 计算标题位置使其居中
    image_width, image_height = img.size
    x = (image_width - title_width) / 2
    y = (image_height - title_height) / 2 + settings.title_spacing  # 使用设置的标题偏移值

    # 添加标题水印
    draw.text(
        (x, y), settings.title, fill=title_text_color, font=title_font, align="center"
    )

    # 添加版本号
    text_font = ImageFont.truetype(settings.text_font_path, settings.text_font_size)
    text_text_color = settings.text_color

    # 获取版本号文本尺寸
    text_bbox = draw.textbbox((0, 0), settings.text, font=text_font)
    text_width = text_bbox[2] - text_bbox[0]

    # 计算版本号位置
    text_x = (image_width - text_width) / 2
    text_y = y + title_height + settings.text_spacing  # 使用设置的文本偏移值

    # 添加版本号水印
    draw.text(
        (text_x, text_y),
        settings.text,
        fill=text_text_color,
        font=text_font,
        align="center",
    )

    # 保存处理后的图片
    img.save(settings.output_image_path)


def plug_cover_center(
    script_dir="",
    file_name="cover",
    title_name="title",
    text_name="text",
    title_font_size=65,
    text_font_size=45,
    title_color=(0, 0, 0),
    text_color=(111, 111, 111),
    rmtree=False,
):
    "生成插件封面"

    input_image_path = os.path.join(script_dir, "static")
    output_image_path = os.path.join("cover")

    if not is_file_with_name_in_directory(
        os.path.join(input_image_path, "font"), "title"
    ):
        print(f"执行前需在 {input_image_path}/font 中放入名为 title 的字体文件")
        return
    if not is_file_with_name_in_directory(
        os.path.join(input_image_path, "font"), "text"
    ):
        print(f"执行前需在 {input_image_path}/font 中放入名为 text 的字体文件")
        return
    if not is_file_in_directory(
        os.path.join(input_image_path, "image"), "cover_background.png"
    ):
        print(f"执行前需在 {input_image_path}/image 中放入名为 cover_background.png 的字体文件")
        return

    if not os.path.exists(input_image_path):
        os.makedirs(input_image_path)

    if os.path.exists(output_image_path) and rmtree:
        shutil.rmtree(output_image_path)
    if not os.path.exists(output_image_path):
        os.makedirs(output_image_path)

    settings = settingsPlugCoverCenter(
        input_image_path=os.path.join(
            input_image_path, "image", "cover_background.png"
        ),
        output_image_path=os.path.join(output_image_path, file_name + ".png"),
        title=title_name,
        text=text_name,
        title_font_path=os.path.join(script_dir, "static", "font", "title.ttf"),
        text_font_path=os.path.join(script_dir, "static", "font", "text.ttf"),
        title_font_size=title_font_size,
        text_font_size=text_font_size,
        title_color=title_color,
        text_color=text_color,
        text_spacing=30,
        title_spacing=-15,
    )

    # 调用函数并传递参数对象
    settings_plug_cover_center(settings)
    print(f"图片 {title_name} 处理完成")


if __name__ == "__main__":
    plug_cover()
