import pandas as pd
import requests


# Lista de locations de la M6Toll alrededor de Birmingham
locations = [
    {'Highway' : 'M6Toll', 'Id': '9228', 'Site' : '7671/1' },
    {'Highway' : 'M6Toll', 'Id': '9229', 'Site' : '7671/2' },
    {'Highway' : 'M6Toll', 'Id': '9230', 'Site' : '7672/1' },
    {'Highway' : 'M6Toll', 'Id': '9231', 'Site' : '7672/2' },
    {'Highway' : 'M6Toll', 'Id': '9232', 'Site' : '7673/1' },
    {'Highway' : 'M6Toll', 'Id': '9233', 'Site' : '7673/2' },
    {'Highway' : 'M6Toll', 'Id': '9234', 'Site' : '7674/1' },
    {'Highway' : 'M6Toll', 'Id': '9235', 'Site' : '7674/2' },
    {'Highway' : 'M6Toll', 'Id': '9236', 'Site' : '7675/1' },
    {'Highway' : 'M6Toll', 'Id': '9237', 'Site' : '7675/2' },
    {'Highway' : 'M6Toll', 'Id': '9238', 'Site' : '7676/1' },
    {'Highway' : 'M6Toll', 'Id': '9239', 'Site' : '7676/2' },
    {'Highway' : 'M6Toll', 'Id': '9240', 'Site' : '7677/1' },
    {'Highway' : 'M6Toll', 'Id': '9241', 'Site' : '7678/1' },
    {'Highway' : 'M6Toll', 'Id': '9242', 'Site' : '7678/2' },
    {'Highway' : 'M6Toll', 'Id': '9243', 'Site' : '7679/1' },
    {'Highway' : 'M6Toll', 'Id': '9244', 'Site' : '7679/2' },
    {'Highway' : 'M6Toll', 'Id': '9245', 'Site' : '7680/1' },
    {'Highway' : 'M6Toll', 'Id': '9246', 'Site' : '7680/2' },
    {'Highway' : 'M6Toll', 'Id': '9247', 'Site' : '7681/1' },
    {'Highway' : 'M6Toll', 'Id': '9248', 'Site' : '7681/2' },
    {'Highway' : 'M6Toll', 'Id': '9249', 'Site' : '7682/1' },
    {'Highway' : 'M6Toll', 'Id': '9250', 'Site' : '7682/2' }    
]

