#include "customTableWidget.h"

#include <QWidgetItem>

customTableWidget::customTableWidget( QWidget *parent )
: QTableWidget( parent )
{
    setSelectionMode(QAbstractItemView::NoSelection);

    connect( this, SIGNAL( clicked( const QModelIndex& ) ),
          this, SLOT( selectRow( const QModelIndex& ) ));
}

//--------------------------------------------------------------------

customTableWidget::~customTableWidget()
{
     this->QTableWidget::~QTableWidget();
}

//--------------------------------------------------------------------

void customTableWidget::editItem( QTableWidgetItem * item)
{
    //do nothing
}

//--------------------------------------------------------------------

void customTableWidget::selectRow( const QModelIndex& index )
{
     //do nothing
}
