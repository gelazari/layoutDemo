#include "senseLayout.h"
#include "senseWindow.h"
#include "sensorwindow.h"
#include "controllerwindow.h"
#include "customstackedwidget.h"

#include <QLabel>
#include <QFrame>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QPushButton>
#include <QToolButton>
#include <QIcon>
#include <customtablewidget.h>
#include <QTableWidgetItem>
#include <QHeaderView>
#include <QFile>
#include <QColor>
#include <QDebug>

senseWindow::senseWindow(QWidget * parent)
    :QMainWindow(parent)
{
    this->layout = new senseLayout();
    this->central_layout_frame = createCentralLayout();
    this->layout->addWidget( this->central_layout_frame, senseLayout::MIDDLE );
    this->layout->addWidget( createTopLayout(), senseLayout::TOP );
    this->layout->addWidget( createLeftLayout(), senseLayout::LEFT );
    this->layout->addWidget( createLabel("Just a label - Untitled.spj"), senseLayout::BOTTOM );

    this->the_central_widget = new QWidget(this);
    this->the_central_widget->setLayout(layout);

    QObject::connect(this->sensor_button, SIGNAL( clicked() ), this, SLOT(setSensorSection()));
    QObject::connect(this->controller_button, SIGNAL( clicked() ), this, SLOT(setControllerSection()));

    setCentralWidget(this->the_central_widget);

    setWindowTitle(tr("Sense Demo App"));
}

//---------------------------------------------------------------

void senseWindow::setControllerSection()
{
    this->central_widget->setCurrentIndex(1);
    this->sensor_button->setChecked(false);
    this->controller_button->setChecked(true);
}

//---------------------------------------------------------------

void senseWindow::setSensorSection()
{
    this->central_widget->setCurrentIndex(0);
    this->sensor_button->setChecked(true);
    this->controller_button->setChecked(false);
}

//---------------------------------------------------------------

QLabel * senseWindow::createLabel(const QString &text)
{
    QLabel *label = new QLabel(text);
    label->setFrameStyle(QFrame::Box | QFrame::Raised);
    return label;
}

//---------------------------------------------------------------

void senseWindow::changeText()
{
    this->controller_button->setText("asdf");
}

//---------------------------------------------------------------

void senseWindow::changeText(const QString & string)
{
    this->sensor_button->setText(string);
    this->controller_button->setText(string);
}

//---------------------------------------------------------------

