import scrapy
import os


class BolosSpider(scrapy.Spider):
    name = "bolos"

    def start_requests(self):
        urls = [
            'http://www.tudogostoso.com.br/categorias/1000-bolos-e-tortas-doces-1.html',
            'http://www.tudogostoso.com.br/categorias/1004-carnes-1.html',
            'http://www.tudogostoso.com.br/categorias/1009-aves-1.html',
            'http://www.tudogostoso.com.br/categorias/1014-peixes-e-frutos-do-mar-1.html',
            'http://www.tudogostoso.com.br/categorias/1023-saladas-molhos-e-acompanhamentos-1.html',
            'http://www.tudogostoso.com.br/categorias/1027-sopas-1.html',
            'http://www.tudogostoso.com.br/categorias/1028-massas-1.html',
            'http://www.tudogostoso.com.br/categorias/1032-bebidas-1.html',
            'http://www.tudogostoso.com.br/categorias/1037-doces-e-sobremesas-1.html',
            'http://www.tudogostoso.com.br/categorias/1044-lanches-1.html',
            'http://www.tudogostoso.com.br/categorias/1334-alimentacao-saudavel-1.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_page(self, response):

        titulo = response.css('div.recipe-title')
        ingredientes = response.css('span.p-ingredient::text')
        a = titulo.css('h1::text').extract_first()
        b = ingredientes.extract()
        path = '/home/caio/Dropbox/%ESTUDO/pythoncrawler/tutorial/results/'
        filename = '%s.json' % a
        filename = os.path.join(path, filename)
        with open(filename, 'wb') as f:
            f.write(str({'titulo': a, 'ingredientes': b}))

        yield {'titulo': a, 'ingredientes': b}

    def parse(self, response):
        for pag in response.css('li.box-hover'):
            mid_page = pag.css('a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(mid_page), callback=self.parse_page)


        for link in response.css('div.holder'):
            next_page = link.css('a.next::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)