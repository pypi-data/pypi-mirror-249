from kraken_datatype import kraken_datatype as kr
import datetime

def test_null_value():

    datatype = None
    data = None
    assert kr.validate(datatype, data) == None

    datatype = 'url'
    data = None
    assert kr.validate(datatype, data) == None

    datatype = None
    data = 'https://www.test.com'
    assert kr.validate(datatype, data) == None

    datatype = ''
    data = 'https://www.test.com'
    assert kr.validate(datatype, data) == None

    datatype = 'url'
    data = ''
    assert kr.validate(datatype, data) == None

def test_url():

    datatype = 'url'
    data = 'https://www.test.com'
    assert kr.validate(datatype, data) == True

    datatype = 'url'
    data = 'www.test.com'
    assert kr.validate(datatype, data) == False

    datatype = 'url'
    data = 'test.com'
    assert kr.validate(datatype, data) == False

def test_date():

    datatype = 'date'
    data = '28/8/78'
    assert kr.normalize(datatype, data) == datetime.datetime(1978, 8, 28)

def test_address():

    data = {
        'streetAddress': '111 Sherbrooke St.',
        'addressLocality': 'Montréal',
        'addressRegion': 'Québec',
        'addressCountry': 'Canada',
        'postalCode': "G1G 1M2"
    }

    expected_result = {
        'streetAddress': '111 SHERBROOKE ST.',
        'addressLocality': 'MONTRÉAL',
        'addressRegion': 'QC',
        'addressCountry': 'CA',
        'postalCode': "G1G 1M2"
    }
    
    datatype = 'address'
    assert kr.normalize(datatype, data) == expected_result


    # 
    
    data = {
        'streetAddress': '111 Sherbrooke St.',
        'addressLocality': 'Montréal',
        'addressRegion': 'Quebec',
        'addressCountry': 'Canada',
        'postalCode': "G1G 1M2"
    }

    expected_result = {
        'streetAddress': '111 SHERBROOKE ST.',
        'addressLocality': 'MONTRÉAL',
        'addressRegion': 'QC',
        'addressCountry': 'CA',
        'postalCode': "G1G 1M2"
    }

    datatype = 'address'
    assert kr.normalize(datatype, data) == expected_result

    # 
    data = {
        'streetAddress': '111 Sherbrooke St.',
        'addressLocality': 'Montréal',
        'addressRegion': 'QC',
        'addressCountry': 'Canada',
        'postalCode': "G1G 1M2"
    }

    expected_result = {
        'streetAddress': '111 SHERBROOKE ST.',
        'addressLocality': 'MONTRÉAL',
        'addressRegion': 'QC',
        'addressCountry': 'CA',
        'postalCode': "G1G 1M2"
    }

    datatype = 'address'
    assert kr.normalize(datatype, data) == expected_result


    # 
    data = {
        'streetAddress': '111 Sherbrooke St.',
        'addressLocality': 'Montréal',
        'addressRegion': 'QC',
        'addressCountry': 'Canada',
        'postalCode': "G1G1M2"
    }
    
    expected_result = {
        'streetAddress': '111 SHERBROOKE ST.',
        'addressLocality': 'MONTRÉAL',
        'addressRegion': 'QC',
        'addressCountry': 'CA',
        'postalCode': "G1G 1M2"
    }
    
    datatype = 'address'
    assert kr.normalize(datatype, data) == expected_result