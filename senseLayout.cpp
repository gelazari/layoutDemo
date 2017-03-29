#include "senseLayout.h"
#include <QDebug>

namespace
{
    const int FIXED_TOP_EXTRA_HEIGHT = 0;
}

senseLayout::senseLayout(QWidget *parent, int margin, int spacing)
    : QLayout(parent)
{
    setMargin(margin);
    setSpacing(spacing);
}

//--------------------------------------------------------------------

senseLayout::senseLayout(int spacing)
{
    setSpacing(spacing);
}


//--------------------------------------------------------------------

senseLayout::~senseLayout()
{
    QLayoutItem *l;
    while ((l = takeAt(0)))
        delete l;
}

//--------------------------------------------------------------------

void senseLayout::addItem(QLayoutItem *item)
{
    add(item, LEFT);
}

//--------------------------------------------------------------------

void senseLayout::addWidget(QWidget *widget, Position position)
{
    add(new QWidgetItem(widget), position);
}

//--------------------------------------------------------------------

Qt::Orientations senseLayout::expandingDirections() const
{
    return Qt::Horizontal | Qt::Vertical;
}

//--------------------------------------------------------------------

bool senseLayout::hasHeightForWidth() const
{
    return false;
}

//--------------------------------------------------------------------

int senseLayout::count() const
{
    return list.size();
}

//--------------------------------------------------------------------

QLayoutItem *senseLayout::itemAt(int index) const
{
    ItemWrapper *wrapper = list.value(index);
    if (wrapper)
        return wrapper->item;
    else
        return 0;
}

//--------------------------------------------------------------------

QSize senseLayout::minimumSize() const
{
    return calculateSize(MinimumSize);
}

//--------------------------------------------------------------------

void senseLayout::setGeometry(const QRect &rect)
{
    ItemWrapper *center = 0;
    int LEFTWidth = 0;
    int TOPHeight = 0;
    int BOTTOMHeight = 0;
    int MIDDLEHeight = 0;
    int RIGHTWidth = 0;
    int i;

    QLayout::setGeometry(rect);

    for (i = 0; i < list.size(); ++i) {
        ItemWrapper *wrapper = list.at(i);
        QLayoutItem *item = wrapper->item;
        Position position = wrapper->position;

        if (position == TOP)
        {
            item->setGeometry( QRect( rect.x(), TOPHeight, rect.width(),
                                    item->sizeHint().height() + FIXED_TOP_EXTRA_HEIGHT ) );
            TOPHeight += item->geometry().height() + spacing() + 1;
        }
        else if (position == BOTTOM)
        {
            item->setGeometry(QRect(item->geometry().x(),
                                    item->geometry().y(), rect.width(),
                                    item->sizeHint().height()));

            BOTTOMHeight += item->geometry().height() + spacing();

            item->setGeometry(QRect(rect.x(),
                              rect.y() + rect.height() - BOTTOMHeight + spacing(),
                              item->geometry().width(),
                              item->geometry().height()));
        }
        else if (position == MIDDLE)
        {
            center = wrapper;
        }
    }

    MIDDLEHeight = rect.height() - TOPHeight - BOTTOMHeight;

    for (i = 0; i < list.size(); ++i) {
        ItemWrapper *wrapper = list.at(i);
        QLayoutItem *item = wrapper->item;
        Position position = wrapper->position;

        if (position == LEFT)
        {
            item->setGeometry(QRect(rect.x() + LEFTWidth, TOPHeight,
                                    item->sizeHint().width(), MIDDLEHeight));

            LEFTWidth += item->geometry().width() + spacing();
        }
    }

    if (MIDDLE)
    {

        center->item->setGeometry(QRect(LEFTWidth, TOPHeight,
                                        rect.width() - RIGHTWidth - LEFTWidth,
                                        MIDDLEHeight));
    }
}

//--------------------------------------------------------------------

QSize senseLayout::sizeHint() const
{
    return calculateSize(SizeHint);
}

//--------------------------------------------------------------------

QLayoutItem *senseLayout::takeAt(int index)
{
    if (index >= 0 && index < list.size()) {
        ItemWrapper *layoutStruct = list.takeAt(index);
        return layoutStruct->item;
    }
    return 0;
}

//--------------------------------------------------------------------

void senseLayout::add(QLayoutItem *item, Position position)
{
    list.append(new ItemWrapper(item, position));
}

//--------------------------------------------------------------------

QSize senseLayout::calculateSize(SizeType sizeType) const
{
    QSize totalSize;

    for (int i = 0; i < list.size(); ++i) {
        ItemWrapper *wrapper = list.at(i);
        Position position = wrapper->position;
        QSize itemSize;

        if (sizeType == MinimumSize)
            itemSize = wrapper->item->minimumSize();
        else // (sizeType == SizeHint)
            itemSize = wrapper->item->sizeHint();

        if (position == TOP )
            totalSize.rheight() += itemSize.height();

        if ( position == BOTTOM )
            totalSize.rheight() += itemSize.height();

        if ( position == MIDDLE )
            totalSize.rheight() += itemSize.height();

        if ( position == LEFT || position == MIDDLE )
            totalSize.rwidth() += itemSize.width();
    }
    return totalSize;
}
