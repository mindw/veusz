#    Copyright (C) 2005 Jeremy S. Sanders
#    Email: Jeremy Sanders <jeremy@jeremysanders.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##############################################################################
 
# $Id$

"""A FITS import dialog."""

import qt

# delay initialisation until dialog is opened
pyfits = None

class ImportFITS(qt.QDialog):
    """A dialog for importing FITS files."""

    dirname = '.'

    def __init__(self, parent, document):
        qt.QDialog.__init__(self, parent)
        self.setCaption('Import FITS file - Veusz')
        self.document = document

        self.spacing = self.fontMetrics().height() / 2

        # layout for dialog
        layout = qt.QVBoxLayout(self, self.spacing)
        
        # lazy load pyfits, so we don't have to wait until startup
        global pyfits
        if pyfits == None:
            try:
                import pyfits as PF
                pyfits = PF
            except ImportError:
                pyfits = None

        # if pyfits is not installed
        if pyfits == None:
            l = qt.QLabel('FITS file support requires that pyfits is placed'
                          ' in the PYTHONPATH. Please download from blah...',
                          self)
            l.setAlignment( l.alignment() | qt.Qt.WordBreak )
            layout.addWidget(l)
            b = qt.QPushButton("&Close", self)
            layout.addWidget(b)
            self.connect(b, qt.SIGNAL('clicked()'), self.slotClose)
            return

        # change the filename
        fnhbox = qt.QHBox(self)
        fnhbox.setSpacing(self.spacing)
        layout.addWidget( fnhbox )
        l = qt.QLabel('&Filename:', fnhbox)
        self.filenameedit = qt.QLineEdit(fnhbox)
        l.setBuddy(self.filenameedit)
        qt.QToolTip.add(self.filenameedit,
                        'The name of the file to import data from')

        qt.QObject.connect( self.filenameedit,
                            qt.SIGNAL('textChanged(const QString&)'),
                            self.slotFilenameChanged )

        browsebutton = qt.QPushButton("&Browse...", fnhbox)
        qt.QObject.connect( browsebutton, qt.SIGNAL('clicked()'),
                            self.slotBrowse )

        # list view to hold the fits structure
        self.listview = qt.QListView(self)
        self.listview.addColumn('Item')
        self.listview.addColumn('Type')

        # buttons
        w = qt.QWidget(self)
        layout.addWidget(w)
        w.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        l = qt.QHBoxLayout(w, 0, self.spacing)
        l.addItem( qt.QSpacerItem(1, 1, qt.QSizePolicy.Expanding,
                                  qt.QSizePolicy.Minimum) )
        
        b = qt.QPushButton("&Import", w)
        self.importbutton = b
        b.setEnabled(False)
        b.setDefault(True)
        l.addWidget(b)
        self.connect(b, qt.SIGNAL('clicked()'), self.slotImport)
        b = qt.QPushButton("&Close", w)
        l.addWidget(b)
        self.connect(b, qt.SIGNAL('clicked()'), self.slotClose)

    def slotBrowse(self):
        """Browse button pressed in dialog."""

        fd = qt.QFileDialog(self, 'importfitsdialog', True)
        fd.setDir( ImportFITS.dirname )
        fd.setMode( qt.QFileDialog.ExistingFile )
        fd.setCaption('Browse FITS file')
        fd.addFilter('FITS files (*.fits *.FITS)')

        # okay was selected
        if fd.exec_loop() == qt.QDialog.Accepted:
            # save directory for next time
            ImportFITS.dirname = fd.dir()
            # update the edit box
            self.filenameedit.setText( fd.selectedFile() )

    def slotFilenameChanged(self, filename):
        """Update preview window when filename changed."""

        filename = unicode(filename)
        try:
            ifile = open(filename)
            line = ifile.readline()
            # is this a hack?
            if line.find('/ file does conform to FITS standard') == -1:
                raise IOError
            ifile.close()
            self.updateListView(filename)
            self.importbutton.setEnabled(True)

        except IOError:
            self.importbutton.setEnabled(False)

    def updateListView(self, filename):
        """Update the listview with the structure of the file."""

        f = pyfits.open(filename, 'readonly')
        lv = self.listview
        lv.clear()

    def slotClose(self):
        """Close dialog."""
        self.close(True)

    def slotImport(self):
        """Actually import the data."""
        pass
    