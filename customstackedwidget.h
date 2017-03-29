#ifndef CUSTOMSTACKEDWIDGET_H
#define CUSTOMSTACKEDWIDGET_H

#include <QVariant>
#include <QWidget>
#include <QLabel>
#include <QStackedWidget>

class customStackedWidget : public QStackedWidget
{
    Q_OBJECT

    Q_PROPERTY( float rotateVal READ rotateVal WRITE setRotateVal)
    public:
        explicit customStackedWidget(QWidget *parent = 0);
        void paintEvent(QPaintEvent *);
        void rotate(int);

        float rotateVal();
        void setRotateVal(float);
    public slots:
        void setCurrentIndex(int index);
    private slots:
        void valChanged(QVariant);
        void animDone();
    private:
        float iRotateVal;

        bool isAnimating;
        int nextIndex;
};

#endif // CUSTOMSTACKEDWIDGET_H
