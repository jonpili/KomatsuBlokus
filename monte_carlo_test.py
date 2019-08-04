from funcy    import *
from math     import inf, log
from operator import *
from random   import randint


def popcount(x):
    return bin(x).count('1')  # Pythonだと、コレが手軽で速いらしい。


# ゲームの状態。
class State:
    def __init__(self, pieces=0, enemy_pieces=0):
        self.pieces       = pieces
        self.enemy_pieces = enemy_pieces

    @property
    def lose(self):
        return any(lambda mask: self.enemy_pieces & mask == mask, (0b111000000, 0b000111000, 0b000000111, 0b100100100, 0b010010010, 0b001001001, 0b100010001, 0b001010100))

    @property
    def draw(self):
        return popcount(self.pieces) + popcount(self.enemy_pieces) == 9

    @property
    def end(self):
        return self.lose or self.draw

    @property
    def legal_actions(self):
        return tuple(i for i in range(9) if not self.pieces & 0b100000000 >> i and not self.enemy_pieces & 0b100000000 >> i)

    def next(self, action):
        return State(self.enemy_pieces, self.pieces | 0b100000000 >> action)

    def __str__(self):
        ox = ('o', 'x') if popcount(self.pieces) == popcount(self.enemy_pieces) else ('x', 'o')
        return '\n'.join(''.join((ox[0] if self.pieces & 0b100000000 >> i * 3 + j else None) or (ox[1] if self.enemy_pieces & 0b100000000 >> i * 3 + j else None) or '-' for j in range(3)) for i in range(3))


# ランダムで次の手を返します。
def random_next_action(state):
    return state.legal_actions[randint(0, len(state.legal_actions) - 1)]


# アルファ・ベータ法（正確にはネガ・アルファ法）
def nega_alpha(state, alpha, beta):
    if state.lose:
        return -1

    if state.draw:
        return  0

    for action in state.legal_actions:
        score = -nega_alpha(state.next(action), -beta, -alpha)

        if score > alpha:
            alpha = score

        if alpha >= beta:
            return alpha

    return alpha


# 次の手を返します（nega_alphaはスコアを返すので、手を返すようにするためにほぼ同じ関数が必要になっちゃいました）。
def nega_alpha_next_action(state):
    alpha = -inf

    for action in state.legal_actions:
        score = -nega_alpha(state.next(action), -inf, -alpha)

        if score > alpha:
            best_action = action
            alpha       = score

    return best_action


# プレイアウト。
def playout(state):
    if state.lose:
        return -1

    if state.draw:
        return  0

    return -playout(state.next(random_next_action(state)))


def argmax(collection, key=None):
    return collection.index(max(collection, key=key) if key else max(collection))


# モンテカルロ探索。
def monte_carlo_search_next_action(state):
    values = [0] * len(state.legal_actions)

    for i, action in enumerate(state.legal_actions):
        for _ in range(10):
            values[i] += -playout(state.next(action))

    return state.legal_actions[argmax(values)]


# モンテカルロ「木」探索。
def monte_carlo_tree_search_next_action(state):
    class node:
        def __init__(self, state):
            self.state       = state
            self.w           = 0     # 価値
            self.n           = 0     # 試行回数
            self.child_nodes = None  # 子ノード

        def evaluate(self):
            if self.state.end:
                value = -1 if self.state.lose else 0

                self.w += value
                self.n += 1

                return value

            if not self.child_nodes:
                value = playout(self.state)

                self.w += value
                self.n += 1

                if self.n == 10:
                    self.expand

                return value
            else:
                value = -self.next_child_node().evaluate()

                self.w += value
                self.n += 1

                return value

        def expand(self):
            self.child_nodes = tuple(node(self.state.next(action)) for action in self.state.legal_actions)

        def next_child_node(self):
            def ucb1_values():
                t = sum(map(attrgetter('n'), self.child_nodes))

                return tuple(-child_node.w / child_node.n + 2 * (2 * log(t) / child_node.n) ** 0.5 for child_node in self.child_nodes)

            for child_node in self.child_nodes:
                if child_node.n == 0:
                    return child_node

            ucb1_values = ucb1_values()

            return self.child_nodes[argmax(ucb1_values)]

    root_node = node(state)
    root_node.expand()

    for _ in range(100):
        root_node.evaluate()

    return state.legal_actions[argmax(root_node.child_nodes, key=attrgetter('n'))]


def main():
    def first_player_point(ended_state):
        if ended_state.lose:
            return 1 if (popcount(ended_state.pieces) + popcount(ended_state.enemy_pieces)) % 2 == 1 else 0

        return 0.5

    def test_algorithm(next_actions):
        total_point = 0

        for _ in range(100):
            state = State()

            for next_action in cat(repeat(next_actions)):
                if state.end:
                    break;

                state = state.next(next_action(state))

            total_point += first_player_point(state)

        return total_point / 100


    print(test_algorithm((monte_carlo_tree_search_next_action, random_next_action)))
    print(test_algorithm((monte_carlo_tree_search_next_action, nega_alpha_next_action)))


if __name__ == '__main__':
    main()
