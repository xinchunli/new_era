# coding:utf-8

__author__ = 'xinchun.li'


from service import hierarchy_service


if __name__ == '__main__':
    node = hierarchy_service.load_from_file()
    print node

    hierarchy_service.save_to_db(node)

