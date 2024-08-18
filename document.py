# -*- coding: utf-8 -*-
# @Author: Xia Yunkai
# @Date:   2024-08-17 21:26:21
# @Last Modified by:   Xia Yunkai
# @Last Modified time: 2024-08-18 21:27:29


from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm  # 单位：cm
from reportlab.graphics.charts.piecharts import Pie

# 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
pdfmetrics.registerFont(TTFont('SimSun', 'font/SimSun.ttf'))


class Document:
    # 绘制标题
    @staticmethod
    def draw_title(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Heading1']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'      # 字体名
        ct.fontSize = 18            # 字体大小
        ct.leading = 50             # 行间距
        ct.textColor = colors.black     # 字体颜色
        ct.alignment = 1    # 居中
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
    
    # 绘制小标题
    @staticmethod
    def draw_subtitle(title: str):
        style = getSampleStyleSheet()
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 15  # 字体大小
        ct.leading = 1.5 * ct.fontSize  # 行间距
        ct.textColor = colors.black  # 字体颜色
        return Paragraph(title, ct)


    # 添加正文文本
    @staticmethod
    def draw_text(text: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 获取普通样式
        ct = style['Normal']
        ct.fontName = 'SimSun'
        ct.fontSize = 12
        ct.wordWrap = 'CJK'     # 设置自动换行
        ct.alignment = 0        # 左对齐
        ct.firstLineIndent = 32     # 第一行开头空格
        ct.leading = 25
        return Paragraph(text, ct)
    
        # 绘制表格标题
    @staticmethod
    def draw_table_title(title: str):
        # 拿到标题样式
        style = getSampleStyleSheet()
        ct = style['Heading1']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 14  # 字体大小
        ct.leading = 15  # 行间距
        ct.textColor = colors.black  # 字体颜色
        ct.alignment = 1  # 居中
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
    
  
    
    @staticmethod
    def draw_table( data: list[list]):
        colWidths = 400 / len(data[0])
        dis_list = []
        for x in data:
            dis_list.append(x)
        style = [
            ("FONTNAME", (0, 0), (-1, -1), 'SimSun'),
            ("BACKGROUND", (0, 0), (-1, 0), "#d5dae6"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (-1, 0), (-2, 0), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]
        component_table = Table(dis_list, colWidths=colWidths, style=style)
        return component_table
    
    @staticmethod
    def draw_image(path:str):
        img = Image(path)       # 读取指定路径下的图片
        # 最大宽400
        img.drawHeight = 600/img.drawWidth * img.drawHeight 
        img.drawWidth = 600
        # 图片居中
        img.hAlign = 'CENTER'
        img.vAlign = 'MIDDLE'
        # 图片返回
        return img
    
     # 创建图表
    @staticmethod
    def draw_bar(bar_data: list, ax: list, items: list):
        drawing = Drawing(500, 250)
        bc = VerticalBarChart()
        bc.x = 45       # 整个图表的x坐标
        bc.y = 45      # 整个图表的y坐标
        bc.height = 200     # 图表的高度
        bc.width = 350      # 图表的宽度
        bc.data = bar_data
        bc.strokeColor = colors.black       # 顶部和右边轴线的颜色
        bc.valueAxis.valueMin = 5000           # 设置y坐标的最小值
        bc.valueAxis.valueMax = 26000         # 设置y坐标的最大值
        bc.valueAxis.valueStep = 2000         # 设置y坐标的步长
        bc.categoryAxis.labels.dx = 2
        bc.categoryAxis.labels.dy = -8
        bc.categoryAxis.labels.angle = 20
        bc.categoryAxis.categoryNames = ax

        # 图示
        leg = Legend()
        leg.fontName = 'SimSun'
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = 475         # 图例的x坐标
        leg.y = 240
        leg.dxTextSpace = 10
        leg.columnMaximum = 3
        leg.colorNamePairs = items
        drawing.add(leg)
        drawing.add(bc)
        return drawing
    
    # 设置页脚
    @staticmethod
    def footer(canvas, doc):
         # 拿到标题样式
        style = getSampleStyleSheet()
        ct = style['Heading1']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 14  # 字体大小
        ct.leading = 15  # 行间距
        ct.textColor = colors.black  # 字体颜色
        ct.alignment = 1  # 居中
        canvas.saveState()  # 先保存当前的画布状态
        pageNumber = ("%s" % canvas.getPageNumber())  # 获取当前的页码
        p = Paragraph(pageNumber, ct)
        p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
        p.drawOn(canvas, 300, 50)  # 将页码放在指示坐标处
        canvas.restoreState()
        
    @staticmethod
    def draw_chart(data: list,  items: list):
        drawing = Drawing(width=500, height=200)
        pie = Pie()
        pie.x = 150
        pie.y = 65
        pie.sideLabels = False
        pie.labels = items
        pie.data = data  
        pie.slices.strokeWidth = 0.5
        drawing.add(pie)
        return drawing
    
    # 创建于构建pdf
    @staticmethod
    def create_doc(name:str,content:list):
        doc = SimpleDocTemplate(name, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
        doc.build(content,onFirstPage=Document.footer, onLaterPages=Document.footer)
      




  