QFrame * senseWindow::createTopLayout()
{
    this->first_button = new QPushButton;
    QObject::connect( first_button, SIGNAL(clicked()), this, SLOT(changeText()));
    first_button->setText("The first button");
    first_button->setObjectName("firstButton");
    first_button->setIcon( getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    first_button->setIconSize( QSize(56, 56 ) );
    first_button->setFixedWidth( 200 );
    first_button->setProperty("buttonType", "topPanelButton");

    QPushButton * second_button = new QPushButton;
    second_button->setText("The second button");
    second_button->setObjectName("secondButton");
    second_button->setIcon( getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    second_button->setIconSize( QSize(56, 56 ) );
    second_button->setFixedWidth( 200 );
    second_button->setProperty("buttonType", "topPanelButton");

    QPushButton * third_button = new QPushButton;
    third_button->setText("The third button");
    third_button->setObjectName("thirdButton");
    third_button->setIcon( getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    third_button->setIconSize( QSize(56, 56 ) );
    third_button->setFixedWidth( 200 );
    third_button->setProperty("buttonType", "topPanelButton");

    QHBoxLayout * top_layout_for_buttons = new QHBoxLayout();
    top_layout_for_buttons->addWidget(first_button, 0, Qt::AlignLeft);
    top_layout_for_buttons->addWidget(second_button, 0, Qt::AlignLeft);
    top_layout_for_buttons->addWidget(third_button, 0, Qt::AlignLeft);
    top_layout_for_buttons->setSpacing(10);
    top_layout_for_buttons->addStretch( 0 );
    top_layout_for_buttons->setMargin(0);
    top_layout_for_buttons->setContentsMargins(0,0,0,0);

    QFrame * top_layout_frame = new QFrame;
    top_layout_frame->setLayout(top_layout_for_buttons);
    top_layout_frame->setContentsMargins(0,0,0,0);

    return top_layout_frame;
}

//---------------------------------------------------------------

QFrame * senseWindow::createLeftLayout()
{
    this->sensor_button = createLeftPanelPushButton("Sensor", getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    this->sensor_button->setObjectName("sensorButton");
    this->sensor_button->setCheckable(true);

    this->controller_button = createLeftPanelPushButton("Controller", getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    this->controller_button->setObjectName("controllerButton");
    this->controller_button->setCheckable(true);

    QPushButton * third_button = createLeftPanelPushButton("Analysis", getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    third_button->setObjectName("analysisButton");
    third_button->setDisabled(true);

    QPushButton * forth_button = createLeftPanelPushButton("Kyriakos button", getIconFromPath("/Users/G_Laza/Desktop/mushroom.ico") );
    forth_button->setObjectName("kyrbutton");
    forth_button->setDisabled(true);

    QVBoxLayout * left_layout_for_buttons = new QVBoxLayout();
    left_layout_for_buttons->addWidget(sensor_button, 0, Qt::AlignTop);
    left_layout_for_buttons->addWidget(controller_button, 0, Qt::AlignTop);
    left_layout_for_buttons->addWidget(third_button, 0, Qt::AlignTop);
    left_layout_for_buttons->addWidget(forth_button, 0, Qt::AlignTop);
    left_layout_for_buttons->setSpacing(10);
    left_layout_for_buttons->addStretch( 0 );
    left_layout_for_buttons->setMargin(0);
    left_layout_for_buttons->setContentsMargins(0,0,0,0);

    QFrame * left_layout_frame = new QFrame;
    left_layout_frame->setFixedWidth(200);
    left_layout_frame->setLayout(left_layout_for_buttons);
    left_layout_frame->setContentsMargins(0,0,0,0);
    //left_layout_frame->setStyleSheet("background-color: red;");

    return left_layout_frame;
}

//--------------------------------------------------------------------

QFrame * senseWindow::createCentralLayout()
{
    this->central_widget = new QStackedWidget(this);
    this->central_widget->addWidget( createSection(Sensor) );
    this->central_widget->addWidget( createSection(Controller) );
//    this->central_widget->addWidget( createSection(Analysis) );
//    this->central_widget->addWidget( createSection(StackUp) );
//    this->central_widget->addWidget( createSection(Pattern) );
//    this->central_widget->addWidget( createSection(Traces) );

    qDebug() << this->central_widget->widget(0);
    qDebug() << this->central_widget->widget(1);

    customTableWidget* table = new customTableWidget();
    QTableWidgetItem* tableItem = new QTableWidgetItem();

    //Set table row count 4 and column count 3
    table->setRowCount(5);
    table->setColumnCount(6);

    table->setSizePolicy(QSizePolicy::Minimum,QSizePolicy::Minimum);

    //Set Header items here
    table->setHorizontalHeaderItem(0, createHeaderItem("Sensor"));
    table->setHorizontalHeaderItem(1, createHeaderItem("Analysis"));
    table->setHorizontalHeaderItem(2, createHeaderItem("Controller"));
    table->setHorizontalHeaderItem(3, createHeaderItem("Pattern"));
    table->setHorizontalHeaderItem(4, createHeaderItem("Stack Up"));
    table->setHorizontalHeaderItem(5, createHeaderItem("Traces"));
    table->horizontalHeader()->setProperty("headerType", "tableHeader");

    //Add Table items here
    table->setItem(0,0, createTableWidgetItem("ITEM 1_1"));
    table->setItem(0,1, createTableWidgetItem("ITEM 1_2"));

    table->setItem(1,0, createTableWidgetItem("ITEM 2_1"));
    table->setItem(1,1, createTableWidgetItem("ITEM 2_2"));

    table->setItem(2,0, createTableWidgetItem("ITEM 3_1"));
    table->setItem(2,1, createTableWidgetItem("ITEM 3_2"));

    table->setItem(3,0, createTableWidgetItem("ITEM 4_1"));
    table->setItem(3,1, createTableWidgetItem("ITEM 4_2"));

    //Add Spanning Widget to Right-Most Element of First Row
    table->setItem(0,2,tableItem);

    //Span Right-Most Item of First Row Here
    table->setSpan(0,2,table->rowCount(),1);
    table->setShowGrid(false);
    table->verticalHeader()->setVisible(false);
    table->resizeColumnsToContents();
    table->resizeRowsToContents();

    QHeaderView* header = table->horizontalHeader();
    header->setSectionResizeMode(QHeaderView::Stretch);

    table->setHorizontalHeader( header );

    QVBoxLayout * central_widget_layout = new QVBoxLayout;
    central_widget_layout->addWidget( this->central_widget );
    central_widget_layout->addWidget( createSimluationSummaryFrame() );
    central_widget_layout->setSpacing(0);
    central_widget_layout->setMargin(0);
    central_widget_layout->setContentsMargins(0,0,0,0);
    central_widget_layout->addWidget( table );

    QFrame * central_frame = new QFrame;
    central_frame->setLayout(central_widget_layout);

    return central_frame;
}

//---------------------------------------------------------------

QIcon senseWindow::getIconFromPath( const QString & iconPath )
{
    return QIcon(iconPath);
}

//---------------------------------------------------------------

QTableWidgetItem * senseWindow::createTableWidgetItem( const QString & text )
{
    QTableWidgetItem * item = new QTableWidgetItem( text );
    item->setFlags( Qt::NoItemFlags );
    item->setFlags( item->flags() ^ Qt::ItemIsEditable );
    item->setForeground( QColor::fromRgb(0,0,0) );
    item->setTextAlignment( Qt::AlignCenter );

    return item;
}

//---------------------------------------------------------------

QTableWidgetItem * senseWindow::createHeaderItem( const QString & text )
{
    QTableWidgetItem * item = new QTableWidgetItem( text );
    item->setFlags( Qt::NoItemFlags );
    item->setFlags( item->flags() ^ Qt::ItemIsEditable );
    item->setTextAlignment( Qt::AlignCenter );

    return item;
}

//---------------------------------------------------------------

QFrame * senseWindow::createSimluationSummaryFrame()
{
    QLabel * simulation_summary_label = new QLabel("Simulation Summary");
    simulation_summary_label->setFrameStyle(QFrame::NoFrame);
    simulation_summary_label->setProperty("labelType", "simulationSummaryLabel");

    QHBoxLayout * simulation_summary_layout = new QHBoxLayout;
    simulation_summary_layout->addWidget(simulation_summary_label, 0, Qt::AlignCenter);

    QFrame * simulation_summary_frame = new QFrame;
    simulation_summary_frame->setLayout(simulation_summary_layout);
    simulation_summary_frame->setProperty("frameType","simulationSummaryFrame");

    return simulation_summary_frame;
}

//---------------------------------------------------------------

QPushButton * senseWindow::createLeftPanelPushButton(const QString & text, const QIcon & icon )
{
    QPushButton * left_button = new QPushButton;
    left_button->setText(text);
    left_button->setIcon( icon );
    left_button->setIconSize( QSize(56, 56 ) );
    left_button->setProperty("buttonType", "leftPanelButton");

    return left_button;
}

//---------------------------------------------------------------

QWidget * senseWindow::createSection(const Section & section)
{
    if ( section == Section::Sensor)
    {
        qDebug() << "I come in here";
        return new sensorwindow(this);
    }
    if ( section == Section::Controller)
    {
        qDebug() << "I also come in here?";
        return new controllerwindow(this);
    }
    if ( section == Section::Analysis)
    {
        return new QWidget();
    }
    if ( section == Section::StackUp)
    {
        return new QWidget();
    }
    if ( section == Section::Pattern)
    {
        return new QWidget();
    }
    if ( section == Section::Traces)
    {
        return new QWidget();
    }

    return new QWidget();
}
