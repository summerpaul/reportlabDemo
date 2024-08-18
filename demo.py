# -*- coding: utf-8 -*-
# @Author: Xia Yunkai
# @Date:   2024-08-17 22:59:51
# @Last Modified by:   Xia Yunkai
# @Last Modified time: 2024-08-18 21:14:21


from document import Document

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

    Document.create_doc('output/report.pdf',content)
