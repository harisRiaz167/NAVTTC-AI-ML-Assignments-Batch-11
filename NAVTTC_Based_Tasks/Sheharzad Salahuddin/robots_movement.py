class Solution:
    def judgeCircle(self, moves: str) -> bool:
        if len(moves) % 2 != 0:
            return False

        x, y = 0, 0

        directions = {
            'U': (0, 1),
            'D': (0, -1),
            'L': (-1, 0),
            'R': (1, 0)
        }

        print(f"Starting position: ({x}, {y})")

        for move in moves.upper():
            if move not in directions:
                print(f"Invalid move: {move}")
                return False

            dx, dy = directions[move]
            x += dx
            y += dy

            print(f"Move {move} -> Position: ({x}, {y})")

        result = x == 0 and y == 0

        print("Robot returned to origin:", result)
        return result

moves = input("Enter moves (U, D, L, R): ")

robot = Solution()
print("Result:", robot.judgeCircle(moves))