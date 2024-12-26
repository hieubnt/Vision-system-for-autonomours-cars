from product.src.pub_sub import Publisher

class Pipeline(Publisher):
    published_topics = ['pipeline_output']
    publisher_name = 'pipeline'

