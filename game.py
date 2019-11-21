from datetime import datetime

def main_loop():
	before = datetime.now()

	FIELD = [0, 0, 0, 0, 0, 0, 0, 0]

	SPEED = (10**6 - 10000) 

	DIRECTIONS = {"LEFT": -1, "RIGHT": 1}

	BALL_POSITION = 0

	DIRECTION = "RIGHT"

	while True:

		now = datetime.now()
		td = now - before
		td = td.seconds * 10**6 + td.microseconds

		if td > SPEED:
			try:
				before = now

				NEW_BALL_POSITION = BALL_POSITION + DIRECTIONS[DIRECTION]
				if NEW_BALL_POSITION == -1:
					raise IndexError

				FIELD[NEW_BALL_POSITION] = 1
				FIELD[BALL_POSITION] = 0
				BALL_POSITION = NEW_BALL_POSITION
				print(FIELD)
				

			except IndexError:
				if DIRECTION == "RIGHT":
					DIRECTION = "LEFT"
				else: 
					DIRECTION = "RIGHT"
				


if __name__ == '__main__':
	main_loop()

