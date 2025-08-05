import unittest
from src.core.fsm import FiniteStateMachine, State
import typing as tp

class TestState(State):
    ANOTHER = 2

class TestFSM(FiniteStateMachine[TestState]):
    def __init__(self, transitions: tp.Dict[TestState, tp.Callable[..., TestState]]):
        super().__init__(TestState, transitions)

class TestFiniteStateMachine(unittest.TestCase):
    def test_initial_state(self):
        class MockFSM(FiniteStateMachine[TestState]):
            def __init__(self, transitions: tp.Dict[TestState, tp.Callable[..., TestState]]):
                super().__init__(TestState, transitions)

        transitions = {
            TestState.INIT: lambda *args, **kwargs: TestState.ANOTHER
        }
        fsm = MockFSM(transitions)
        self.assertEqual(fsm.state, TestState.INIT)

    def test_update_state(self):
        transitions = {
            TestState.INIT: lambda *args, **kwargs: TestState.ANOTHER,
            TestState.ANOTHER: lambda *args, **kwargs: TestState.DEAD
        }
        fsm = TestFSM(transitions)
        fsm.update()
        self.assertEqual(fsm.state, TestState.ANOTHER)

        fsm.update()
        self.assertEqual(fsm.state, TestState.DEAD)

    def test_missing_transition_raises_key_error(self):
        transitions = {
            TestState.INIT: lambda *args, **kwargs: TestState.ANOTHER
        }
        fsm = TestFSM(transitions)
        fsm.update()
        with self.assertRaises(KeyError):
            fsm.update()

    def test_invalid_transition_callable_raises_exception(self):
        invalid_callable = "this is not a callable"
        transitions = {
            TestState.INIT: invalid_callable
        }
        with self.assertRaises(TypeError):
            fsm = TestFSM(transitions)
            fsm.update()

if __name__ == '__main__':
    unittest.main()
