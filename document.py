# -*- coding: utf-8 -*-
# @Author: Xia Yunkai
# @Date:   2024-08-17 21:26:21
# @Last Modified by:   Xia Yunkai
# @Last Modified time: 2024-08-22 19:57:22


from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import (
    Table,
    SimpleDocTemplate, 
    Paragraph, 
    Image, 
    Spacer,
    PageBreak)

from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm ,inch 
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import PCMYKColor
import copy

import random
def random_cmyk_color():
    """生成随机的CMYK颜色"""
    c = round(random.uniform(0, 100))  # 青色(Cyan)随机值
    m = round(random.uniform(0, 100))  # 洋红(Magenta)随机值
    y = round(random.uniform(0, 100))  # 黄色(Yellow)随机值
    k = round(random.uniform(0, 50))  # 黑色(Black)随机值
    return PCMYKColor(c, m, y, k)

class Empty(object):
    pass

def dummy_stationery(c, doc):
    pass

class Document:
    # 构造函数
    def __init__(self, filename: str):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=letter)
        self.story = []
        self.fontName = "SimSun"
        self.fontSize = 9
        self.headerImagePath = None
        
        
    
    # 结束添加内容并创建报告
    def end_content(self):
        self.doc.build(self.story,onFirstPage=self.header_and_footer, onLaterPages=self.header_and_footer)
    
    # 注册字体
    def register_fonts(self,font_size:float, font_name:str,font_path:str):
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        self.fontName = font_name
        self.fontSize = font_size
        self.generate_style()

# 下一页
    def add_page_brake(self):
        self.append(PageBreak())

    def set_header_image(self,path:str, width:float, height:float):
        self.headerImagePath = path
        self.headerImageWidth = width
        self.headerImageHeight = height
        
    # 生成style
    def generate_style(self):
        self.style = Empty()
        self.style.fontName = self.fontName
        self.style.fontSize = self.fontSize
        _styles = getSampleStyleSheet()
        self.style.normal = _styles["Normal"]
        self.style.normal.fontName = "%s" % self.style.fontName
        self.style.normal.fontSize = self.style.fontSize
        self.style.normal.firstLineIndent = 0

        self.style.heading1 = copy.deepcopy(self.style.normal)
        self.style.heading1.fontName = "%s" % self.style.fontName
        self.style.heading1.fontSize = 1.5 * self.style.fontSize
        self.style.heading1.leading = 2 * self.style.fontSize
        self.style.heading1.alignment = 1    # 居中
        self.style.heading1.bold = True

        self.style.heading2 = copy.deepcopy(self.style.normal)
        self.style.heading2.fontName = "%s" %self.style.fontName
        self.style.heading2.fontSize = 1.25 * self.style.fontSize
        self.style.heading2.leading = 1.75 * self.style.fontSize
        self.style.heading2.bold = True
        self.style.heading2.alignment = 0

        self.style.heading3 = copy.deepcopy(self.style.normal)
        self.style.heading3.fontName = "%s" % self.style.fontName
        self.style.heading3.fontSize = 1.1 * self.style.fontSize
        self.style.heading3.leading = 1.5 * self.style.fontSize
        self.style.heading3.textColor = "#666666"
        self.style.heading3.bold = True
        self.style.heading3.alignment = 0

        self.style.small = copy.deepcopy(self.style.normal)
        self.style.small.fontSize = self.style.fontSize - 0.9

        self.style.smaller = copy.deepcopy(self.style.normal)
        self.style.smaller.fontSize = self.style.fontSize * 0.75

        self.style.tableBase = (
            ("FONT", (0, 0), (-1, -1), "%s" % self.style.fontName, self.style.fontSize),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("FIRSTLINEINDENT", (0, 0), (-1, -1), 0),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        )

        self.style.table = self.style.tableBase + (
              ("FONT", (0, 0), (-1, -1), "%s" % self.style.fontName, self.style.fontSize * 0.8),
            ("BACKGROUND", (0, 0), (-1, 0), "#d5dae6"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (-1, 0), (-2, 0), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        )

        self.style.tableLLR = self.style.tableBase + (
            ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),
        )

        self.style.tableHead = self.style.tableBase + (
            (
                "FONT",
                (0, 0),
                (-1, 0),
                "%s-Bold" % self.style.fontName,
                self.style.fontSize,
            ),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LINEABOVE", (0, 0), (-1, 0), 0.2, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 0.2, colors.black),
        )

        self.style.tableOptional = self.style.tableBase + (
            (
                "FONT",
                (0, 0),
                (-1, 0),
                "%s-Italic" % self.style.fontName,
                self.style.fontSize,
            ),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (1, 0), (-1, -1), 2 * cm),
        )

     


# 添加表格
    def add_table(self, data, columns, style=None):
        self.append(Table(data, columns, style=style or self.style.table))
