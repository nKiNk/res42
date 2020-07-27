import re
'''Brother Python EscP Command Library
Description:
A collection of functions to more easily facilitate printing to the Brother QL label
printers without having to memorize the ESC/P commands. Also handles sending to sockets
for you.
'''


class BrotherPrint:
    
    font_types = {'bitmap': 0,
                  'outline': 1}
    
    def __init__(self, fsocket):
        self.fsocket = fsocket
        self.fonttype = self.font_types['bitmap']
    
    ###########################################################################
    # System Commands & Settings
    ###########################################################################
  
    def template_mode(self):
        self.send(chr(27)+'i'+'a'+'3')
    
    def initialize(self):
        self.fonttype = self.font_types['bitmap']
        self.send(chr(27)+chr(64))
  
    ############################################################################
    # Print Operations
    ############################################################################
    def send(self, text):
        '''Sends text to printer
        
        Args:
            text: string to be printed
        Returns:
            None
        Raises:
            None'''
        self.fsocket.send(text.encode())
        
    ###########################################################################
    # Text Operations
    ###########################################################################
        
    def select_font(self, font):
        '''Select font type
        
        Choices are: 
        <Bit map fonts>
        'brougham'
        'lettergothicbold'
        'brusselsbit'
        'helsinkibit'
        'sandiego'
        <Outline fonts>
        'lettergothic'
        'brusselsoutline'
        'helsinkioutline'
        
        Args:
            font: font type
        Returns:
            None
        Raises:
            RuntimeError: Invalid font.
        '''
        fonts = {'brougham': 0, 
                 'lettergothicbold': 1, 
                 'brusselsbit' : 2, 
                 'helsinkibit': 3, 
                 'sandiego': 4, 
                 'lettergothic': 9,
                 'brusselsoutline': 10, 
                 'helsinkioutline': 11}
        
        if font in fonts:
            if font in ['broughham', 'lettergothicbold', 'brusselsbit', 'helsinkibit', 'sandiego']:
                self.fonttype = self.font_types['bitmap']
            else:
                self.fonttype = self.font_types['outline']
                
            self.send(chr(27)+'k'+chr(fonts[font]))
        else:
            raise RuntimeError('Invalid font in function selectFont')
        
       
    ############################################################################
    # Template Commands
    ############################################################################
    
    def template_print(self):
        '''Print the page
        '''
        self.send('^FF')
    
    def choose_template(self, template):
        '''Choose a template
        '''
        n1 = int(template/10)
        n2 = int(template)%10
        self.send('^TS'+'0'+str(n1)+str(n2))
        
    def machine_op(self, operation):
        '''Perform machine operations
        '''
        operations = {'feed2start': 1,
                      'feedone': 2,
                      'cut': 3
                      }
        
        if operation in operations:
            self.send('^'+'O'+'P'+chr(operations[operation]))
        else:
            raise RuntimeError('Invalid operation.')
            
    def template_init(self):
        '''Initialize command for template mode
        '''
        self.send(chr(94)+chr(73)+chr(73))
        
    def print_start_command(self, command):
        '''Set print command
        
        Args:
            command: the type of command you desire.
        Returns:
            None
        Raises:
            RuntimeError: Command too long.
        '''
        size = len(command)
        if size > 20:
            raise RuntimeError('Command too long')
        n1 = int(size/10)
        n2 = size%10
        self.send('^PS'+chr(n1)+chr(n2)+command)
    
    def select_obj(self, name):
        '''Select an object
        
        Args:
            name: the name of the object you want to select
        Returns:
            None
        Raises:
            None
        '''
        self.send('^ON'+name+chr(0))
    
    def insert_into_obj(self, data):
        '''Insert text into selected object.
        
        Args:
            data: vThe data you want to insert.
        Returns:
            None
        Raises:
            None
        '''
        if not data:
            data = ''
        size = len(data)
        n1 = size%256
        n2 = int(size/256)
        print('^DI'+chr(n1)+chr(n2)+data)    
        self.send('^DI'+chr(n1)+chr(n2)+data)
    
    def select_and_insert(self, name, data):
        '''Combines selection and data insertion into one function
        
        Args:
            name: the name of the object you want to insert into
            data: the data you want to insert
        Returns:
            None
        Raises:
            None
        '''
        self.select_obj(name)
        self.insert_into_obj(data)
    
    