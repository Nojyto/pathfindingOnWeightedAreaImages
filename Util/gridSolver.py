import heapq
import func_timeout
from collections import deque

ALGO_TLE_LIMIT = -1

MANHATTAN_MOVEMENT = [(-1, 0), (1, 0), (0, -1), (0, 1)]
EUCLIDEAN_MOVEMENT = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
DIR_OF_MOVEMENT = EUCLIDEAN_MOVEMENT

START_SYMBOL = 'S'
END_SYMBOL = 'E'
PATH_SYMBOL = '#'
EMPTY_SYMBOL = '.'


def TLE(func):
    def function_wrapper(*args):
        try:
            if (ALGO_TLE_LIMIT < 0):
                return func(*args)
            else:
                return func_timeout.func_timeout(ALGO_TLE_LIMIT, func, args=[*args])
        except func_timeout.FunctionTimedOut:
            print("Time limit exceeded on function")
            pass
        return -1, []
    return function_wrapper


def construct_path(seen, start, end, N, M):
    # Create new visual grid
    minPath = [[EMPTY_SYMBOL for _ in range(N)] for _ in range(M)]
    sX, sY = start
    eX, eY = end
    pX, pY = end
    
    # Backtrack on precursors
    while not (sX == pX and sY == pY):
        minPath[pY][pX] = PATH_SYMBOL
        pX, pY = seen[(pX, pY)][1]
    
    # Specify the endings
    minPath[sY][sX] = START_SYMBOL
    minPath[eY][eX] = END_SYMBOL
    
    return minPath

@TLE
def BFS(grid, start, end):
    # Validate start and end points
    if start == (-1, -1) or end == (-1, -1):
        print("Invalid endpoints.")
        return -1, []

    sX, sY = start
    eX, eY = end
    N, M = len(grid[0]), len(grid)
    
    # Initialize the queue with the start position
    q = deque()  # Format: (x, y, prec_x, prec_y)
    q.append((sX, sY, sX, sY))
    seen = dict()
    seen[(sX, sY)] = (grid[sY][sX], (sX, sY))
    
    while q:
        cX, cY, pX, pY = q.popleft()

        # Check if the end point is reached
        if cX == eX and cY == eY:
            # Construct the minimum path
            seen[(eX, eY)] = [seen[(cX, cY)][0] + grid[cY][cX], (pX, pY)]
            return seen[(eX, eY)][0], construct_path(seen, start, end, N, M)
        
        # Explore neighbors
        for dX, dY in DIR_OF_MOVEMENT:
            nX, nY = cX + dX, cY + dY
            if 0 <= nX < N and 0 <= nY < M:
                new_cost = seen[(cX, cY)][0] + grid[nY][nX]  # Add the weight of the grid cell
                if (nX, nY) not in seen or new_cost < seen[(nX, nY)][0]:
                    seen[(nX, nY)] = (new_cost, (cX, cY))
                    q.append((nX, nY, cX, cY))

    return -1, []


@TLE
def Dijkstra(grid, start, end):
    # Validate start and end points
    if start == (-1, -1) or end == (-1, -1):
        print("Invalid endpoints.")
        return -1, []

    sX, sY = start
    eX, eY = end
    N, M = len(grid[0]), len(grid)
    
    # Initialize the heap with the start position
    h = []  # Format: (distance, x, y, previous_x, previous_y)
    heapq.heappush(h, (grid[0][0], sX, sY, sX, sY))
    seen = dict()

    while h:
        cD, cX, cY, pX, pY = heapq.heappop(h)

        # Check if the end point is reached
        if cX == eX and cY == eY:
            # Construct the minimum path
            seen[(cX, cY)] = [cD, (pX, pY)]
            return cD, construct_path(seen, start, end, N, M)

        # Skip already processed or longer paths
        if (cX, cY) in seen and cD >= seen[(cX, cY)][0]: continue
        seen[(cX, cY)] = [cD, (pX, pY)]

        # Explore neighbors
        for dX, dY in DIR_OF_MOVEMENT:
            nX, nY = cX + dX, cY + dY
            if 0 <= nX < N and 0 <= nY < M:
                nD = cD + grid[nY][nX]
                if ((nX, nY) not in seen or nD < seen[(nX, nY)][0]):
                    heapq.heappush(h, (nD, nX, nY, cX, cY))

    return -1, []


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def euclidean_distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
    # return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


@TLE
def Astar(grid, start, end):
    # Validate start and end points
    if start == (-1, -1) or end == (-1, -1):
        print("Invalid endpoints.")
        return -1, []

    sX, sY = start
    eX, eY = end
    N, M = len(grid[0]), len(grid)
    
    # Initialize the heap with the start position
    h = []  # Format: (total_cost, current_distance, x, y, previous_x, previous_y)
    initial_heuristic = euclidean_distance(sX, sY, eX, eY)
    heapq.heappush(h, (initial_heuristic, grid[0][0], sX, sY, sX, sY))
    seen = dict()

    while h:
        total_cost, cD, cX, cY, pX, pY = heapq.heappop(h)

        # Check if the end point is reached
        if cX == eX and cY == eY:
            # Construct the minimum path
            seen[(cX, cY)] = [cD, (pX, pY)]
            return cD, construct_path(seen, start, end, N, M)

        # Skip already processed or longer paths
        if (cX, cY) in seen and cD >= seen[(cX, cY)][0]: continue
        seen[(cX, cY)] = [cD, (pX, pY)]

        # Explore neighbors
        for dX, dY in DIR_OF_MOVEMENT:
            nX, nY = cX + dX, cY + dY
            if 0 <= nX < N and 0 <= nY < M:
                nD = cD + grid[nY][nX]
                heuristic_cost = nD
                
                if DIR_OF_MOVEMENT == MANHATTAN_MOVEMENT:
                    heuristic_cost += manhattan_distance(nX, nY, eX, eY)
                elif DIR_OF_MOVEMENT == EUCLIDEAN_MOVEMENT:
                    heuristic_cost += euclidean_distance(nX, nY, eX, eY)
                    
                if ((nX, nY) not in seen or nD < seen[(nX, nY)][0]):
                    heapq.heappush(h, (heuristic_cost, nD, nX, nY, cX, cY))

    return -1, []


def printGrid(grid):
    print('\n'.join([' '.join(map(str, i)) for i in grid]))