# 添加文字
    def add_text(self, data:str, style=None):
        self.story.append(Paragraph(data, style=style or self.style.normal))



    def append(self,data):
        self.story.append(data)
    
    # 开始添加内容
    def begin_content(self):
        self.append(Spacer(1, 2 * cm))  
    
    # 添加大标题,默认居中
    def add_heading1(self, title: str, is_centered: bool = True):
        if is_centered:
            self.style.heading1.alignment = 1
        else:
            self.style.heading1.alignment = 0
        self.append(Paragraph(title, self.style.heading1))
    
    # 添加中标题
    def add_heading2(self, title: str, is_centered: bool = False):
        if is_centered:
            self.style.heading2.alignment = 1
        else:
            self.style.heading2.alignment = 0
        self.append(Paragraph(title, self.style.heading2))
    
    # 添加小标题
    def add_heading3(self, title: str, is_centered: bool = False):
        if is_centered:
            self.style.heading3.alignment = 1
        else:
            self.style.heading3.alignment = 0
        self.append(Paragraph(title, self.style.heading3))

    def add_info(self, name: str, info:str):
        self.append(self.draw_subtitle(f"{name}: {info}"))
        
    # 添加空格
    def add_space(self, size: float):
        self.append(Spacer(1, size))

 

    
    # 添加水印
    def add_watermark(self, image_path: str, x_offset: float, y_offset: float):
        drawing = Drawing(0, 0)
        image = Image(image_path, width=2.5 * cm, height=2.5 * cm)
        drawing.add(image, (x_offset, y_offset))
        self.story.append(drawing)
    
    # 添加图片
    def add_image(self, image_path: str, width = 400):

        try:
            img = Image(image_path)       # 读取指定路径下的图片
            # 最大宽400
            img.drawHeight = width/img.drawWidth * img.drawHeight 
            img.drawWidth = width
            # 图片居中
            img.hAlign = 'CENTER'
            img.vAlign = 'MIDDLE'
            self.append(img)
            self.add_space(20)
        except Exception as e:
            print(f"Error occurred while adding image: {e}")

        
 
    def on_page(self):
        pass

    def header(self,canvas, doc):
        canvas.saveState()
        pageNumber = canvas.getPageNumber()
        if pageNumber > 0 and self.headerImagePath is not None:
            header_left_image = Image(self.headerImagePath, width=self.headerImageWidth, height=self.headerImageHeight)
            header_left_image.hAlign = 'LEFT'
            header_left_image.drawOn(canvas, doc.leftMargin, doc.bottomMargin+doc.height + 0.5*cm)
            canvas.line(doc.leftMargin, doc.bottomMargin+doc.height + 0.5*cm, doc.leftMargin+doc.width, doc.bottomMargin+doc.height + 0.5*cm) #画一条横线
        canvas.restoreState()

    def footer(self,canvas, doc):
        canvas.saveState()  # 先保存当前的画布状态
        pageNumber = ("%s" % canvas.getPageNumber())  # 获取当前的页码
        p = Paragraph(pageNumber, self.style.normal)
        p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
        p.drawOn(canvas, 300, 50)  # 将页码放在指示坐标处
        canvas.restoreState()

    def header_and_footer(self,canvas, doc):
        self.header(canvas, doc)
        self.footer(canvas, doc)
    # 绘制饼状图
    def add_pie(self,data: list,  items: list):
        drawing = Drawing(width=500, height=200)
        pie = Pie()
        pie.x = 25
        pie.y = -25
        pie.sideLabels = False
        pie.height = 252
        pie.sameRadii          = 1
        pie.direction          = 'clockwise'
        pie.startAngle         = 90
        pie.data = data  
        pie.slices.popout                    = len(data)
        # pie.
        pie.slices.strokeWidth = 0.5
        drawing.add(pie)
        pie_legend = Legend()
        pie_legend.y               = 150
        pie_legend.fontSize        = self.fontSize * 0.8
        pie_legend.fontName        = self.fontName
        pie_legend.dx              = 8
        pie_legend.dy              = 8
        pie_legend.yGap            = 0
        pie_legend.deltay          = 8
        pie_legend.strokeColor     = PCMYKColor(0,0,0,0)
        pie_legend.strokeWidth     = 0
        pie_legend.columnMaximum   = 10
        pie_legend.alignment       ='right'
        pie_legend.x               = 182
        pie_legend.subCols.rpad      = 12
        pie_legend.colorNamePairs.clear()


        for i in range(len(data)):
            # 随机生成颜色
            pie.slices[i].fillColor = random_cmyk_color()



        for i in range(len(items)):
            color = pie.slices[i].fillColor
            
            pie_legend.colorNamePairs.append((color,(items[i], str(data[i]))))
        drawing.add(pie_legend)

        self.append(drawing)
        


        
  




  

