# -*- coding: utf-8 -*-
# @Author: Xia Yunkai
# @Date:   2024-08-17 22:59:51
# @Last Modified by:   Xia Yunkai
# @Last Modified time: 2024-08-18 20:09:52


from document import Document
from reportlab.platypus import SimpleDocTemplate, Frame,PageTemplate
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

import matplotlib.pyplot as plt



if __name__ == '__main__':
    # 创建内容对应的空列表
    content = list()
    # 添加标题
    content.append(Document.draw_title('大标题'))

    # 添加小标题
    content.append(Document.draw_subtitle('小标题'))
   # 添加正文
    content.append(Document.draw_text('11111'))
    # 添加正文
    content.append(Document.draw_text('2222'))
    # 添加正文
    content.append(Document.draw_text('3333'))

    # 添加表格标题
    content.append(Document.draw_table_title('表格标题'))

    data = [
        ['111', '222', '333'],
        ['444', '18.5K', '25%'],
        ['555', '25.5K', '14%'],
        ['666', '29.3K', '10%']
    ]
    content.append(Document.draw_table(data))

    data = [
        ['11','22','33','44'],
        ['aa','bb','cc','dd']
    ]
    content.append(Document.draw_table(data))
    b_data = [(25400, 12900, 20100, 20300, 20300, 17400), (15800, 9700, 12982, 9283, 13900, 7623)]
    ax_data = ['BeiJing', 'ChengDu', 'ShenZhen', 'ShangHai', 'HangZhou', 'NanJing']
    leg_items = [(colors.red, '平均薪资'), (colors.green, '招聘量')]
    content.append(Document.draw_bar(b_data, ax_data, leg_items))

    content.append( Document.draw_chart([10,20,30,40,50],['aa','bb','cc','dd','ee']))

    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.title('Simple Plot')
    plt.xlabel('x')
    plt.ylabel('y')

    # 保存图表为PNG文件
    plt.savefig('image/plot.png')
    plt.close()
    content.append(Document.draw_image('image/plot.png'))
    content.append(Document.draw_image('image/pika.png'))
    doc = SimpleDocTemplate('output/report.pdf',  pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18,
                            showBoundary=0)

    doc.build(content,onFirstPage=Document.footer, onLaterPages=Document.footer)
