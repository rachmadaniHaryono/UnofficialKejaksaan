
# coding: utf-8

# In[360]:

from lxml import etree
import ssl
import urllib2

from bs4 import BeautifulSoup as bs

# download first page
def load_page(url):
    #join url and page
    # have to use ssl to fix this 
    # http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed-error
    context = ssl._create_unverified_context()
    response = urllib2.urlopen(url, context=context)
    html = response.read()
    soup = bs(html)    
    return soup

def remove_double_whitespace(text):
    return '\n'.join(' '.join(line.split()) for line in text.split('\n'))

def convert_htmltable_to_dict(table_body):
    # http://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
    rows = table_body.find_all('tr')
    data = []
    for i_row, row in enumerate(rows):
        cols = row.find_all('td')
        parsed_cols = []
        for i_ele, ele in enumerate(cols) :
            # get links on row >= 2and last column
            if (i_ele == len(cols)-1) and i_row > 1:
                parsed_cols.append(ele.find('a').get('href'))               
            else :
                parsed_cols.append(remove_double_whitespace(ele.text.strip()))
        data.append(parsed_cols) 
    return data

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_table(tags_soup):
    # return table_soup
    pass
    
#class PageLoader(object):
    
def parse_html(page_soup):
    # find table
    page_soup.find
    pass

class PageLoadError(Exception):
    """Error when loading page"""

# berkas 
class Berkas(object):
    base_url = 'https://www.kejaksaan.go.id'
    
    def __init__(self, data):
        self.nomor_urut = data[0]
        self.nomor_perkara = data[1]
        self.nama_terdakwa = data[2] # parse the alias
        self.tanggal_dakwaan = data[3] # convert to python date
        self.wilayah_hukum = data[4] 
        self.detail_link = data[5]

        self.url = self.base_url + self.detail_link

    def convert_htmltable_to_dict(self, table_body):
        # http://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
        rows = table_body.find_all('tr')
        data = []
        for i_row, row in enumerate(rows):
            cols = row.find_all('td')
            parsed_cols = []
            for i_ele, ele in enumerate(cols) :
                parsed_cols.append(remove_double_whitespace(ele.text.strip()))
            data.append(parsed_cols) 
        return data

    def load_page(self):
        self.page_html = load_page(self.url)
        
    def load_detail(self):
        self.load_page()
        cell = filter(lambda x : 'Nomor Perkara' in x.text, self.page_html.find_all('td'))
        table = cell[2].parent.parent
        self.table_dict = self.convert_htmltable_to_dict(table)
        #return detail_data # instance dict, contain details
        
class Pidana(object):
    base_url = 'https://www.kejaksaan.go.id'
    api_url = '/berkas-dakwaan.php?'
    
    def __init__(self):
        self.max_page = None
        self.total_berkas = None
    
    def load_page(self, page_num=None):
        self.daftar_berkas = []
        
        url = self.base_url + self.api_url + self.api_attribute
        url_template = url + "&hal=%s"
        
        if page_num == 1:
            url_dest = url_template % str(1)
            self.parse_page( url_dest)
        elif page_num == None:
            url_dest = url_template % str(1)
            self.parse_page(url_dest)
            
            # dont parse all page if no max page defined
            if self.max_page is None:
                for x in range(2, self.max_page):
                    url_dest = url_template % str(x)
                    self.parse_page(url_dest)
            else:
                raise LoadPageError
        else :
            url_dest = url_template % str(page_num)
            self.parse_page(url_dest)
        # TODO raise error when page not found
            
    def parse_page(self, url):
        page_html = load_page(url)
        
        # parse table
        filter_result = filter(lambda x:"Total Data Berkas" in x.text, phtml.find_all('td'))
        table = filter_result[1].parent.parent
        dict_result = convert_htmltable_to_dict(table)
        
        # find total_berkas
        if self.total_berkas is None:
            self.total_berkas = int(find_between(dict_result[0][0],':','perkara').strip())
        
        # find max_page
        if self.max_page is None:
            last_page_url = filter(lambda x:">>" in x.text, phtml.find_all('a',{'class':'mn2'}))
            self.max_page = find_between(last_page_url[0].get('href'),'hal=','&')            
        
        for y,x in enumerate(dict_result):
            if y>1 : # ignore the first two row
                self.daftar_berkas.append(Berkas(x)) 

class PidanaUmum(Pidana):
    api_attribute = 'unt=1'

    def __ini__(self):
        super(PidanaUmum, self).__init__()

class PidanaKhusus(Pidana):
    api_attribute = 'unt=2'
    
    def __ini__(self):
        super(PidanaKhusus, self).__init__()