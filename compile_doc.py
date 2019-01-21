import re
import os
import tempfile as tf

# quick function to santize and standardize inputs
def clean_input( inp ):    
    inp = str(inp).strip().lower().title()
    return inp
    
def compile_pdf(name, streetAdd1, streetAdd2, city, state, zipcode, amtOwed, explanation):
    # establish directory context and set relevant directories
    projectDir = os.path.realpath( os.curdir )
    pdfDir = os.path.join(projectDir, 'pdfs')
    buildDir =  os.path.join(projectDir, '.build')
    srcDir = os.path.join(buildDir,'src')
    tmpDir = os.path.join(buildDir,'tmp')
    tf.tempdir = tmpDir
    
    # compile arguments into template input
    field_ents = { 'name' : name,
                   'streetAdd1' : streetAdd1,
                   'streetAdd2' : streetAdd2,
                   'city' : city,
                   'state' : state,
                   'zip' : zipcode,
                   'amtOwed' : amtOwed,
                   'explanation' : explanation
    }

    for key in field_ents:
        if key=='state':
            assert len( field_ents[key] ) == 2
            field_ents[key] = field_ents[key].upper()

        elif key=='explanation':
            pass
            
        else:
            field_ents[key] = clean_input( field_ents[key] )
            
    # load and fill template
    tex_code = open( os.path.join(srcDir,'template' ) ).read()
    tex_code = tex_code.format( **field_ents )
    
    # create a temp directory for pdflatex to compile PDF
    with tf.TemporaryDirectory() as td:
        # temp file to store TeX
        outFile = td+'/{}{}.tex'.format( name.replace(' ', '').lower(), str(hash(tex_code)) )

        # output file for PDF
        outPDF = td+'/{}{}.pdf'.format( name.replace(' ', '').lower(), str(hash(tex_code)) )

        # write TeX
        f = open(outFile,'w+t')
        f.writelines( tex_code )
        f.close()
        
        # compile PDF
        os.system('pdflatex -output-directory {} {} > /dev/null 2>&1'.format( td, outFile ) )
        pdfContent = open( outPDF, 'rb' ).close()
        os.system('mv {} {}'.format( outPDF, pdfDir))
        
    return pdfContent

import time as t
start = t.time()
compile_pdf("Peter Shaffery",
            "2050 Athens St",
            "Apt D",
            "Boulder",
            "CO",
            "80302",
            "6000",
            "3 months of missed paychecks for TA duties.  Employed to teach Calculus III in the Dept of Applied Math."
)

print( t.time() - start )        
