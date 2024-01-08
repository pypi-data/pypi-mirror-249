#! /bin/env python3
import argparse
import os

from pdf_client_wrapper import client

def _parse_args():
    parser = argparse.ArgumentParser(prog='passer_template_server', description='模板开发工具')

    parser.add_argument('address', help= '远程渲染容器的地址, eg: 192.168.1.218:50055')
    parser.add_argument('resources', help= '资源文件夹地址, eg: test-data/abdomen_fatty3')
    parser.add_argument('pdf_path', help= '生成报告的地址，默认在资源文件夹下生成, eg: .')
    return parser.parse_args()

def _main():
    args = _parse_args()
    address = args.address
    resources_dir = args.resources
    pdf_path = args.pdf_path
    if not os.path.exists(resources_dir):
        raise FileNotFoundError(f'文件夹{resources_dir}不存在')
    ip_port = address.split(':')
    if len(ip_port) != 2:
        raise RuntimeError(f'[{address}]不是合法的地址')
    ip = ip_port[0]
    port = ip_port[1]

    cli = client.PdfClient(ip, port)
    try:
        cli.say_hello()
    except Exception:
        raise RuntimeError(f'pdf渲染容器[{address}]不可访问')
    cli._pts_render(resources_dir, pdf_path)


if __name__ == '__main__':
    _main()