#include <QApplication>
#include <QDesktopWidget>
#include <QFile>
#include <QDebug>

#include "senseWindow.h"

int main(int argc, char *argv[])
{
    QApplication * app = new QApplication(argc, argv);
    senseWindow * sense_window = new senseWindow();

    QFile file(":/Resources/style.qss");
    if(file.open(QFile::ReadOnly)) {
       QString StyleSheet = QLatin1String(file.readAll());
       sense_window->setStyleSheet(StyleSheet);
    }
    sense_window->resize( QApplication::desktop()->size() );
    sense_window->show();

    return app->exec();
}
