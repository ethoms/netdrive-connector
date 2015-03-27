import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from NetdriveConnector import NetdriveConnector

def main():

    # create application
    app = QApplication( sys.argv )
    app.setApplicationName( 'netdrive-connector' )

    # create widget
    w = NetdriveConnector()
    w.setWindowTitle( 'Netdrive Connector v1.1' )
    w.resize(700,600)
    w.setWindowIcon(QIcon('/usr/share/pixmaps/netdrive-connector.png'))
    w.show()

    # connection
    QObject.connect( app, SIGNAL( 'lastWindowClosed()' ), app, SLOT( 'quit()' ) )

    # execute application
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
