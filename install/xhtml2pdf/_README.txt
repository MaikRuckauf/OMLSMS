Xhtml2pdf is a package for python that converts html to pdf documents.

*************************************************************************
Note: This support for this library is questionable.  I have switched
to wkhtmltopdf instead.  I didn't make  python wrappers for the library,
so there are two temporary files and OS calls when printing.  Hopefully,
this will not prove to be a performance issue.
*************************************************************************

To install, first install pip.  Then:



I will recommend using virtualenv for development. This is great to have separate environment for each project, keeping the dependencies for multiple projects separated:

sudo pip install virtualenv

For more information about virtualenv refer to http://www.virtualenv.org/

Create virtualenv for the project. This can be inside the project directory, but cannot be under version control:

virtualenv --distribute xhtml2pdfenv --python=python2

Activate your virtualenv:

source xhtml2pdfenv/bin/activate

Later to deactivate use:

deactivate

Next step will be to install/upgrade dependencies from requirements.txt file:

pip install -r requirements.txt

Run tests to check your configuration:

nosetests --with-coverage

You should have a log with success status:

Ran 36 tests in 0.322s

OK

