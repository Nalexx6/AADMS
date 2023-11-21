class RegionalAutomaton:
    def __init__(self, timed_automaton):
        self.states = {}
        self.transitions = []
        self.timed_automaton = timed_automaton

    def add_state(self, state, clock_values):
        self.states[state] = {'clock_values': clock_values}

    def add_transition(self, source, target, action, guard):
        self.transitions.append({
            'source': source,
            'target': target,
            'action': action,
            'guard': guard
        })

    def generate_regional_automaton(self):
        for initial_state in self.timed_automaton.initial_states:
            self.add_state((initial_state, 0), clock_values={})

        for transition in self.timed_automaton.transitions:
            source, action, target, guard = transition
            source_state, source_region = source
            target_state, target_region = target

            next_region = self.find_next_region(source_region)

            source_state_new = (source_state, next_region)
            target_state_new = (target_state, target_region)

            self.add_state(source_state_new, clock_values={})
            self.add_transition(source_state_new, target_state_new, action, guard)

    def find_next_region(self, current_region):
        next_region = current_region + 1

        return next_region


class TimedAutomaton:
    def __init__(self):
        self.states = {'a0', 'a1', 'a2'}
        self.initial_states = {'a0'}
        self.alphabet = {'a', 'b'}
        self.transitions = [
            (('a0', 0), 'a', ('a0', 0), 'x=1'),
            (('a0', 0), 'a', ('a1', 1), 'y<1'),
            (('a1', 0), 'b', ('a0', 1), 'x<2'),
            (('a1', 0), 'a', ('a2', 0), 'y=2'),
            (('a2', 0), 'a, b', ('a2', 1), 'x=1, y=0'),
        ]


if __name__ == "__main__":
    timed_automaton = TimedAutomaton()
    regional_automaton = RegionalAutomaton(timed_automaton)
    regional_automaton.generate_regional_automaton()

    for state, attributes in regional_automaton.states.items():
        print(f"{state} --{regional_automaton.transitions}--> {state}")