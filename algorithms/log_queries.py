from bppy import *


def test_count_e1_after_e2(bp_log, e1, e2):
    yield {request: e1}
    print(bp_log.count_e1_after_e2(e1, e2))
    yield {request: e2}
    print(bp_log.count_e1_after_e2(e1, e2))
    yield {request: e1}
    print(bp_log.count_e1_after_e2(e1, e2))


def test_e1_after_e2(bp_log, e1, e2):
    yield {request: e1}
    print(bp_log.e1_after_e2(e1, e2))
    yield {request: e2}
    print(bp_log.e1_after_e2(e1, e2))
    yield {request: e1}
    print(bp_log.e1_after_e2(e1, e2))


if __name__ == "__main__":
    b_log = BpLog()
    e1 = BEvent(name="1", data={1: 1})
    e2 = BEvent(name="2", data={2: 1})

    b_program = BProgram(bthreads=[test_count_e1_after_e2(b_log, e1, e2)],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener(),
                         logger=b_log)
    b_program.run()
