import pytest
import emberfactory
import re
import os
import json
"""
Early and basic implementation of Flask app testing
---------------------------------------------------
The purpose of this file is to help development. ** It is not intended to help new users testing the app **

The main aim is to produce the .pdf from a set of test .xlsx files (i.e. the test is more input related than 
code-functionality related, although doing some more testing of code functionality is possible)
"""

cfgfile = "../instance/test_emberfactory.json"
if os.path.exists(cfgfile):
    # You may insert your specific paths here
    with open(cfgfile) as json_data_file:
        cfg = json.load(json_data_file)
else:
    cfg = {}


@pytest.fixture
def client():
    app = emberfactory.create_app()
    app.config['TESTING'] = True  # Probably not used so far, at least, not explicitly used in EF's code
    with app.test_client() as client:
        yield client  # (from flask tuto, but not sure that it is useful here: only one client anyway so purpose?)
    # Any operation to be done after tests would take place here


def test_documentation(client):
    rv = client.post('/doc/tutorial')
    assert b'starting point to learn' in rv.data, "Having trouble displaying the tutorial ?!"
    rv = client.post('/doc/parameters')
    assert b'This page documents parameters' in rv.data, "Having trouble displaying the parameters' reference ?!"


def test_file_processing(client):
    # Upload and process all files from a test directory (you may add your own in the config file, see above)
    if "testdirs" in cfg:
        testdirs = cfg["testdirs"]
    else:
        testdirs = [os.path.join(os.path.dirname(emberfactory.__file__), "doc/examples")]
    # Tests below do not intent in succeeding or failing but rather in issuing warnings. However,
    # all my attempts at writing warnings directly to stdout or using warnings.warn() with a hook
    # had the same strange result that it would continue the last line of test reports from pytest / assess statements,
    # hence this poor solution of ending a line (which we do not know why it was not ended yet) with a print():
    print("\n")
    testfiles = []
    for adir in testdirs:
        for afile in os.listdir(adir):
            if os.path.splitext(afile)[-1] == '.xlsx' \
                    and os.path.splitext(afile)[0] != "colors" and os.path.splitext(afile)[0][0] != '~':
                testfiles.append(os.path.join(adir, afile))

    outdir = 'instance/out/test/'
    try:
        for f in os.listdir(outdir):
            os.remove(os.path.join(outdir, f))
    except OSError:
        try:
            os.makedirs(outdir)
        except OSError:
            print("Could not get a clean out/test directory.")

    for filename in testfiles:
        # Submit file for processing
        print (filename)
        rv = client.post('/process', data=dict(
            file=(open(filename, 'rb'), filename),
            csys="standard",
            delfile=1
        ), follow_redirects=True)
        assert b'To download' in rv.data, f"File wasn't successfully processed: {filename}"
        if b"Warning messages" in rv.data:
            print(f"Warnings for: {filename}")
            print("\t", re.findall(r'class="error">(.*?)</p>', str(rv.data)))

        # Download the result to the out/test folder.
        if b"To download" in rv.data:
            producedfiles = re.findall(r'/out/(.+?)"', str(rv.data))
            testfile = [file for file in producedfiles if ".svg" in file][0]
            rv = client.post('/out/'+testfile)
            with open(outdir+testfile, 'w+b') as fout:
                fout.write(rv.data)
                fout.close()

            testfile = [file for file in producedfiles if ".pdf" in file][0]
            rv = client.post('/out/'+testfile)
            with open(outdir+testfile, 'w+b') as fout:
                fout.write(rv.data)
                fout.close()

