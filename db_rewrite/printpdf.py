import os, tempfile, subprocess
#import time
#import win32print

# defined by main() after loading config file:
# printpdf.pdfview_filename = configValues[PDF_VIEWER_PATH]
# printpdf.gsprint_filename = configValues[PDF_PRINTER_PATH]
# printpdf.htmltopdf_filename = configValues[HTML_CONVERTER_PATH]
# printpdf.labelPrinterName = configValues[LABEL_PRINTER]
# printpdf.defaultPrinterName = configValues[DEFAULT_PRINTER]
testPrinting = False # test printing, use a viewer rather than send directly to printer

'''    
def printPDF(PDF_string):
    try:
        file = tempfile.NamedTemporaryFile (suffix=".html", delete=False)
        file.write (PDF_string)
        file.close()
    except:
        raise EnvironmentError(101, "Error opening temporary file.")
    
    try:
        p = subprocess.Popen([gsviewpath, file.name], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except:
        raise EnvironmentError(102, "Error printing file.")
    
    try:
        os.remove(file.name)
    except:
        raise Warning("Could not delete temporary file: %s." % file.name)

    return None
'''

def printHTML(HTML_string, useLabelPrinter=False):
    startupinfo = subprocess.STARTUPINFO()
    if not testPrinting:
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW # prevent dos box popup
        print_app = gsprint_filename, 
    else:
        print_app = pdfview_filename

    try:
        file = tempfile.NamedTemporaryFile (suffix=".html", delete=False)
        file.write (HTML_string)
        file.close()
    except:
        raise EnvironmentError(101, "Error opening temporary file.")

    try:
        pdffilename = os.path.join(os.path.dirname(file.name),
                        os.path.basename(file.name).split('.')[0] + ".pdf")
        p = subprocess.Popen([htmltopdf_filename, file.name, pdffilename],
                             startupinfo=startupinfo, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if testPrinting:
            print_command = [pdfview_filename, pdffilename]
        elif useLabelPrinter:
            print_command = [gsprint_filename, pdffilename, '-printer', '%s' % labelPrinterName]
        elif defaultPrinterName != "default":
            print_command = [gsprint_filename, pdffilename, '-printer', '%s' % defaultPrinterName]
        else:
            print_command = [gsprint_filename, pdffilename]
        
        #if useLabelPrinter and not testPrinting:
        #    print_jobs = True
        #    while print_jobs:
        #        phandle = win32print.OpenPrinter(labelPrinterName)
        #        print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
        #        win32print.ClosePrinter(phandle)
        #        if print_jobs:
        #            time.sleep(0.2)
        
        p = subprocess.Popen(print_command, 
                             startupinfo=startupinfo, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except:
        raise EnvironmentError(102, "Error printing file.")
    finally:
        try:
            os.remove(pdffilename)
            os.remove(file.name)
        except:
            pass

    return None


def viewText(text):
    startupinfo = subprocess.STARTUPINFO()
    #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        file = tempfile.NamedTemporaryFile (suffix=".txt", delete=False)
        file.write (text)
        file.close()
    except:
        raise EnvironmentError(101, "Error opening temporary file.")

    try:
        p = subprocess.Popen(["notepad.exe", file.name], 
                             startupinfo=startupinfo, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except:
        raise EnvironmentError(103, "Error viewing file.")
    finally:
        try:
            os.remove(file.name)
        except:
            pass


def printText(text):
    startupinfo = subprocess.STARTUPINFO()
    #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        file = tempfile.NamedTemporaryFile (suffix=".txt", delete=False)
        file.write (text)
        file.close()
    except:
        raise EnvironmentError(101, "Error opening temporary file.")

    try:
        p = subprocess.Popen(["notepad.exe /P", file.name], 
                             startupinfo=startupinfo, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except:
        raise EnvironmentError(102, "Error printing file.")
    finally:
        try:
            os.remove(file.name)
        except:
            pass           
