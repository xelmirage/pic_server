import SimpleHTTPServer
import SocketServer
import os,sys,urllib
import json
from PIL import Image
import random
PORT = 8002


class myhandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server): 
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self,request, client_address, server)
    def generate_html(self,pic_path):
        list_images=os.listdir(pic_path)

        head_file=open('head.txt','r')
        back_file=open('back.txt','r')
        head_list=head_file.readlines()
        back_list=back_file.readlines()

        
        html_file=open(pic_path+'0pictures.html','w')
        html_file.writelines(head_list)
        html_file.write("var selfpath=\""+pic_path+"\";")

        html_file.writelines(back_list)    
        html_file.close()
        return
    def cp_html(self,pic_path):
        list_images=os.listdir(pic_path)

        head_file=open('w.html','r')
        
        head_list=head_file.readlines()
        

        
        html_file=open(pic_path+'0pictures.html','w')
        html_file.writelines(head_list)
        

        
        html_file.close()
        return
    def generate_json(self,page,path):
        batch=5
        class picfile:
            def __init__(self,preview,width,height):
                self.preview=preview
                self.width=width
                self.height=height
            def __repr__(self):    
                return repr((self.preview, self.width, self.height)) 
    
    
        json_list=[]
        current_dir=os.getcwd()+path
        file_list=os.listdir(current_dir)
        file_list.sort()
        if len(file_list)>500:
            random.shuffle(file_list)
        file_list=file_list[page*batch:(page+1)*batch]
        for f in file_list:
            ext=os.path.splitext(f)[1]
            if ext in ['.jpg','.jpeg','.png','.gif']:
                file_path=current_dir+'/'+f
                
                im = Image.open(file_path)
                width, height=im.size
                json_list.append(picfile(path+'/'+f,width, height))
        print json_list
        json_str = json.dumps(json_list,default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json_str
        
    def do_GET(self):
        
        path_list=self.path.split('?')
        if len(path_list)>1:
            print self.path
            para=path_list[len(path_list)-1]
            para_list=para.split("=")
            if para_list[0]=="page":
                page=int(para_list[1])
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            img_dir=urllib.unquote(self.path).split('?')[0][:-4]
            json_str=self.generate_json(page,img_dir)
            
            self.wfile.write(json_str)
            return
        current_dir=os.getcwd()+urllib.unquote(self.path)
        if os.path.isdir(current_dir[:-1]):
            f_list=os.listdir(current_dir)
            for f in f_list:
                current_file=current_dir+f
                if not os.path.isdir(current_file):
                    ext=os.path.splitext(f)[1]
                    if ext in ['.jpg','.jpeg','.png','.gif']:
                        self.cp_html(urllib.unquote(self.path)[1:])
                        
                        break
                
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)





Handler = myhandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