# Lista de locationsde la M6 que pasa por dentro de Birmingham
locations2 = [
    {'Highway' : 'M6', 'Site' : 'M6/5686A' },
    {'Highway' : 'M6', 'Site' : 'M6/5686B' },
    {'Highway' : 'M6', 'Site' : 'M6/5689B' },
    {'Highway' : 'M6', 'Site' : 'M6/5690A' },
    {'Highway' : 'M6', 'Site' : 'M6/5692A' },
    {'Highway' : 'M6', 'Site' : 'M6/5697A' },
    {'Highway' : 'M6', 'Site' : 'M6/5697B' },
    {'Highway' : 'M6', 'Site' : 'M6/5697J' },
    {'Highway' : 'M6', 'Site' : 'M6/5701A' },
    {'Highway' : 'M6', 'Site' : 'M6/5701B' },
    {'Highway' : 'M6', 'Site' : 'M6/5707B' },
    {'Highway' : 'M6', 'Site' : 'M6/5711B' },
    {'Highway' : 'M6', 'Site' : 'M6/5711L' },
    {'Highway' : 'M6', 'Site' : 'M6/5712L' },
    {'Highway' : 'M6', 'Site' : 'M6/5713A' },
    {'Highway' : 'M6', 'Site' : 'M6/5716B' },
    {'Highway' : 'M6', 'Site' : 'M6/5717L' },
    {'Highway' : 'M6', 'Site' : 'M6/5718B' },
    {'Highway' : 'M6', 'Site' : 'M6/5718A' },
    {'Highway' : 'M6', 'Site' : 'M6/5719B' },
    {'Highway' : 'M6', 'Site' : 'M6/5726A' },
    {'Highway' : 'M6', 'Site' : 'M6/5728B' },
    {'Highway' : 'M6', 'Site' : 'M6/5730A' },
    {'Highway' : 'M6', 'Site' : 'M6/5732B' },
    {'Highway' : 'M6', 'Site' : 'M6/5722A' },
    {'Highway' : 'M6', 'Site' : 'M6/5722B' },
    {'Highway' : 'M6', 'Site' : 'M6/5733A' },
    {'Highway' : 'M6', 'Site' : 'M6/5735B' },
    {'Highway' : 'M6', 'Site' : 'M6/5737A' },
    {'Highway' : 'M6', 'Site' : 'M6/5739B' },
    {'Highway' : 'M6', 'Site' : 'M6/5742A' },
    {'Highway' : 'M6', 'Site' : 'M6/5742B' },
    {'Highway' : 'M6', 'Site' : 'M6/5745B' },
    {'Highway' : 'M6', 'Site' : 'M6/5746A' },
    {'Highway' : 'M6', 'Site' : 'M6/5748B' },
    {'Highway' : 'M6', 'Site' : 'M6/5749A' },
    {'Highway' : 'M6', 'Site' : 'M6/5751L' },
    {'Highway' : 'M6', 'Site' : 'M6/5751B' },
    {'Highway' : 'M6', 'Site' : 'M6/5750K' },
    {'Highway' : 'M6', 'Site' : 'M6/5752A' },
    {'Highway' : 'M6', 'Site' : 'M6/5754B' },
    {'Highway' : 'M6', 'Site' : 'M6/5754A' },
    {'Highway' : 'M6', 'Site' : 'M6/5754A' },
    {'Highway' : 'M6', 'Site' : 'M6/5757B' },
    {'Highway' : 'M6', 'Site' : 'M6/5757A' },
    {'Highway' : 'M6', 'Site' : 'M6/5760A' },
    {'Highway' : 'M6', 'Site' : 'M6/5761B' },
    {'Highway' : 'M6', 'Site' : 'M6/5757B' },
    {'Highway' : 'M6', 'Site' : 'M6/5763A' },
    {'Highway' : 'M6', 'Site' : 'M6/5764B' },
    {'Highway' : 'M6', 'Site' : 'M6/5765B' },
    {'Highway' : 'M6', 'Site' : 'M6/5769B' },
    {'Highway' : 'M6', 'Site' : 'M6/5769A' },
    {'Highway' : 'M6', 'Site' : 'M6/5772A' },
    {'Highway' : 'M6', 'Site' : 'M6/5774B' },
    {'Highway' : 'M6', 'Site' : 'M6/5775A' },
    {'Highway' : 'M6', 'Site' : 'M6/5778B' },
    {'Highway' : 'M6', 'Site' : 'M6/5778A' },
    {'Highway' : 'M6', 'Site' : 'M6/5781A' },
    {'Highway' : 'M6', 'Site' : 'M6/5782B' },
    {'Highway' : 'M6', 'Site' : 'M6/5783J' },
    {'Highway' : 'M6', 'Site' : 'M6/5784A' },
    {'Highway' : 'M6', 'Site' : 'M6/5784B' },
    {'Highway' : 'M6', 'Site' : 'M6/5788A' },
    {'Highway' : 'M6', 'Site' : 'M6/5788B' },
    {'Highway' : 'M6', 'Site' : 'M6/5791A' },
    {'Highway' : 'M6', 'Site' : 'M6/5791B' },
    {'Highway' : 'M6', 'Site' : 'M6/5795A' },
    {'Highway' : 'M6', 'Site' : 'M6/5795B' },
    {'Highway' : 'M6', 'Site' : 'M6/5798A' },
    {'Highway' : 'M6', 'Site' : 'M6/5798B' },
    {'Highway' : 'M6', 'Site' : 'M6/5804A' },
    {'Highway' : 'M6', 'Site' : 'M6/5804B' },
    {'Highway' : 'M6', 'Site' : 'M6/5807A' },
    {'Highway' : 'M6', 'Site' : 'M6/5807B' },
    {'Highway' : 'M6', 'Site' : 'M6/5810A' },
    {'Highway' : 'M6', 'Site' : 'M6/5810B' },
    {'Highway' : 'M6', 'Site' : 'M6/5813A' },
    {'Highway' : 'M6', 'Site' : 'M6/5813B' },
    {'Highway' : 'M6', 'Site' : 'M6/5819A' },
    {'Highway' : 'M6', 'Site' : 'M6/5819B' },
    {'Highway' : 'M6', 'Site' : 'M6/5822A' },
    {'Highway' : 'M6', 'Site' : 'M6/5822B' },
    {'Highway' : 'M6', 'Site' : 'M6/5826A' },
    {'Highway' : 'M6', 'Site' : 'M6/5826B' },
    {'Highway' : 'M6', 'Site' : 'M6/5831A' },
    {'Highway' : 'M6', 'Site' : 'M6/5829B' },
    {'Highway' : 'M6', 'Site' : 'M6/5832B' },
    {'Highway' : 'M6', 'Site' : 'M6/5834J' },
    {'Highway' : 'M6', 'Site' : 'M6/5834A' },
    {'Highway' : 'M6', 'Site' : 'M6/5834M' },
    {'Highway' : 'M6', 'Site' : 'M6/5835B' },
    {'Highway' : 'M6', 'Site' : 'M6/5839K' },
    {'Highway' : 'M6', 'Site' : 'M6/5838B' },
    {'Highway' : 'M6', 'Site' : 'M6/5838A' },
    {'Highway' : 'M6', 'Site' : 'M6/5839L' },
    {'Highway' : 'M6', 'Site' : 'M6/5841A' },
    {'Highway' : 'M6', 'Site' : 'M6/5841B' },
    {'Highway' : 'M6', 'Site' : 'M6/5845A' },
    {'Highway' : 'M6', 'Site' : 'M6/5845B' },
    {'Highway' : 'M6', 'Site' : 'M6/5848B' },
    {'Highway' : 'M6', 'Site' : 'M6/5848A' },
    {'Highway' : 'M6', 'Site' : 'M6/5851B' },
    {'Highway' : 'M6', 'Site' : 'M6/5851A' },
    {'Highway' : 'M6', 'Site' : 'M6/5854B' },
    {'Highway' : 'M6', 'Site' : 'M6/5854A' },
    {'Highway' : 'M6', 'Site' : 'M6/5857B' },
    {'Highway' : 'M6', 'Site' : 'M6/5857A' },
    {'Highway' : 'M6', 'Site' : 'M6/5860B' },
    {'Highway' : 'M6', 'Site' : 'M6/5860A' },
    {'Highway' : 'M6', 'Site' : 'M6/5865B' },
    {'Highway' : 'M6', 'Site' : 'M6/5865A' },
    {'Highway' : 'M6', 'Site' : 'M6/5868B' },
    {'Highway' : 'M6', 'Site' : 'M6/5868A' },
    {'Highway' : 'M6', 'Site' : 'M6/5870B' },
    {'Highway' : 'M6', 'Site' : 'M6/5870A' },
    {'Highway' : 'M6', 'Site' : 'M6/5873B' },
    {'Highway' : 'M6', 'Site' : 'M6/5873A' },
    {'Highway' : 'M6', 'Site' : 'M6/5880B' },
    {'Highway' : 'M6', 'Site' : 'M6/5880A' },
    {'Highway' : 'M6', 'Site' : 'M6/5884B' },
    {'Highway' : 'M6', 'Site' : 'M6/5884A' },
    {'Highway' : 'M6', 'Site' : 'M6/5887B' },
    {'Highway' : 'M6', 'Site' : 'M6/5887A' },
    {'Highway' : 'M6', 'Site' : 'M6/5891A' },
    {'Highway' : 'M6', 'Site' : 'M6/5892B' },
    {'Highway' : 'M6', 'Site' : 'M6/5895B' },
    {'Highway' : 'M6', 'Site' : 'M6/5895A' },
    {'Highway' : 'M6', 'Site' : 'M6/5900B' },
    {'Highway' : 'M6', 'Site' : 'M6/5900A' },
    {'Highway' : 'M6', 'Site' : 'M6/5900M' },
    {'Highway' : 'M6', 'Site' : 'M6/5903A' },
    {'Highway' : 'M6', 'Site' : 'M6/5905L' },
    {'Highway' : 'M6', 'Site' : 'M6/5905K' },
    {'Highway' : 'M6', 'Site' : 'M6/5906B' },
    {'Highway' : 'M6', 'Site' : 'M6/5908A' },
    {'Highway' : 'M6', 'Site' : 'M6/5911B' },
    {'Highway' : 'M6', 'Site' : 'M6/5913A' },
    {'Highway' : 'M6', 'Site' : 'M6/5914M' },
    {'Highway' : 'M6', 'Site' : 'M6/5916B' },
    {'Highway' : 'M6', 'Site' : 'M6/5924A' },
    {'Highway' : 'M6', 'Site' : 'M6/5924B' },
    {'Highway' : 'M6', 'Site' : 'M6/5927A' },
    {'Highway' : 'M6', 'Site' : 'M6/5927B' },
    {'Highway' : 'M6', 'Site' : 'M6/5931A' },
    {'Highway' : 'M6', 'Site' : 'M6/5931B' },
    {'Highway' : 'M6', 'Site' : 'M6/5934A' },
    {'Highway' : 'M6', 'Site' : 'M6/5934B' },
    {'Highway' : 'M6', 'Site' : 'M6/5936K' },
    {'Highway' : 'M6', 'Site' : 'M6/5936L' },
    {'Highway' : 'M6', 'Site' : 'M6/5941B' },
    {'Highway' : 'M6', 'Site' : 'M6/5937B' },
    {'Highway' : 'M6', 'Site' : 'M6/5937A' },
    {'Highway' : 'M6', 'Site' : 'M6/5939L' },
    {'Highway' : 'M6', 'Site' : 'M6/5939B' },
    {'Highway' : 'M6', 'Site' : 'M6/5942A' },
    {'Highway' : 'M6', 'Site' : 'M6/5943B' },
    {'Highway' : 'M6', 'Site' : 'M6/5945A' },
    {'Highway' : 'M6', 'Site' : 'M6/5945B' },
    {'Highway' : 'M6', 'Site' : 'M6/5947A' },
    {'Highway' : 'M6', 'Site' : 'M6/5947B' },
    {'Highway' : 'M6', 'Site' : 'M6/5950A' },
    {'Highway' : 'M6', 'Site' : 'M6/5950B' },
    {'Highway' : 'M6', 'Site' : 'M6/5953A' },
    {'Highway' : 'M6', 'Site' : 'M6/5955M' },
    {'Highway' : 'M6', 'Site' : 'M6/5955J' },
    {'Highway' : 'M6', 'Site' : 'M6/5956A' },
    {'Highway' : 'M6', 'Site' : 'M6/5956B' },
    {'Highway' : 'M6', 'Site' : 'M6/5959L' },
    {'Highway' : 'M6', 'Site' : 'M6/5959K' },
    {'Highway' : 'M6', 'Site' : 'M6/5960B' },
    {'Highway' : 'M6', 'Site' : 'M6/5960A' },
    {'Highway' : 'M6', 'Site' : 'M6/5962B' },
    {'Highway' : 'M6', 'Site' : 'M6/5963A' },
    {'Highway' : 'M6', 'Site' : 'M6/5967A' },
    {'Highway' : 'M6', 'Site' : 'M6/5967B' },
    {'Highway' : 'M6', 'Site' : 'M6/5968B6'},
    {'Highway' : 'M6', 'Site' : 'M6/5968B5'},
    {'Highway' : 'M6', 'Site' : 'M6/5969B' },
    {'Highway' : 'M6', 'Site' : 'M6/5969A' },
    {'Highway' : 'M6', 'Site' : 'M6/5973B' },
    {'Highway' : 'M6', 'Site' : 'M6/5973A' },
    {'Highway' : 'M6', 'Site' : 'M6/5976A' },
    {'Highway' : 'M6', 'Site' : 'M6/5976B' },
    {'Highway' : 'M6', 'Site' : 'M6/5977J' },
    {'Highway' : 'M6', 'Site' : 'M6/5978M' },
    {'Highway' : 'M6', 'Site' : 'M6/5979A' },
    {'Highway' : 'M6', 'Site' : 'M6/5979B' },
    {'Highway' : 'M6', 'Site' : 'M6/5983A' },
    {'Highway' : 'M6', 'Site' : 'M6/5983B' },
    {'Highway' : 'M6', 'Site' : 'M6/5984L' },
    {'Highway' : 'M6', 'Site' : 'M6/5984K' },
    {'Highway' : 'M6', 'Site' : 'M6/5986B' },
    {'Highway' : 'M6', 'Site' : 'M6/5986A' },
    {'Highway' : 'M6', 'Site' : 'M6/5989B' },
    {'Highway' : 'M6', 'Site' : 'M6/5989A' },
    {'Highway' : 'M6', 'Site' : 'M6/5993B' },
    {'Highway' : 'M6', 'Site' : 'M6/5993A' },
    {'Highway' : 'M6', 'Site' : 'M6/5997B' },
    {'Highway' : 'M6', 'Site' : 'M6/5997A' },
    {'Highway' : 'M6', 'Site' : 'M6/6000B' },
    {'Highway' : 'M6', 'Site' : 'M6/6000A' },
    {'Highway' : 'M6', 'Site' : 'M6/6005B' },
    {'Highway' : 'M6', 'Site' : 'M6/6005A' },
    {'Highway' : 'M6', 'Site' : 'M6/6009B' },
    {'Highway' : 'M6', 'Site' : 'M6/6009A' },
    {'Highway' : 'M6', 'Site' : 'M6/6013B' },
    {'Highway' : 'M6', 'Site' : 'M6/6013A' },
    {'Highway' : 'M6', 'Site' : 'M6/6016B' },
    {'Highway' : 'M6', 'Site' : 'M6/6016A' },
    {'Highway' : 'M6', 'Site' : 'M6/6020B' },
    {'Highway' : 'M6', 'Site' : 'M6/6020A' },
    {'Highway' : 'M6', 'Site' : 'M6/6024B' },
    {'Highway' : 'M6', 'Site' : 'M6/6023A' },
    {'Highway' : 'M6', 'Site' : 'M6/6025A' },
    {'Highway' : 'M6', 'Site' : 'M6/6028A' },
    {'Highway' : 'M6', 'Site' : 'M6/6029B' },
    {'Highway' : 'M6', 'Site' : 'M6/6032A' },
    {'Highway' : 'M6', 'Site' : 'M6/6032B' },
    {'Highway' : 'M6', 'Site' : 'M6/6036A' },
    {'Highway' : 'M6', 'Site' : 'M6/6036J' },
    {'Highway' : 'M6', 'Site' : 'M6/6040B' },
    {'Highway' : 'M6', 'Site' : 'M6/6040A' },
    {'Highway' : 'M6', 'Site' : 'M6/6041M' },
    {'Highway' : 'M6', 'Site' : 'M6/6042A' },
    {'Highway' : 'M6', 'Site' : 'M6/6042J' },
    {'Highway' : 'M6', 'Site' : 'M6/6046B' },
    {'Highway' : 'M6', 'Site' : 'M6/6046A' },
    {'Highway' : 'M6', 'Site' : 'M6/6046L' },
    {'Highway' : 'M6', 'Site' : 'M6/6051J' },
    {'Highway' : 'M6', 'Site' : 'M6/6050B' },
    {'Highway' : 'M6', 'Site' : 'M6/6052A' },
    {'Highway' : 'M6', 'Site' : 'M6/6054B' },
    {'Highway' : 'M6', 'Site' : 'M6/6054A' },
    {'Highway' : 'M6', 'Site' : 'M6/6054B' },
    {'Highway' : 'M6', 'Site' : 'M6/6056L' },
    {'Highway' : 'M6', 'Site' : 'M6/6058A' },
    {'Highway' : 'M6', 'Site' : 'M6/6058B' },
    {'Highway' : 'M6', 'Site' : 'M6/6061A' },
    {'Highway' : 'M6', 'Site' : 'M6/6061B' },
    {'Highway' : 'M6', 'Site' : 'M6/6061L' },
    {'Highway' : 'M6', 'Site' : 'M6/6065A' },
    {'Highway' : 'M6', 'Site' : 'M6/6065J' },
    {'Highway' : 'M6', 'Site' : 'M6/6067B' },
    {'Highway' : 'M6', 'Site' : 'M6/6067A' },
    {'Highway' : 'M6', 'Site' : 'M6/6067B' },
    {'Highway' : 'M6', 'Site' : 'M6/6067M' },
    {'Highway' : 'M6', 'Site' : 'M6/6067J' },
    {'Highway' : 'M6', 'Site' : 'M6/6070A' },
    {'Highway' : 'M6', 'Site' : 'M6/6070B' },
    {'Highway' : 'M6', 'Site' : 'M6/6073A' },
    {'Highway' : 'M6', 'Site' : 'M6/6073K' },
    {'Highway' : 'M6', 'Site' : 'M6/6075L' },
    {'Highway' : 'M6', 'Site' : 'M6/6075B' },
    {'Highway' : 'M6', 'Site' : 'M6/6077A' },
    {'Highway' : 'M6', 'Site' : 'M6/6077K' },
    {'Highway' : 'M6', 'Site' : 'M6/6078L' },
    {'Highway' : 'M6', 'Site' : 'M6/6078B' },
    {'Highway' : 'M6', 'Site' : 'M6/6080A' },
    {'Highway' : 'M6', 'Site' : 'M6/6080K' },
    {'Highway' : 'M6', 'Site' : 'M6/6085A' },
    {'Highway' : 'M6', 'Site' : 'M6/6081B' },
    {'Highway' : 'M6', 'Site' : 'M6/6085K' },
    {'Highway' : 'M6', 'Site' : 'M6/6086B' }
]

