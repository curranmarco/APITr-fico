import pandas as pd
import requests



# Lista de locationsde la M6Toll y la M6 que pasa por dentro de Birmingham
locations = [
    {'Highway' : 'M6Toll', 'Site' : '7671/1' },
    {'Highway' : 'M6Toll', 'Site' : '7671/2' },
    {'Highway' : 'M6Toll', 'Site' : '7672/1' },
    {'Highway' : 'M6Toll', 'Site' : '7672/2' },
    {'Highway' : 'M6Toll', 'Site' : '7673/1' },
    {'Highway' : 'M6Toll', 'Site' : '7673/2' },
    {'Highway' : 'M6Toll', 'Site' : '7674/1' },
    {'Highway' : 'M6Toll', 'Site' : '7674/2' },
    {'Highway' : 'M6Toll', 'Site' : '7675/1' },
    {'Highway' : 'M6Toll', 'Site' : '7675/2' },
    {'Highway' : 'M6Toll', 'Site' : '7676/1' },
    {'Highway' : 'M6Toll', 'Site' : '7676/2' },
    {'Highway' : 'M6Toll', 'Site' : '7677/1' },
    {'Highway' : 'M6Toll', 'Site' : '7678/1' },
    {'Highway' : 'M6Toll', 'Site' : '7678/2' },
    {'Highway' : 'M6Toll', 'Site' : '7679/1' },
    {'Highway' : 'M6Toll', 'Site' : '7679/2' },
    {'Highway' : 'M6Toll', 'Site' : '7680/1' },
    {'Highway' : 'M6Toll', 'Site' : '7680/2' },
    {'Highway' : 'M6Toll', 'Site' : '7681/1' },
    {'Highway' : 'M6Toll', 'Site' : '7681/2' },
    {'Highway' : 'M6Toll', 'Site' : '7682/1' },
    {'Highway' : 'M6Toll', 'Site' : '7682/2' },
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
    {'Highway' : 'M6', 'Site' : 'M6/6040A', 'Id' : '10412' },
    {'Highway' : 'M6', 'Site' : 'M6/6041M' },
    {'Highway' : 'M6', 'Site' : 'M6/6042A', 'Id' : '10562'},
    {'Highway' : 'M6', 'Site' : 'M6/6042J' },
    {'Highway' : 'M6', 'Site' : 'M6/6046B' },
    {'Highway' : 'M6', 'Site' : 'M6/6046A' },
    {'Highway' : 'M6', 'Site' : 'M6/6046L' },
    {'Highway' : 'M6', 'Site' : 'M6/6051J' },
    {'Highway' : 'M6', 'Site' : 'M6/6050B' },
    {'Highway' : 'M6', 'Site' : 'M6/6052A' },
    {'Highway' : 'M6', 'Site' : 'M6/6054B' },
    {'Highway' : 'M6', 'Site' : 'M6/6054A', 'Id' : '10507' },
    {'Highway' : 'M6', 'Site' : 'M6/6054B', 'Id' : '10318' },
    {'Highway' : 'M6', 'Site' : 'M6/6056L' },
    {'Highway' : 'M6', 'Site' : 'M6/6058A', 'Id' : '10563' },
    {'Highway' : 'M6', 'Site' : 'M6/6058B', 'Id' : '10466' },
    {'Highway' : 'M6', 'Site' : 'M6/6061A', 'Id' : '10312' },
    {'Highway' : 'M6', 'Site' : 'M6/6061B',  'Id' : '10425' },
    {'Highway' : 'M6', 'Site' : 'M6/6061L' },
    {'Highway' : 'M6', 'Site' : 'M6/6065A' },
    {'Highway' : 'M6', 'Site' : 'M6/6065J' },
    {'Highway' : 'M6', 'Site' : 'M6/6067B' },
    {'Highway' : 'M6', 'Site' : 'M6/6067A', 'Id' : '10281' },
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
    {'Highway' : 'M6', 'Site' : 'M6/6086B' },
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
    {'Highway' : 'M6 North', 'Site' : 'M6/6197B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6200K' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6206A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6206B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6209A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6209B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6216B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6220A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6220B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6226A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6226B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6231A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6231B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6234A', 'Id' : '19324' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6234B', 'Id' : '19254' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6238A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6238B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6241A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6241B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6245A', 'Id' : '19338' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6245B', 'Id' : '18175' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6248A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6249B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6252A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6252B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6257A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6257B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6260A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6260B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6265A', 'Id' : '19340'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6265B', 'Id' : '19300'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6271A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6271B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6274A', 'Id' : '19242'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6274B', 'Id' : '19140'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6279A', 'Id' : '19230'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6279B', 'Id' : '19431'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6282A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6282B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6282J', 'Id' : '19370'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6283M' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6285A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6285B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6285K', 'Id' : '19425'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6285L', 'Id' : '19160'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6289A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6289B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6292A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6292B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6297A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6297B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6302A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6302B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6304A', 'Id' : '19250'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6304B', 'Id' : '19403'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6307B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6310A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6314A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6314B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6318B', 'Id' : '19210'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6320A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6319B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6324A', 'Id' : '19362'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6324B', 'Id' : '19216'  },
    {'Highway' : 'M6 North', 'Site' : 'M6/6327A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6327B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6330A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6330B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6333A', 'Id' : '19396'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6333B', 'Id' : '19314'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6338A', 'Id' : '19149'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6340B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6340L' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6344A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6344B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6346A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6346B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6349J' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6350B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6350A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6353B', 'Id' : '19248'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6353A', 'Id' : '19289'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6357B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6357A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6361B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6361A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6365A' }, 
    {'Highway' : 'M6 North', 'Site' : 'M6/6365B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6368A', 'Id' : '19145'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6368B', 'Id' : '19340'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6373A', 'Id' : '19415'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6373B', 'Id' : '19426'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6377A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6377B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6380A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6380B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6386A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6386B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6389A', 'Id' : '19200'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6389B', 'Id' : '19299'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6394A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6394B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6398A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6398B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6403A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6403B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6406A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6406B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6412A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6412B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6417A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6417B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6422A', 'Id' : '19294'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6422B', 'Id' : '19241'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6425A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6425B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6431A', 'Id' : '19443'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6431B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6437A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6435B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6442A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6442B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6447A', 'Id' : '19168'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6446B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6452A', 'Id' : '19421'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6452B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6456A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6454B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6462J' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6458B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6461A', 'Id' : '19212'   },
    {'Highway' : 'M6 North', 'Site' : 'M6/6462B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6462M' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6472B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6472A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6477B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6477A' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6491B' },
    {'Highway' : 'M6 North', 'Site' : 'M6/6491A' }

]

# Lista de locations desde que se juntan la M6 y la M6Toll hacia el norte
# TODO Terminar lista de locations de la M6 hacia el norte 

StartDate = '01012025'
EndDate = '30042025'
PageSize = 12000 # Hay 96 intervalos de 15 minutos en un día, con lo que 12000 intervalos cubren desde el 1 de enero de 2025 hasta el 31 de marzo de 2025

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

# Apendar los Ids a la lista locations
for location in locations:
    if 'Id' not in location or not location['Id']:
        site_name = location['Site']
        site_id = get_Id_M6(site_name)
        location['Id'] = site_id  
    
# Verificar que se han añadido los Ids correctamente

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