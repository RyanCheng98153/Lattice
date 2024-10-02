from src.graph import KagomeGraph
from src.helper import PrintHelper, NodeHelper

class Test:
    @staticmethod
    def checkIsingleNode( _graph: KagomeGraph ):
        helper = NodeHelper(_graph.L, _graph.W)
        n = 0
        while(n >= 0):
            try:
                id = int(input(f"node id you wanna check (0~{ _graph.L * _graph.W -1 }): "))
            except:
                print("invalid input, terminate")
                break
            if ( id >= ( _graph.L * _graph.W -1 ) ):
                print("invalid input")
                continue
            
            if _graph.nodes[id] != None:
                _graph.nodes[id].printNodeVisual(True)
            else:
                print( PrintHelper.getPrettyId(None) + '   ' + PrintHelper.getPrettyId(helper.getRight(id) ) )
                print( '     ' + '   ' + '     ' )
                print( PrintHelper.getPrettyId(helper.getBottom(id)) + '   ' + PrintHelper.getPrettyId(helper.getBottomRight(id) ) )
                