# Lista de locations desde que se juntan la M6 y la M6Toll hacia el norte
locations3 = [
    {'Highway' : 'M6 North', 'Site' : 'M6/6089A' },
    {'Highway' : 'M6 North', 'Site' : 'M600/1516B'},
    {'Highway' : 'M6 North', 'Site' : 'M6/6092B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6093A' },
    {'Highway' : 'M6 North', 'Site' : 'M600/1520B'},
    {'Highway' : 'M6 North', 'Site' : 'M6/6098A' },
    {'Highway' : 'M6 North', 'Site' : 'M600/1525B'},
    {'Highway' : 'M6 North', 'Site' : 'M6/6101B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6101A' },
    {'Highway' : 'M6 North', 'Site' : 'M600/1530B'},
    {'Highway' : 'M6 North', 'Site' : 'M6/6105A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6106B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6108A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6112A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6112B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6111J' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6111M' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6116B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6118A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6119K' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6119B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6120L' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6122A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6122B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6125B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6126A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6129A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6129B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6133A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6134B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6138A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6138B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6144A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6142B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6149A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6147B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6153A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6150B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6153B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6158B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6158A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6164B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6164A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6170A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6170B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6174A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6175B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6179A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6179B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6182A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6183B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6185A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6187B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6189A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6189J' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6191B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6195A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6195B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6196J' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6196M' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6197A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6197B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6200A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6200B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6200K' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6201L' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6206A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6206B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6209A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6209B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6214A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6214B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6216B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6220A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6220B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6223A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6223B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6226A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6226B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6231A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6231B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6234A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6234B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6238A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6238B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6241A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6241B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6245A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6245B' }

]


StartDate = '01012025'
EndDate = '30042025'
PageSize = 39990 # Hay 96 intervalos de 15 minutos en un día, con lo que 39990 intervalos cubren desde el 1 de enero de 2025 hasta el 31 de marzo de 2025

# Función para obtener los datos de tráfico
def get_traffic_data(Id):
    url = f'https://webtris.nationalhighways.co.uk/api/v1.0/reports/daily?sites={Id}&start_date={StartDate}&end_date={EndDate}&page=1&page_size={PageSize}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Función para obtener los datos de calidad
def get_quality_traffic_data(Id):
    url = f'https://webtris.nationalhighways.co.uk/api/v1.0/quality/daily?siteid={Id}&start_date={StartDate}&end_date={EndDate}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Función para obtener el Id de M6
def get_Id_M6(Site):
    url = 'https://webtris.nationalhighways.co.uk/api/v1.0/sites'
    response = requests.get(url)
    # Verificar si la respuesta es exitosa
    if response.status_code == 200:
        data = response.json()
        # Verificar si la clave 'sites' está en la respuesta
        if 'sites' in data:
            # Iterar sobre los sitios y buscar el Id correspondiente
            for row in data['sites']:
                desc = row.get('Description', '').strip().upper()
                site = Site.strip().upper()
                # Comparar el nombre del sitio con la descripción
                if desc == site:
                    # Si coinciden, devolver el Id
                    return row.get('Id')
        else:
            print("No 'Sites' key in API response!")
            
    else:
        print(f"Error: {response.status_code}")
    return None

# Apendar los Ids a la lista locations2
for location in locations2:
    site_name = location['Site']
    site_id = get_Id_M6(site_name)
    location['Id'] = site_id  
    
# Verificar que se han añadido los Ids correctamente
#print(locations2)  

# Apendar los Ids a la lista locations3
for location in locations3:
    site_name = location['Site']
    site_id = get_Id_M6(site_name)
    location['Id'] = site_id  

# Lista para almacenar los datos
data=[]
for location in locations:
    # Construir la URL para cada ubicación
    Id = location['Id']
    traffic_data = get_traffic_data(Id)
    quality_data = get_quality_traffic_data(Id)

    # Crear un diccionario para almacenar los datos de calidad por fecha
    qualitybyDate = {}
    # Verificar si se obtuvo la respuesta y si contiene datos
    if quality_data and 'Qualities' in quality_data:
        for q in quality_data['Qualities']:
            # Extraer los datos de calidad
            date = q.get('Date', '')[:10]
            qualitybyDate[date] = q.get('Quality', '')
    else:
        print(f"No quality data found for {location['Site']} with Id {Id}")


    #print(traffic_data)
    # Verificar si se obtuvo la respuesta y si contiene datos
    if traffic_data and 'Rows' in traffic_data:
        # Extraer los datos que nos interesan
        for row in traffic_data['Rows']:
            Date = row.get('Report Date')
            TimeInterval = row.get('Time Interval')
            AverageSpeed = row.get('Avg mph')
            TotalTraffic = row.get('Total Volume')
            Cars0520 = row.get('0 - 520 cm')
            Cars521660 = row.get('521 - 660 cm')
            Cars6611160 = row.get('661 - 1160 cm')
            Cars1161 = row.get('1160+ cm') 
            quality = qualitybyDate.get(Date[:10] if Date else None)
            # Agregar los datos a la lista
            data.append({
                'Highway': location['Highway'],
                'Id': location['Id'],
                'Site': location['Site'],
                'Date': Date,
                'TimeInterval': TimeInterval,
                'Cars 0 - 520 cm': Cars0520,
                'Cars 521 - 660 cm': Cars521660,
                'Cars 661 - 1160 cm': Cars6611160,
                'Cars 1160+ cm': Cars1161,
                'AverageSpeed': AverageSpeed,
                'TotalTraffic': TotalTraffic,
                'Quality': quality
            })

        #print(data)
    else:
        print(f"No data found for {location['Site']} with Id {Id}")
    
    """
    Este codigo es el antiguo para extraer los datos de calidad, esta aquí por si se necesita
    if quality_data and 'Qualities' in quality_data:
        # Extraer los datos de calidad
        for row in quality_data['Qualities']:
            Quality = row.get('Quality')
            data.append({
                'Quality' : Quality
            })
    else :
        print(f"No quality data found for {location['Site']} with Id {Id}") 

    """    
   
for location in locations2:
    # Construir la URL para cada ubicación
    Id = location['Id']
    traffic_data = get_traffic_data(Id)
    quality_data = get_quality_traffic_data(Id)

    # Crear un diccionario para almacenar los datos de calidad por fecha
    qualitybyDate = {}
    # Verificar si se obtuvo la respuesta y si contiene datos
    if quality_data and 'Qualities' in quality_data:
        for q in quality_data['Qualities']:
            # Extraer los datos de calidad
            date = q.get('Date', '')[:10]
            qualitybyDate[date] = q.get('Quality', '')
    else:
        print(f"No quality data found for {location['Site']} with Id {Id}")
    # Verificar si se obtuvo la respuesta y si contiene datos
    if traffic_data and 'Rows' in traffic_data:
        # Extraer los datos que nos interesan
        for row in traffic_data['Rows']:
            Date = row.get('Report Date')
            TimeInterval = row.get('Time Interval')
            AverageSpeed = row.get('Avg mph')
            TotalTraffic = row.get('Total Volume')
            Cars0520 = row.get('0 - 520 cm')
            Cars521660 = row.get('521 - 660 cm')
            Cars6611160 = row.get('661 - 1160 cm')
            Cars1161 = row.get('1160+ cm') 
            quality = qualitybyDate.get(Date[:10] if Date else None)
            # Agregar los datos a la lista
            data.append({
                'Highway': location['Highway'],
                'Id': location['Id'],
                'Site': location['Site'],
                'Date': Date,
                'TimeInterval': TimeInterval,
                'Cars 0 - 520 cm': Cars0520,
                'Cars 521 - 660 cm': Cars521660,
                'Cars 661 - 1160 cm': Cars6611160,
                'Cars 1160+ cm': Cars1161,
                'AverageSpeed': AverageSpeed,
                'TotalTraffic': TotalTraffic,
                'Quality': quality
            })

        #print(data)
    else:
        print(f"No data found for {location['Site']} with Id {Id}")
    
for location in locations3:
    # Construir la URL para cada ubicación
    Id = location['Id']
    traffic_data = get_traffic_data(Id)
    quality_data = get_quality_traffic_data(Id)

    # Crear un diccionario para almacenar los datos de calidad por fecha
    qualitybyDate = {}
    # Verificar si se obtuvo la respuesta y si contiene datos
    if quality_data and 'Qualities' in quality_data:
        for q in quality_data['Qualities']:
            # Extraer los datos de calidad
            date = q.get('Date', '')[:10]
            qualitybyDate[date] = q.get('Quality', '')
    else:
        print(f"No quality data found for {location['Site']} with Id {Id}")
    # Verificar si se obtuvo la respuesta y si contiene datos
    if traffic_data and 'Rows' in traffic_data:
        # Extraer los datos que nos interesan
        for row in traffic_data['Rows']:
            Date = row.get('Report Date')
            TimeInterval = row.get('Time Interval')
            AverageSpeed = row.get('Avg mph')
            TotalTraffic = row.get('Total Volume')
            Cars0520 = row.get('0 - 520 cm')
            Cars521660 = row.get('521 - 660 cm')
            Cars6611160 = row.get('661 - 1160 cm')
            Cars1161 = row.get('1160+ cm') 
            quality = qualitybyDate.get(Date[:10] if Date else None)
            # Agregar los datos a la lista
            data.append({
                'Highway': location['Highway'],
                'Id': location['Id'],
                'Site': location['Site'],
                'Date': Date,
                'TimeInterval': TimeInterval,
                'Cars 0 - 520 cm': Cars0520,
                'Cars 521 - 660 cm': Cars521660,
                'Cars 661 - 1160 cm': Cars6611160,
                'Cars 1160+ cm': Cars1161,
                'AverageSpeed': AverageSpeed,
                'TotalTraffic': TotalTraffic,
                'Quality': quality
            })

        #print(data)
    else:
        print(f"No data found for {location['Site']} with Id {Id}")
    
    
# Convertir la lista de datos a un DataFrame de pandas
df = pd.DataFrame(data)
#print(df)
# Guardar el DataFrame en un archivo CSV
#df.to_csv('traffic_data.csv', index=False)
# Guardar el DataFrame en un archivo Excel


# 1,048,575 + 1 cabecero = 1,048,576 filas (límite de Excel)
max_rows = 1048575  
for i, start in enumerate(range(0, len(df), max_rows)):
    end = min(start + max_rows, len(df))
    chunk = df.iloc[start:end].reset_index(drop=True)
    chunk.to_excel(f'traffic_data_part{i+1}.xlsx', index=False)
#df.to_excel('traffic_data.xlsx', index=False)