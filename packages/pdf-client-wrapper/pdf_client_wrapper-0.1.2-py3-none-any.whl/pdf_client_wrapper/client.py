"""
Author: Daryl.Xu
E-mail: xuziqiang@zyheal.com
"""
import grpc
import os
import time
import json
import shutil

from pdf_client_wrapper.rpc import pdf_pb2, pdf_pb2_grpc, xy_units_pb2, xy_units_pb2_grpc
from pdf_client_wrapper import utils


class PdfClient:
    def __init__(self, host="127.0.0.1", port=50052):
        self.host = host
        self.port = port

        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = pdf_pb2_grpc.PdfStub(self.channel)

    def say_hello(self):
        with grpc.insecure_channel(f'{self.host}:{self.port}') as channel:
            stub = xy_units_pb2_grpc.ReportsGeneratorStub(channel)
            request = xy_units_pb2.HelloRequest(Message="pdf-client-wrapper")
            respose = stub.SayHello(request)
            print(respose.Message)

    def upload_resource(self, zip_path: str) -> str:
        """
        the zip file needs to contain the following files:
        template.html, written in jinjia2 syntax
        resources files used by the template.html, by relative reference
        zip文件需要包含如下文件：
        template.html, 使用jinjia2语法编写
        被tempalte.html引用的文件，相对引用

        Notice: 
        You can use font by this way, the font file will be prepared in advance
        @font-face {
            font-family: puhui-regular;
            src: url("fonts/Alibaba-PuHuiTi-Regular.ttf");
        }

        Upload the resource to the server
        :param path: path of the resource
        :return uid of the task
        """
        stream = utils.gen_stream(zip_path)
        reply = self.stub.uploadResource(stream)
        # TODO check the statusCode
        return reply.uid

    def render(self, uid: str, parameters: str):
        """
        Render the resources to PDF
        :param uid: uid of the task
        :param parameters: parameters fill into the template, JSON format
        """
        request = pdf_pb2.RenderRequest(uid=uid, parameters=parameters)
        reply = self.stub.render(request)

    def download(self, uid: str, target_pdf_path: str):
        """
        Download the PDF file of the given task
        :param uid: uid of the task
        :param target_pdf_path: target path of the PDF
        """
        request = pdf_pb2.DownloadRequest(uid=uid, filename='report.pdf')
        reply = self.stub.download(request)
        with open(target_pdf_path, 'wb') as f:
            for chunk in reply:
                f.write(chunk.content)

    def download_html(self, uid: str, target_html_path: str):
        """
        Download the PDF file of the given task
        :param uid: uid of the task
        :param target_pdf_path: target path of the PDF
        """
        request = pdf_pb2.DownloadRequest(uid=uid, filename='report.html')
        reply = self.stub.download(request)
        with open(target_html_path, 'wb') as f:
            for chunk in reply:
                f.write(chunk.content)

    def render_resources_to_pdf(self, zip_path: str, target_pdf_path: str,
                                target_html_path: str, parameters: str):
        uid = self.upload_resource(zip_path)
        self.render(uid, parameters)
        self.download(uid, target_pdf_path)
        self.download_html(uid, target_html_path)

    def close(self):
        self.channel.close()



    def _pts_render(self, resources_dir: str, pdf_path:str= '.'):
        '''
        实现`pts_render`脚本
        '''
        tmp_dir = os.path.join(resources_dir, 'cache')

        def tp(name: str):
            # Template path
            return os.path.join(resources_dir, name)

        def rrp(name: str):
            # Report resource path
            return os.path.join(tmp_dir, 'resources', name)
        
        if pdf_path == '.':
            pdf_path = os.path.join(resources_dir, 'report.pdf')
        
        img_dir = os.path.join(resources_dir, 'src', 'files', 'img')
        parameters_path = os.path.join(resources_dir, 'parameters-zyheal.json')
        
        with open(parameters_path, 'r', encoding='utf-8') as f:
            parameters = json.load(f)
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        shutil.copytree(img_dir, rrp('files/img'))
        shutil.copytree(tp('src/assets'), rrp('assets'))
        shutil.copytree(tp('src/js'), rrp('js'))
        shutil.copyfile(tp('src/template.html'), rrp('template.html'))
        shutil.copyfile(tp('src/style.css'), rrp('style.css'))
        # src/public文件夹可能是软连接
        if os.path.exists(tp('src/public')):
            shutil.copytree(tp('src/public'), rrp('public'), symlinks= True)

        resources_zip = utils.zip_folder(tmp_dir+'/resources')
        print(f'资源文件打包完成：{resources_zip}')

        t0 = time.time()
        print("pdf渲染开始.....")
        try:
            self.render_resources_to_pdf(resources_zip, pdf_path, rrp('report.html'), json.dumps(parameters))
            shutil.rmtree(tmp_dir) # 删除缓存目录
        except Exception as e1:
            raise RuntimeError(f'pdf渲染失败: {e1}')

        t1 = time.time()
        print(f"pdf渲染完成, 用时:{t1-t0:.2f}s, 保存位置:{pdf_path}")


    def remote_render(self, parameters: dict, img_dir: str, tmp_dir: str, report_path: str, template_dir: str):
        '''
        用于pipeline中渲染报告pdf
        '''
        print("测试pdf渲染容器的连通性.....")
        try:
            self.say_hello()
            print("[√]pdf渲染容器可以访问")
        except Exception:
            raise RuntimeError(f'[X]pdf渲染容器[{self.host}:{self.port}]不可访问')
        
        def tp(name: str):
            # Template path
            return os.path.join(template_dir, name)
        def rrp(name: str):
            # Report resource path
            return os.path.join(tmp_dir, 'resources', name)
        os.makedirs(tmp_dir, exist_ok=True)
        shutil.copytree(img_dir, rrp('files/img'), symlinks= True, dirs_exist_ok= True)
        shutil.copytree(tp('src/public'), rrp('public'), symlinks= True, dirs_exist_ok= True)
        shutil.copytree(tp('src/assets'), rrp('assets'), dirs_exist_ok= True)
        if os.path.exists(tp('src/js')):
            shutil.copytree(tp('src/js'), rrp('js'), dirs_exist_ok= True)
        shutil.copy2(tp('src/template.html'), rrp('template.html'))
        shutil.copy2(tp('src/style.css'), rrp('style.css'))
        resources_zip = rrp('../resources.zip')
        print(f'资源文件打包完成：{resources_zip}')
        utils.zip_dir(rrp('.'), resources_zip)
        # 报告资源打包完毕
        t0 = time.time()
        print("pdf渲染开始.....")
        self.render_resources_to_pdf(resources_zip, report_path, rrp('report.html'), json.dumps(parameters))
        t1 = time.time()
        print(f"pdf渲染完成, 用时:{t1-t0:.2f}s, 保存位置:{report_path}")


if __name__ == "__main__":
    client = PdfClient(host="127.0.0.1", port=50053)
    client.say_hello()
    zip_path = "/home/ziqiang_xu/zy/middle-platform/pdf/pdf-server/workplace/test-dir/test.zip"
    target_pdf_path = "/home/ziqiang_xu/zy/middle-platform/pdf/pdf-server/workplace/test-dir/"\
                      "client-test.pdf"
    target_html_path = "/home/ziqiang_xu/zy/middle-platform/pdf/pdf-server/workplace/test-dir/"\
        "client-test.html"
    client.render_resources_to_pdf(zip_path, target_pdf_path,
                                   target_html_path, '{"k1": "v1"}')
