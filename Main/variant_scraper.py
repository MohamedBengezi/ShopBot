import csv
import json
from urllib.request import urlopen
import sys


prodDict = {}
variantDict = {}


def get_page(page, url):
    url = url + '/products.json'
    data = urlopen(url + '?page={}'.format(page)).read()
    try:
        products = json.loads(data)['products']
    except:
        products = json.loads(data)['product']['variants']
    return products


def make_product_dict(url):
    page = 1
    products = get_page(page, url)
    while products:
        for product in products:
            name = product['title']
            product_url = url + '/products/' + product['handle']
            category = product['product_type']
            for variant in product['variants']:
                variant_names = []
                for i in range(1, 4):
                    k = 'option{}'.format(i)
                    if variant.get(k) and variant.get(k) != 'Default Title':
                        variant_names.append(variant[k])
                variant_name = ' '.join(variant_names)
                price = variant['price']
                row = [category, name + variant_name,
                       variant_name, price, product_url]
                row = [c.encode('utf8') for c in row]
                tmp = name
                name = name + variant_name.split(' ')[0]
                prodDict.update(
                    {name: {"Variant": variant_name, "url": product_url}})

                if name not in prodDict:
                    prodDict.update(
                        {name: {"Variant": variant_name, "url": product_url}})

                name = tmp
        page += 1
        products = get_page(page, url)

    return prodDict


# ['product']['options']['values']


def make_variant_dict(url):
    page = 1
    product = get_page(page, url)
    for var in product:
        if var['option2'] is not None:
            variant = var['option2']
        if var['option3'] is not None:
            variant = var['option2']
        id = var['id']
        print("CCCCC", variant, id, "\n")
        if variant:
            variantDict.update({variant: id})

    return variantDict
