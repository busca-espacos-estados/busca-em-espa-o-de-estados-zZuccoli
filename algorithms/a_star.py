import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Heurística de Manhattan."""

        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            goal_index = GOAL_STATE.index(tile)

            current_row = index // 3
            current_col = index % 3

            goal_row = goal_index // 3
            goal_col = goal_index % 3

            distance += abs(current_row - goal_row) + abs(current_col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        counter = 0

        frontier = []
        heapq.heappush(frontier, (self.heuristic(initial), counter, initial))

        frontier_set = {initial}
        explored = set()

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)
            frontier_set.remove(current)

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1,
                )

            explored.add(current)
            nodes_expanded += 1

            for neighbor in current.neighbors():
                if neighbor not in explored and neighbor not in frontier_set:
                    counter += 1
                    priority = neighbor.cost + self.heuristic(neighbor)

                    heapq.heappush(frontier, (priority, counter, neighbor))
                    frontier_set.add(neighbor)
                    nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )