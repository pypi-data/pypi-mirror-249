# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'channel_configuration_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ChannelConfigurationWidget(object):
    def setupUi(self, ChannelConfigurationWidget):
        if not ChannelConfigurationWidget.objectName():
            ChannelConfigurationWidget.setObjectName(u"ChannelConfigurationWidget")
        ChannelConfigurationWidget.resize(299, 164)
        self.main_layout = QVBoxLayout(ChannelConfigurationWidget)
        self.main_layout.setSpacing(15)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(-1, 20, -1, 20)
        self.input_channel_configuration_label = QLabel(ChannelConfigurationWidget)
        self.input_channel_configuration_label.setObjectName(u"input_channel_configuration_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_channel_configuration_label.sizePolicy().hasHeightForWidth())
        self.input_channel_configuration_label.setSizePolicy(sizePolicy)
        self.input_channel_configuration_label.setMinimumSize(QSize(0, 30))
        self.input_channel_configuration_label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(16)
        self.input_channel_configuration_label.setFont(font)

        self.main_layout.addWidget(self.input_channel_configuration_label, 0, Qt.AlignHCenter)

        self.input_channel_configuration_layout = QGridLayout()
        self.input_channel_configuration_layout.setObjectName(u"input_channel_configuration_layout")
        self.input_channel_configuration_layout.setVerticalSpacing(4)

        self.main_layout.addLayout(self.input_channel_configuration_layout)

        self.output_channel_configuration_label = QLabel(ChannelConfigurationWidget)
        self.output_channel_configuration_label.setObjectName(u"output_channel_configuration_label")
        sizePolicy.setHeightForWidth(self.output_channel_configuration_label.sizePolicy().hasHeightForWidth())
        self.output_channel_configuration_label.setSizePolicy(sizePolicy)
        self.output_channel_configuration_label.setMinimumSize(QSize(0, 30))
        self.output_channel_configuration_label.setMaximumSize(QSize(16777215, 30))
        self.output_channel_configuration_label.setFont(font)

        self.main_layout.addWidget(self.output_channel_configuration_label, 0, Qt.AlignHCenter)

        self.output_channel_configuration_layout = QGridLayout()
        self.output_channel_configuration_layout.setObjectName(u"output_channel_configuration_layout")
        self.output_channel_configuration_layout.setVerticalSpacing(4)

        self.main_layout.addLayout(self.output_channel_configuration_layout)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(self.vertical_spacer)


        self.retranslateUi(ChannelConfigurationWidget)

        QMetaObject.connectSlotsByName(ChannelConfigurationWidget)
    # setupUi

    def retranslateUi(self, ChannelConfigurationWidget):
        ChannelConfigurationWidget.setWindowTitle(QCoreApplication.translate("ChannelConfigurationWidget", u"Channel Configuration", None))
        self.input_channel_configuration_label.setText(QCoreApplication.translate("ChannelConfigurationWidget", u"Input Channel Configuration", None))
        self.output_channel_configuration_label.setText(QCoreApplication.translate("ChannelConfigurationWidget", u"Output Channel Configuration", None))
    # retranslateUi

