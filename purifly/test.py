from core import Pipe, Sequencer
from monad import Option

def test_seq():
    class AddOnePipe(Pipe[int]):
        def map(self, data):
            return data.map(lambda x: x+1)

    p0 = AddOnePipe()
    p1 = AddOnePipe()
    p2 = Sequencer([p0, p1])
    res = p2(Option.some(5))
    
    assert res == Option.some(7)
    print(res)

test_seq()