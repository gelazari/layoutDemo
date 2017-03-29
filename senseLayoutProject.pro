QT += widgets

HEADERS     = \
              senseWindow.h \
    senseLayout.h \
    customTableWidget.h \
    customstackedwidget.h \
    sensorwindow.h \
    controllerwindow.h
SOURCES     = \
              main.cpp \
              senseWindow.cpp \
    senseLayout.cpp \
    customTableWidget.cpp \
    customstackedwidget.cpp \
    sensorwindow.cpp \
    controllerwindow.cpp
# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/layouts/borderlayout
INSTALLS += target

DISTFILES +=

RESOURCES += \
    resources.qrc
