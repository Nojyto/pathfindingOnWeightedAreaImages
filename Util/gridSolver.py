import heapq
import func_timeout
import math
import time
from collections import deque

ALGO_TLE_LIMIT = -1

MANHATTAN_MOVEMENT = [(1, 0), (-1, 0), (0, 1), (0, -1)]
EUCLIDEAN_MOVEMENT = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
DIR_OF_MOVEMENT = EUCLIDEAN_MOVEMENT

START_SYMBOL = 'S'
END_SYMBOL = 'E'
PATH_SYMBOL = '#'
EMPTY_SYMBOL = '.'
VISITED_SYMBOL = '-'

def TimeoutAndMonitor(func):
    def function_wrapper(*args):
        try:
            start_time = time.time()
            min_dist = -1
            if (ALGO_TLE_LIMIT < 0):
                min_dist, min_path = func(*args)
            else:
                min_dist, min_path = func_timeout.func_timeout(ALGO_TLE_LIMIT, func, args=[*args])
        except func_timeout.FunctionTimedOut:
            print("Time limit exceeded on function")
        except Exception as e:
            print(e)
        else:
            return min_dist, min_path
        finally:
            end_time = round(time.time() - start_time, 3)
            print(f"{func.__name__:<8}\tmin_dist: {round(min_dist, 2)}\tRT: {end_time}s")
        return -1, []
    return function_wrapper


def construct_path(seen, start, end, N, M):
    # Create new visual grid
    minPath = [[EMPTY_SYMBOL for _ in range(N)] for _ in range(M)]
    sX, sY = start
    eX, eY = end
    pX, pY = end
    
    # Mark visited cells
    for (cX, cY), d in seen.items():
        minPath[cY][cX] = VISITED_SYMBOL
    
    # Backtrack on precursors and mark optimal path
    while not (sX == pX and sY == pY):
        minPath[pY][pX] = PATH_SYMBOL
        pX, pY = seen[(pX, pY)][1]
    
    # Specify the endings
    minPath[sY][sX] = START_SYMBOL
    minPath[eY][eX] = END_SYMBOL
    
    return minPath


@TimeoutAndMonitor
def BFS(grid, start, end):
    sX, sY = start
    eX, eY = end
    N, M = len(grid[0]), len(grid)
    # Validate start and end points
    if not (0 <= sX < N and 0 <= sY < M) or not (0 <= eX < N and 0 <= eY < M):
        raise Exception("Start or endpoint is out of bounds")
    
    if start == end:
        raise Exception("Start and end point overlap")
    
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
            return seen[(eX, eY)][0], construct_path(seen, start, end, N, M)
        
        # Explore neighbors
        for dX, dY in DIR_OF_MOVEMENT:
            nX, nY = cX + dX, cY + dY
            if 0 <= nX < N and 0 <= nY < M:
                nD = seen[(cX, cY)][0] + (math.sqrt(2) * grid[nY][nX] if dX != 0 and dY != 0 else grid[nY][nX])
                if (nX, nY) not in seen or nD < seen[(nX, nY)][0]:
                    seen[(nX, nY)] = (nD, (cX, cY))
                    q.append((nX, nY, cX, cY))

    return -1, []


@TimeoutAndMonitor
def Dijkstra(grid, start, end):
    sX, sY = start
    eX, eY = end
    N, M = len(grid[0]), len(grid)
    # Validate start and end points
    if not (0 <= sX < N and 0 <= sY < M) or not (0 <= eX < N and 0 <= eY < M):
        raise Exception("Start or endpoint is out of bounds")
    
    if start == end:
        raise Exception("Start and end point overlap")
    
    # Initialize the heap with the start position
    h = []  # Format: (distance, x, y, previous_x, previous_y)
    heapq.heappush(h, (grid[sY][sX], sX, sY, sX, sY))
    seen = dict()

    while h:
        cD, cX, cY, pX, pY = heapq.heappop(h)

        # Skip already processed or longer paths
        if (cX, cY) in seen: continue
        seen[(cX, cY)] = [cD, (pX, pY)]

        # Check if the end point is reached
        if cX == eX and cY == eY:
            return cD, construct_path(seen, start, end, N, M)

        # Explore neighbors
        for dX, dY in DIR_OF_MOVEMENT:
            nX, nY = cX + dX, cY + dY
            if 0 <= nX < N and 0 <= nY < M:
                nD = cD + (math.sqrt(2) * grid[nY][nX] if dX != 0 and dY != 0 else grid[nY][nX])
                if (nX, nY) not in seen or nD < seen[(nX, nY)][0]:
                    heapq.heappush(h, (nD, nX, nY, cX, cY))

    return -1, []


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def euclidean_distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
    # return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


@TimeoutAndMonitor
def Astar(grid, start, end):
    sX, sY = start
    eX, eY = end
    N, M = len(grid[0]), len(grid)
    # Validate start and end points
    if not (0 <= sX < N and 0 <= sY < M) or not (0 <= eX < N and 0 <= eY < M):
        raise Exception("Start or endpoint is out of bounds")

    if start == end:
        raise Exception("Start and end point overlap")
    
    heuristic = manhattan_distance if DIR_OF_MOVEMENT == EUCLIDEAN_MOVEMENT else euclidean_distance
    initial_heuristic = heuristic(sX, sY, eX, eY)
    # Initialize the queue with the start position
    h = [] # Format: (heuristic, distance, x, y, previous_x, previous_y)
    heapq.heappush(h, (initial_heuristic + grid[sY][sX], grid[sY][sX], sX, sY, sX, sY))
    seen = dict()

    while h:
        _, cD, cX, cY, pX, pY = heapq.heappop(h)

        # Skip already processed or longer paths
        if (cX, cY) in seen: continue
        seen[(cX, cY)] = (cD, (pX, pY))
        
        # Check if the end point is reached
        if cX == eX and cY == eY:
            return cD, construct_path(seen, start, end, N, M)

        # Explore neighbors
        for dX, dY in DIR_OF_MOVEMENT:
            nX, nY = cX + dX, cY + dY
            if 0 <= nX < N and 0 <= nY < M:
                nD = cD + (math.sqrt(2) * grid[nY][nX] if dX != 0 and dY != 0 else grid[nY][nX])
                total_cost = nD + heuristic(nX, nY, eX, eY)
                if (nX, nY) not in seen or nD < seen[(nX, nY)][0]:
                    heapq.heappush(h, (total_cost, nD, nX, nY, cX, cY))

    return -1, []


def printGrid(grid):
    print('\n'.join([' '.join(map(str, i)) for i in grid]))