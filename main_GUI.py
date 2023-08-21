import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QFileDialog, QProgressBar, QComboBox, QDialog, QScrollArea
)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pandas as pd
import Technology
import Economy
import Politics
import Society


class CrawlerThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, mode, search_text, depth):
        super().__init__()
        self.mode = mode
        self.search_text = search_text
        self.depth = depth

    def run(self):
        if self.mode == '科技':
            data = Technology.crawl_data(self.mode, self.search_text, self.depth)
        elif self.mode == '经济':
            data = Economy.crawl_data(self.mode, self.search_text, self.depth)
        elif self.mode == '政治':
            data = Politics.crawl_data(self.mode, self.search_text, self.depth)
        elif self.mode == '社会':
            data = Society.crawl_data(self.mode, self.search_text, self.depth)
        else:
            data = []

        self.progress_signal.emit(50)

        save_path = self.get_save_path()
        if save_path:
            if save_path.endswith('.xlsx'):
                df = pd.DataFrame(data)
                df.to_excel(save_path, index=False)
            elif save_path.endswith('.csv'):
                df = pd.DataFrame(data)
                df.to_csv(save_path, index=False)
            elif save_path.endswith('.txt'):
                with open(save_path, 'w', encoding='utf-8') as f:
                    for item in data:
                        f.write(str(item) + '\n')

        self.progress_signal.emit(100)

    def get_save_path(self):
        return QFileDialog.getSaveFileName(filter="Excel files (*.xlsx);;CSV files (*.csv);;Text files (*.txt)")[0]


class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("作者碎碎念")
        self.setFixedSize(600, 400)

        scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        scroll_area.setWidget(self.scroll_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        about_text = (
            "这个是一个自动化的数据收集程序，现在推出了1.0版本。\n"
            "这个可以收集科技、经济、政治、社会四个大类的数据。\n"
            "由于每一个网站都有他们自己的 rankPage 算法，所以借助这个原因，我们可以保证爬取到的数据都是得分最好的数据。\n"
            "这些数据对我们进行决策具有重大意义。\n"
            "\n"
            "在2.0版本中，我们计划增添一些智能算法，这将使我们能够对爬取到的数据进行更深入的分析。\n"
            "此外，我们也将提供数据的可视化呈现结果，以便更直观地理解数据的含义。\n"
            "\n"
            "希望这个工具对您有所帮助！"
        )

        about_label = QLabel(about_text)
        self.scroll_layout.addWidget(about_label)

        scroll_area.setWidgetResizable(True)
        layout = QVBoxLayout()
        layout.addWidget(scroll_area, alignment=Qt.AlignTop)
        self.setLayout(layout)


class ModeInfoWindow(QDialog):
    def __init__(self, mode):
        super().__init__()

        self.setWindowTitle(f"{mode} 模式操作指南")
        self.setFixedSize(600, 400)

        scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        scroll_area.setWidget(self.scroll_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        if mode == "经济":
            guide_text = "一、内容\n1、经济(jinji)(48页)\n2、热点(redian)(46页)\n3、媒体(meiti)(1000页)\n4、环球要闻(huanqiu)(26页)\n5、注意搜索内容要填括号里面的拼音，而且搜索深度不能超过最大页数"
        elif mode == "科技":
            guide_text = "一、内容\n1、前端(web)\n2、后端(back-end)\n3、移动开发(mobile)\n4、编程语言(lang)\n5、Java(java)\n6、Python(python)\n7、人工智能(ai)\n8、AIGC(aigc-0)\n9、大数据(big-data)\n10、数据库(database)\n11、数据结构与算法(algo)\n12、音视频(avi)\n13、云原生(cloud-native)\n14、云平台(cloud)\n15、前沿技术(advanced-technology)\n16、开源(open-source)\n17、小程序(miniprog-0)\n18、运维(ops)\n19、服务器(server)\n20、操作系统(os)\n21、硬件开发(hardware)\n22、嵌入式(embedded)\n22、嵌入式(embedded)\n23、微软技术(microsoft)\n24、软件工程(software-engineering)\n24、测试(test)\n25、安全(sec)\n26、网络与通信(telecommunication)\n27、用户体验设计(design)\n28、学习和成长(job)\n29、搜索(search)\n30、开发工具(devtools)\n31、游戏(game)\n32、HarmonyOS(harmonyos)\n33、区域链(blockchain)\n34、数学(math)\n35、3C硬件(3c-hardware)\n36、资讯(news)\n34、数学(math)"
        elif mode == "社会":
            guide_text = "一、内容\n1、社会(society)\n2、国际(world)\n3、国内(china)\n4、法治(law)\n5、文娱(ent)\n6、生活(life)\n7、注意搜索内容要填括号里面的拼音，而且搜索深度不能超过最大页数"
        elif mode == "政治":
            guide_text = "一、内容\n1、时政(politics)\n2、国际(world)\n3、文化(culture)\n4、健康(health)\n5、军事(milpro)\n6、注意搜索内容要填括号里面的拼音，而且搜索深度不能超过最大页数"
        else:
            guide_text = "无操作指南"

        guide_label = QLabel(guide_text)
        self.scroll_layout.addWidget(guide_label)

        scroll_area.setWidgetResizable(True)
        layout = QVBoxLayout()
        layout.addWidget(scroll_area, alignment=Qt.AlignTop)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 500)
        self.init_ui()
    def show_about(self):
        about_window = AboutWindow()
        about_window.exec_()

    def init_ui(self):
        self.setWindowTitle("数据爬取与保存")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.operation_guide_label = QLabel("操作指南:\n1. 选择模式\n2. 输入搜索内容和输入搜索深度\n3. 点击“开始”按钮\n4. 选择保存文件路径")
        layout.addWidget(self.operation_guide_label)

        self.mode_label = QLabel("选择模式:")
        layout.addWidget(self.mode_label)

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(['经济', '科技', '社会', '政治'])
        layout.addWidget(self.mode_combobox)

        self.search_label = QLabel("搜索内容:")
        layout.addWidget(self.search_label)

        self.search_text_edit = QLineEdit()
        layout.addWidget(self.search_text_edit)

        self.depth_label = QLabel("搜索深度:")
        layout.addWidget(self.depth_label)

        self.depth_edit = QLineEdit()
        layout.addWidget(self.depth_edit)

        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_crawling)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        layout.addWidget(self.result_text_edit)

        self.about_button = QPushButton("作者碎碎念")
        self.about_button.clicked.connect(self.show_about)
        layout.addWidget(self.about_button)

        self.mode_info_button = QPushButton("查看操作指南")
        self.mode_info_button.clicked.connect(self.show_mode_info)
        layout.addWidget(self.mode_info_button)

        self.central_widget.setLayout(layout)

        self.crawler_thread = None

    def start_crawling(self):
        if self.crawler_thread is None or not self.crawler_thread.isRunning():
            self.crawler_thread = CrawlerThread(self.mode_combobox.currentText(), self.search_text_edit.text(), self.depth_edit.text())
            self.crawler_thread.progress_signal.connect(self.update_progress_bar)
            self.crawler_thread.finished.connect(self.crawling_finished)
            self.crawler_thread.start()
            self.start_button.setEnabled(False)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def crawling_finished(self):
        self.result_text_edit.moveCursor(QTextCursor.End)
        self.result_text_edit.insertPlainText("\n爬取完成！")
        self.result_text_edit.moveCursor(QTextCursor.End)
        self.start_button.setEnabled(True)

    def show_mode_info(self):
        selected_mode = self.mode_combobox.currentText()
        mode_info_window = ModeInfoWindow(selected_mode)
        mode_info_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
